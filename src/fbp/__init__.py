"""Flow library"""
import json
import time

from fastapi import WebSocket

from config.constants import EXEC_MODE_STREAMING
from config.log_config import log
from fbp.node import Node
from fbp.flow import Flow
from fbp.repository import repository


__version_info__ = (0, 0, 1)
__version__ = ".".join(map(str, __version_info__))


def create_node(spec_id, id, name):
    spec = repository().get("nodespec", spec_id)

    if spec is None:
        raise Exception("No such node specification {}".format(spec_id))

    if type(spec) is not dict:
        try:
            spec_obj = json.loads(spec, strict=False)
        except Exception as e:
            raise Exception("Invalid node specification {}".format(spec))

        anode = Node(id, name, spec_obj)
        return anode

    anode = Node(id, name, spec)
    return anode

# Run a flow based on a defined specification of flow
# Todo consider unify the flow definition spec and running spec


def _parse_flow(flow_spec):
    flow_spec_obj = None

    if type(flow_spec) is not dict:
        try:
            flow_spec_obj = json.loads(flow_spec, strict=False)
        except Exception as e:
            # print "invalid flow specification format"
            raise e
    else:
        flow_spec_obj = flow_spec

    aflow = Flow(flow_spec_obj.get("id"), flow_spec_obj.get("name"))

    end_node_list = []
    for node_def in flow_spec_obj.get("nodes"):
        anode = create_node(node_def.get("spec_id"),
                            node_def.get("id"), node_def.get("name"))
        aflow.add_node(anode)
        if "is_end" in node_def.keys() and node_def.get("is_end") == 1:
            end_node_list.append(anode)
        for port_def in node_def.get("ports"):
            anode.set_inport_value(port_def.get("name"), port_def.get("value"))

    for link_def in flow_spec_obj.get("links"):
        source = link_def.get("source").split(":")
        target = link_def.get("target").split(":")

        aflow.link(source[0], source[1], target[0], target[1])

    # Generate func of all nodes in flow
    aflow.generate_node_func()

    nodemap = end_node_list.copy()
    aflow.find_source_nodes(end_node_list, nodemap)
    return aflow, nodemap


async def run_flow_streaming(flow_spec, interval, websocket: WebSocket):
    """
    Run flow by streaming
    :param flow_spec:
    :param interval: Unit is ms
    :param websocket:
    """
    aflow, nodemap = _parse_flow(flow_spec)
    try:
        ret_msg = await aflow.run_streaming(nodemap, interval=interval, websocket=websocket)
        log.info(ret_msg)
    except Exception as e:
        log.exception(e)


def run_flow_once(flow_spec):
    aflow, nodemap = _parse_flow(flow_spec)
    stat = aflow.run_once(nodemap)

    # TODO : support run in async mode
    while not stat.check_stat():
        time.sleep(0.1)
    return [i for i in stat.result()]
