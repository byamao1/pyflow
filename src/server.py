from fastapi import FastAPI
from fastapi.requests import Request

import os
import json

from starlette.staticfiles import StaticFiles

import nodemaker
import fbp
from config.log_config import log

from routers.ds import ds_router
from routers.common import common_router

app = FastAPI()
app.include_router(ds_router)
app.include_router(common_router)

staticFiles = StaticFiles(directory="static")


@app.get("/")
async def index(request: Request):
    return await staticFiles.get_response('index.html', request.scope)


@app.middleware("http")
async def add_filter(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        log.exception(e)
    return response


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
                workers=1,  # os.cpu_count()//4,  # worker数设置，如果不设置就是1个worker
                reload=False, debug=False,  # 在生产环境，这两个参数必须是False，否则多进程性能将下降
                )
