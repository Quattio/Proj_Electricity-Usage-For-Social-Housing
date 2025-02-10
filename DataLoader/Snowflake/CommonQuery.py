def query_define(extractVariables, table, clientid, startTime, endTime):
    columns = ', '.join(extractVariables)
    base_query = f"""
        SELECT
            {columns}
        FROM
            {table}
        WHERE
            clientid = %(clientid)s
    """
    if startTime is not None and endTime is not None:
        base_query += """
            AND time_ts BETWEEN %(startTime)s AND %(endTime)s
        """
    params = {
        'clientid'        : clientid,
        'startTime'       : startTime,
        'endTime'         : endTime
    }
    return base_query, params

def listDataBases():
    # DataBases: "default" and "system" 
    return f'''
    SHOW DATABASES
    '''

def listTables():
    return f'''
    SHOW TABLES
    '''

def test():
    return f'''
        SELECT
            HP1_LIMITEDBYCOP
        FROM
            FIREHOSE_CIC.CIC.STATS_DYNAMIC
        WHERE
            -- CLIENTID LIKE 'cic-5795534%'
            CLIENT_TIME BETWEEN '2024-12-30 00:00:00' AND '2024-12-30 00:59:59'
    '''

