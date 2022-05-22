#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/22 11:52
# @Author  : Tom
from fastapi import APIRouter, Body

from config.Constants import ReturnMsg
from dto.db_connect import DbConfig
from utils.mysql_util import connect_db, close_conn

router = APIRouter(tags=["Data input"],)


@router.post("/test_db_conn", summary='Test db', description='Test database connect', )
def test_db_conn(db_config: DbConfig = Body(..., example={"host": "rm-uf607hj14l5cl21o7fo.mysql.rds.aliyuncs.com",
                                                          "port": 3306,
                                                          "user": "aiit_jie",
                                                          "password": "Aiit-jie-jkwerouioer",
                                                          "database": "mysql"
                                                          })):
    try:
        cursor, conn = connect_db(db_config)
        close_conn(cursor, conn)
        return ReturnMsg.SUCCESS
    except Exception as e:
        return str(e)