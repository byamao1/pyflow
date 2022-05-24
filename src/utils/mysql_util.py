import pymysql


def connect_db(db_config):
    """
    Connect mysql
    :param host:
    :param user:
    :param password:
    :param database:
    :return:
    """
    conn = pymysql.connect(host=db_config.host, port=db_config.port,
                           user=db_config.user, passwd=db_config.password,
                           database=db_config.database)
    cur = conn.cursor()
    return conn, cur


def close_conn(cursor, connection):
    # 先关闭游标
    cursor.close()

    # 再关闭数据库连接
    connection.close()

