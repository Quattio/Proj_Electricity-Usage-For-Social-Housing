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

def ElectricityUsage_over_year():
    return f'''
    WITH EligibleClients AS (
            SELECT 
                clientid, 
                min(time_ts) AS first_record_time
            FROM cic_stats
            GROUP BY clientid
            HAVING first_record_time BETWEEN '2022-11-01 00:00:00' AND '2024-02-10 00:00:00'
        )
    SELECT  
            clientid,
            ((MAX(hp1_electricalEnergyCounter) - MIN(hp1_electricalEnergyCounter)) + ifNull(MAX(hp2_electricalEnergyCounter) - MIN(hp2_electricalEnergyCounter), 0)) / 1000 AS electricity_usage
    FROM 
            cic_stats s
    JOIN EligibleClients c ON s.clientid = c.clientid
    WHERE
            time_ts BETWEEN '2024-10-01 00:00:00' AND '2025-02-20 00:00:00'
            AND system_ccNumberOfHeatPumps=1  -- Hybrid or DUO
    GROUP BY
            s.clientid
    '''

def data_during_day():
    return f'''
    SELECT 
        interval_time,
        COUNT(DISTINCT clientid) as activeCIC,
        SUM(gas_usage) / COUNT(DISTINCT clientid) AS avg_gas_usage,
        SUM(co2_emission) / COUNT(DISTINCT clientid) AS avg_co2_emission,
        SUM(electricity_usage) / COUNT(DISTINCT clientid) AS avg_electricity_usage
    FROM (
        SELECT 
            toStartOfInterval(time_ts, INTERVAL 10 minute) AS interval_time,  
            clientid,
            (MAX(qc_cvEnergyCounter) - MIN(qc_cvEnergyCounter)) / 1000 / 8.8 AS gas_usage,  
            (MAX(qc_cvEnergyCounter) - MIN(qc_cvEnergyCounter)) / 1000 / 8.8 * 1.788 + ((MAX(hp1_electricalEnergyCounter) - MIN(hp1_electricalEnergyCounter)) + ifNull(MAX(hp2_electricalEnergyCounter) - MIN(hp2_electricalEnergyCounter), 0)) * 0.272 / 1000 AS co2_emission,
            ((MAX(hp1_electricalEnergyCounter) - MIN(hp1_electricalEnergyCounter)) + ifNull(MAX(hp2_electricalEnergyCounter) - MIN(hp2_electricalEnergyCounter), 0)) / 1000 AS electricity_usage
        FROM cic_stats
        WHERE 
            time_ts BETWEEN toDateTime('2023-10-01 00:00:00') 
                       AND toDateTime('2024-03-31 23:59:59')
            -- And clientid LIKE 'CIC-1%' OR clientid LIKE 'CIC-2%'
            And clientid LIKE 'CIC-1%' 
            -- AND substring(clientid, 5, 2) BETWEEN '11' AND '1A' 
            AND system_ccNumberOfHeatPumps=1  -- Hybrid or DUO
        GROUP BY clientid, interval_time  
    ) AS per_client_usage
    GROUP BY interval_time
    ORDER BY interval_time;
    '''
