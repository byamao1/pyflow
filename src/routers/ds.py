#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/22 11:52
# @Author  : Tom
import os

from fastapi import APIRouter, Body, UploadFile

import pandas as pd
from fastapi.params import File

from config.constants import ReturnMsg
from config.path_config import TMP_DIR
from dto.db_connect import DbConfig
from utils.mysql_util import connect_db, close_conn
from utils.time_util import get_now_str

ds_router = APIRouter(tags=["Data input"], )


@ds_router.post("/test_db_conn", summary='Test db', description='Test database connect', )
def test_db_conn(db_config: DbConfig = Body(..., example={"host": "rm-uf607hj14l5cl21o7fo.mysql.rds.aliyuncs.com",
                                                          "port": 3306,
                                                          "user": "aiit_jie",
                                                          "password": "Aiit-jie-jkwerouioer",
                                                          "database": "test"
                                                          })):
    try:
        cursor, conn = connect_db(db_config)
        close_conn(cursor, conn)
        return ReturnMsg.SUCCESS
    except Exception as e:
        return str(e)


@ds_router.post("/read_table", summary='Read table', description='Read database table', )
def read_table(body: dict = Body(..., example={"db_config": {"host": "rm-uf607hj14l5cl21o7fo.mysql.rds.aliyuncs.com",
                                                             "port": 3306,
                                                             "user": "aiit_jie",
                                                             "password": "Aiit-jie-jkwerouioer",
                                                             "database": "test"
                                                             },
                                               "sql": "select id, x from ts_data_repair",
                                               "limit": 20
                                               })):
    try:
        db_config = body['db_config']
        sql = str(body['sql'])
        limit_num = int(body['limit'])

        # Check sql containing 'limit'
        if 'limit' not in sql.lower():
            sql = f'{sql} limit {limit_num}'

        import pymysql
        conn = pymysql.connect(host=db_config['host'], port=db_config['port'],
                               user=db_config['user'], passwd=db_config['password'],
                               database=db_config.get('database', None))
        df = pd.read_sql(sql=sql, con=conn)
        conn.close()

        # Limit number
        if len(df) > limit_num:
            df = df[:limit_num]
        return df.to_dict(orient="list")
    except Exception as e:
        return str(e)


@ds_router.post("/upload_file", summary='Upload file', description='Upload file', )
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()

    # Check tmp dir
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    tmp_file_path = os.path.join(TMP_DIR, f"{get_now_str('%Y%m%d%H%M%S%f')}-{file.filename}")
    with open(tmp_file_path, 'wb') as f:
        f.write(contents)
    return tmp_file_path
