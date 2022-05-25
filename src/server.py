import traceback

from fastapi import FastAPI, WebSocket, Body
from fastapi.requests import Request

import os
import json

from starlette import status
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

import nodemaker
import fbp
from config.log_config import log
from fbp.common import Status

from fbp.port import Port
from routers.ds import ds_router

app = FastAPI()
app.include_router(ds_router)

staticFiles = StaticFiles(directory="static")


@app.middleware("http")
async def add_filter(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        log.exception(e)
    return response


@app.get("/")
async def index(request: Request):
    return await staticFiles.get_response('index.html', request.scope)


@app.get("/nodestree")
def nodestree():
    tree = list()
    repository = fbp.repository()
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


@app.get("/nodes")
def nodes():
    repository = fbp.repository()
    node_specs = repository.get("nodespec")

    if not node_specs:
        return {}

    # Adding default output when it is not there
    for k, v in node_specs.items():
        if "output" not in v.get("port", []):
            v["port"]["output"] = list()
            v["port"]["output"].append({"name": "out"})

    return node_specs


@app.post("/nodes")
def nodes(node: dict):
    repository = fbp.repository()
    repository.register("nodespec", node["id"], node)
    return node


@app.get("/nodes/{node_id}")
def get_node(node_id):
    repository = fbp.repository()
    node = repository.get("nodespec", node_id)
    return node


@app.delete("/nodes/{node_id}")
def del_node(node_id):
    repository = fbp.repository()
    repository.unregister("nodespec", node_id)
    return {'success': True}


@app.put("/nodes/{node_id}")
def update_node(node_id, node: dict):
    repository = fbp.repository()
    # TODO Valude the node here
    repository.register("nodespec", node_id, node)
    return node


@app.get("/flows")
def get_flows():
    repository = fbp.repository()

    flows = repository.get("flow")
    if flows is None:
        return {}

    result = [v for k, v in flows.items()]
    return result


@app.post("/flows")
def add_flows(flow: dict):
    repository = fbp.repository()
    repository.register("flow", flow["id"], flow)
    return flow


@app.get("/flows/{node_id}")
def get_flow(node_id):
    repository = fbp.repository()
    node = repository.get("flow", node_id)
    return node


@app.websocket("/ws_runflow")
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


@app.post("/runflow")
def runflow(flow_spec: dict):
    try:
        return fbp.run_flow_once(flow_spec)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})


@app.post("/dumprepo")
def dumprepo(data: dict):
    try:
        repository = fbp.repository()
        repository.dumps(data["path"])
        return data
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})


@app.post("/loadrepo")
def loadrepo(data: dict):
    try:
        repository = fbp.repository()
        repository.loads(data["path"])
        return data
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})


@app.get("/ports/types")
def get_supported_port_types():
    return list(Port.support_types())


app.mount(r"/", staticFiles, name="static")


def load_node_spec():
    records = []
    for file in os.listdir('node_specs'):
        if file.endswith('.py') and file != '__init__.py':
            with open('node_specs' + os.path.sep + file)as f:
                spec = nodemaker.create_node_spec(f.read())
                records.append(json.dumps(spec))

    repository = fbp.repository()
    for r in records:
        node = json.loads(r)
        repository.register("nodespec", node["id"], node)


def init():
    # load node spec from spec folders
    # load_node_spec()

    # TODO
    # initialize flows
    pass


if __name__ == "__main__":
    init()

    import uvicorn
    uvicorn.run(app='server:app', host="0.0.0.0", port=5000,
                workers=1, #os.cpu_count()//4,  # worker数设置，如果不设置就是1个worker
                reload=False, debug=False,  # 在生产环境，这两个参数必须是False，否则多进程性能将下降
                )
