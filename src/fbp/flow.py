"""Core Class for Flow."""
import asyncio
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
import sys
import json
from fastapi import WebSocket
from config.Constants import EXEC_MODE_BATCH, EXEC_MODE_STREAMING, STREAMING_LOOP_WAIT_MSG
from config.log_config import log
from fbp.common import Command, Status
from fbp.node import Node
from fbp.port import Port


class Path(object):
    def __init__(self, source_node, source_port, target_node, target_port):
        self._name = source_node.id + ":" + source_port.name + \
            "~" + target_node.id + ":" + target_port.name
        self._source_node = source_node
        self._target_node = target_node
        self._source_port = source_port
        self._target_port = target_port

    @property
    def name(self):
        return self._name

    @property
    def source_node(self):
        return self._source_node

    @property
    def source_port(self):
        return self._source_port

    @property
    def target_node(self):
        return self._target_node

    @property
    def target_port(self):
        return self._target_port


def _gen_lable(node, port):
    return node.id + ":" + port.name


class FlowStates(object):
    def __init__(self):
        self._result = list()
        self._complete = False

    def check_stat(self):
        return self._complete

    def result(self):
        return self._result

    def append_stat(self, node):
        self._result.append(node)

    def set_stat(self, is_complete):
        self._complete = is_complete

    def get_result_by_id(self, id):
        for r in self._result:
            if r["id"] == id:
                return r
        return None


class Flow(object):

    def __init__(self, id, name, mode: str = EXEC_MODE_BATCH):
        self._name = name
        self._id = id
        self._nodes = dict()
        self._links = dict()
        self._mode = mode

    def add_node(self, node):
        self._nodes[node.id] = node

    def get_node(self, id):
        return self._node.get(id)

    def get_nodes(self):
        return self._nodes.values()

    def remove_node(self, node_id):
        if self._nodes.get(node_id) is not None:
            del self._nodes[node_id]

    def generate_node_func(self):
        for n in self._nodes.values():
            n.generate_node_func()

    def link(self, source_node_id, source_port_name, target_node_id, target_port_name):

        # TODO : link should do data transfer if source port contains data
        if self._nodes.get(source_node_id) is None:
            raise Exception(
                "The source node {} is not in the flow".format(source_node_id))

        if self._nodes.get(target_node_id) is None:
            raise Exception(
                "The target node {} is not in the flow".format(target_node_id))

        source_node = self._nodes.get(source_node_id)
        target_node = self._nodes.get(target_node_id)
        source_port = source_node.get_port(source_port_name, Port.TYPE_OUT)
        target_port = target_node.get_port(target_port_name, Port.TYPE_IN)

        if source_port is None:
            raise Exception("The source port {} is not in the node {}".format(
                source_port_name, source_node_id))

        if target_port is None:
            raise Exception("The target port {} is not in the node {}".format(
                target_port_name, target_node_id))

        # source lable is not used
        source_label = _gen_lable(source_node, source_port)
        target_label = _gen_lable(target_node, target_port)

        link_to_target = self._links.get(target_label)
        if link_to_target is not None:
            raise Exception(
                "Link to target port {} already exist, unlink first!".format(target_label))

        # bi-directional link the port
        target_port.point_from(source_port)
        source_port.point_to(target_port)

        self._links[target_label] = Path(
            source_node, source_port, target_node, target_port)

    # def unlink(self, target_node_id, target_port_name):
    #     target_label = target_node_id + ":" + target_port_name
    #     link_to_target = self._links.get(target_label)
    #     if link_to_target is not None:
    #         link_to_target.source_port.un_point_to(link_to_target.target_port)
    #         link_to_target.target_port.point_from(None)
    #         del self._links[target]

    def get_links(self):
        return self._links

    def _find_dependant_nodes(self, target_node, source_nodes):
        in_ports = target_node.get_ports(Port.TYPE_IN)
        children = []
        for p in in_ports:
            link_to_p = self._links.get(_gen_lable(target_node, p))
            if link_to_p is not None:
                children.append(link_to_p.source_node)
                if link_to_p.source_node in source_nodes:
                    source_nodes.remove(link_to_p.source_node)
                source_nodes.append(link_to_p.source_node)
        return children

    def find_source_nodes(self, target_nodes, source_nodes):
        # TODO : Add loop check
        children = target_nodes
        new_children = []
        while True:
            for child in children:
                new_children += self._find_dependant_nodes(child, source_nodes)

            if len(new_children) == 0:
                break
            children = new_children
            new_children = []

    def _run_once(self, nodemap, stat):
        while True:
            if len(nodemap) == 0:
                break
            anode = nodemap.pop()
            node_value = anode.get_node_value()

            dep_nodes = list()
            find_failure = False
            for n in self._find_dependant_nodes(anode, dep_nodes):
                if n._status in [Status.FAIL, Status.SKIP]:
                    node_value["status"] = Status.SKIP
                    node_value["error"] = "skip due to denpendency node failure"
                    stat.append_stat(node_value)
                    find_failure = True
                    break

            if find_failure:
                # break incase there is depedency failure
                break

            try:
                if anode.get_port("loop_n", Port.TYPE_IN) is not None:
                    anode.set_inport_value("loop_n", 0)
                anode.run()
                node_value = anode.get_node_value()
            except Exception as e:
                node_value = anode.get_node_value()
                node_value["status"] = Status.FAIL
                node_value["error"] = str(e)
            finally:
                stat.append_stat(node_value)

        stat.set_stat(True)

    def run_once(self, nodemap:list):
        BaseManager.register('FlowStates', FlowStates)
        BaseManager.register('Node', Node)
        manager = BaseManager()
        manager.start()
        stat = manager.FlowStates()

        # p = Process(target=self._run_batch, args=(end_node, stat))
        # p.start()
        self._run_once(nodemap, stat)
        return stat

    async def run_streaming(self, nodemap, interval, websocket: WebSocket) -> str:
        """

        :param nodemap:
        :param interval: Unit is ms
        :param websocket:
        """
        node_i = 0
        loop_n = 0
        while True:
            if len(nodemap) == 0:
                return "Node number is 0"
            # Reset
            if node_i <= -1 * len(nodemap):
                node_i = 0
                # If receive stop message
                try:
                    msg = await asyncio.wait_for(websocket.receive_text(), STREAMING_LOOP_WAIT_MSG)
                    log.debug(f"msg: {msg}")
                    if msg == Command.STOP:
                        return "Streaming flow is stopped by client."
                except asyncio.TimeoutError:
                    pass
                # Run flow interval
                await asyncio.sleep(interval / 1000)

            node_i -= 1
            anode = nodemap[node_i]
            node_value = anode.get_node_value()

            dep_nodes = list()
            find_failure = False
            for n in self._find_dependant_nodes(anode, dep_nodes):
                if n._status in [Status.FAIL, Status.SKIP]:
                    node_value["status"] = Status.SKIP
                    node_value["error"] = "skip due to denpendency node failure"
                    await websocket.send_text([node_value])
                    find_failure = True
                    return f"Node status is [{n._status}]"

            if find_failure:
                # break incase there is depedency failure
                return "Find failure"

            try:
                if anode.get_port("loop_n", Port.TYPE_IN) is not None:
                    anode.set_inport_value("loop_n", loop_n)
                    anode.set_inport_value("db_config", {"host": "rm-uf607hj14l5cl21o7fo.mysql.rds.aliyuncs.com",
                                                         "port": 3306,
                                                         "user": "aiit_jie",
                                                         "password": "Aiit-jie-jkwerouioer",
                                                         "database": "test"
                                                         })
                    anode.set_inport_value("sql", "select id, x from ts_data_repair")
                    anode.set_inport_value("axis_col_map", {'x': 'id', 'y': 'x'})
                    anode.set_inport_value("window_config", {"window_len": 1000, "shift_len": 30})

                anode.run()
                node_value = anode.get_node_value()
            except Exception as e:
                node_value = anode.get_node_value()
                node_value["status"] = Status.FAIL
                node_value["error"] = str(e)
            finally:
                await websocket.send_text(json.dumps([node_value]))

            loop_n += 1


