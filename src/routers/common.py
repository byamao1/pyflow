#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/27 18:07
# @Author  : Tom
import traceback

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse
from fastapi import WebSocket

import fbp
from fbp.common import Status
from fbp.port import Port

from config.log_config import log


common_router = APIRouter(tags=["Common"], )


@common_router.get("/nodestree")
def nodestree():
    tree = list()
    repository = fbp.NodeRepository()
    node_specs = repository.get("nodespec")

    for k, v in node_specs.iteritems():
        _insert(tree, v)
    return tree


def _insert(treeroot, node):
    node_id = node["id"]
    ids = node_id.split(".")
    found = False

    for n in treeroot:
        if n["id"] == ids[0]:
            found = True
            _inset_node(n, node, ids)

    if not found:
        item = dict()
        item["id"] = ids[0]
        item["title"] = ids[0]
        item["children"] = list()
        treeroot.append(item)
        _inset_node(item, node, ids)

    return


def _inset_node(parent, node, path):
    if len(path) == 1:
        if path[0] == parent["id"]:
            parent["value"] = node
    else:
        if path[0] == parent["id"]:
            children = parent["children"]
            found = False
            for item in children:
                if item["id"] == path[1]:
                    _inset_node(item, node, path[1:])
                    found = True

            if not found:
                item = dict()
                item["id"] = path[1]
                item["title"] = path[1]
                item["children"] = list()
                parent["children"].append(item)
                _inset_node(item, node, path[1:])
    return


@common_router.get("/nodes")
def nodes():
    repository = fbp.NodeRepository()
    node_specs = repository.get("nodespec")

    if not node_specs:
        return {}

    # Adding default output when it is not there
    for k, v in node_specs.items():
        if "output" not in v.get("port", []):
            v["port"]["output"] = list()
            v["port"]["output"].append({"name": "out"})

    return node_specs


@common_router.post("/nodes")
def nodes(node: dict):
    repository = fbp.NodeRepository()
    repository.register("nodespec", node["id"], node)
    return node


@common_router.get("/nodes/{node_id}")
def get_node(node_id):
    repository = fbp.NodeRepository()
    node = repository.get("nodespec", node_id)
    return node


@common_router.delete("/nodes/{node_id}")
def del_node(node_id):
    repository = fbp.NodeRepository()
    repository.unregister("nodespec", node_id)
    return {'success': True}


@common_router.put("/nodes/{node_id}")
def update_node(node_id, node: dict):
    repository = fbp.NodeRepository()
    # TODO Valude the node here
    repository.register("nodespec", node_id, node)
    return node


@common_router.get("/flows")
def get_flows():
    repository = fbp.FlowRepository()

    flows = repository.get("flow")
    if flows is None:
        return {}

    result = [v for k, v in flows.items()]
    return result


@common_router.post("/flows")
def add_flows(flow: dict):
    repository = fbp.FlowRepository()
    repository.register("flow", flow["id"], flow)
    return flow


@common_router.get("/flows/{node_id}")
def get_flow(node_id):
    repository = fbp.FlowRepository()
    node = repository.get("flow", node_id)
    return node


@common_router.websocket("/ws_runflow")
async def ws_runflow(websocket: WebSocket):
    await websocket.accept()

    while True:
        from starlette.websockets import WebSocketDisconnect
        try:
            body_dict = await websocket.receive_json()
            await fbp.run_flow_streaming(body_dict['flow'], body_dict['interval'], websocket)
            await websocket.send_text(Status.END)
            await websocket.close()
        except WebSocketDisconnect as e:
            log.info('Websocket disconnect')


@common_router.post("/runflow")
def runflow(flow_spec: dict):
    try:
        return fbp.run_flow_once(flow_spec)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})


@common_router.post("/dumprepo")
def dumprepo(data: dict):
    try:
        repository = fbp.FlowRepository()
        repository.dumps(data["path"])
        return data
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})


@common_router.post("/loadrepo")
def loadrepo(data: dict):
    try:
        repository = fbp.FlowRepository()
        repository.loads(data["path"])
        return data
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})


@common_router.get("/ports/types")
def get_supported_port_types():
    return list(Port.support_types())
