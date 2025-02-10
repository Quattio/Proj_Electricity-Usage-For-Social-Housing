import snowflake.connector
from .loadSnowFlakeCredentials import snowflake_user, snowflake_password
from . import CommonQuery
import pandas as pd


def connect_snowflake(arguments):
    conn = None
    cur = None
    try:
        conn = snowflake.connector.connect(
            user=snowflake_user,
            password=snowflake_password,
            account='iejbhuk-quatt',
            database='FIREHOSE_CIC',  
            schema='CIC.STATS_DYNAMIC', 
            warehouse='COMPUTE_WH', 
            # role='your_role',          
            session_parameters={
                'QUERY_TAG': 'Snowflake_Example',
            }
        )

        cur = conn.cursor()
        
        if arguments.query is None:
            query, params = CommonQuery.query_define(
                arguments.extractVariables,
                arguments.table,
                arguments.clientid,
                arguments.startTime,
                arguments.endTime
            )
            # print("Generated query:", query)
            # print("Query parameters:", params)
            cur.execute(query, params)
        else:
            sql_query = getattr(CommonQuery, arguments.query)()
            # print("Generated query:", sql_query)
            cur.execute(sql_query)
        
        # Fetch results once and build DataFrame
        results = cur.fetchall()
        df = pd.DataFrame(results, columns=[desc[0] for desc in cur.description])
        
        #print("Rows returned:", len(df))
        return df

    except Exception as e:
        print("An exception occurred:", str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

