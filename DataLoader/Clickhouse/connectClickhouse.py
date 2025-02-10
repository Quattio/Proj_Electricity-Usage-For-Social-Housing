import clickhouse_connect
from .loadClickHouseCredentials import clickhouse_host, clickhouse_user, clickhouse_password, clickhouse_port
from . import CommonQuery

def connect_clickhouse(arguments):

    # Connect Clickhouse
    client = clickhouse_connect.get_client(
        host     = clickhouse_host,
        user     = clickhouse_user,
        password = clickhouse_password,
        port     = clickhouse_port,
        secure   = True
    )

    # Execute Query
    if arguments.query == None:
        query, params = CommonQuery.query_define(arguments.extractVariables,
                                    arguments.table,
                                    arguments.clientid,
                                    arguments.startTime,
                                    arguments.endTime)
        df = client.query_df(query, params)
    else:
        df = client.query_df(getattr(CommonQuery, arguments.query)())

    return df


