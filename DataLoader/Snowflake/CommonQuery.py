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

def gethousedata():
    return f'''
    SELECT DISTINCT c.CLIENTID, c.E_hp1, c.E_hp2, c.Q_cv, cs.INSTALLATIONID, d.objectid, d.property_dimensionsofthehouse
    FROM DWH.DEV_SICHEN.CIC_MORETHANONEYEAR AS c
    JOIN DWH.STG.STG_QUATT_CLOUD_CIC_STATES AS cs
        ON c.CLIENTID = cs.CICID
    JOIN DWH.STG.STG_QUATT_CLOUD_INSTALLATIONS AS i
        ON cs.INSTALLATIONID = i.ID
        AND i.HUBSPOTDEALID IS NOT NULL
        AND i.status = 'active'
    JOIN HUBSPOT_DATA_SHARE.V2_LIVE.objects_deals AS d
        ON i.HUBSPOTDEALID = d.objectid
    WHERE d.property_dimensionsofthehouse IS NOT NULL
        AND LOWER(d.property_dimensionsofthehouse) != 'nan'
    '''

