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


def CiCdata_MoreThanOneYear():
    return f'''
    WITH EligibleClients AS (
        SELECT 
            clientid, 
            min(time_ts) AS first_record_time
        FROM "cic_stats"
        GROUP BY clientid
        HAVING first_record_time BETWEEN '2022-11-01 00:00:00' AND '2024-02-10 00:00:00'
    )
    SELECT  
        clientid,
        max(hp1_electricalEnergyCounter) - min(hp1_electricalEnergyCounter) AS E_hp1,
        ifNull(max(hp2_electricalEnergyCounter) - min(hp2_electricalEnergyCounter), 0) AS E_hp2,
        max(qc_cvEnergyCounter) - min(qc_cvEnergyCounter) AS Q_cv
    FROM 
        "cic_stats" s
    JOIN EligibleClients c ON s.clientid = c.clientid
    WHERE
        time_ts BETWEEN '2024-02-10 00:00:00' AND '2025-02-10 23:59:59'
    GROUP BY
        s.clientid
    HAVING 
        E_hp1 > 0 AND Q_cv > 0;
    '''



