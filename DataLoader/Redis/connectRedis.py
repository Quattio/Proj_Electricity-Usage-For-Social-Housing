from .loadRedisCredentials import redis_host, redis_port, redis_db, redis_passport, redis_username
import redis
import os
import pandas as pd
from dotenv import load_dotenv
import json

def connect_redis(arguments):

    try:
        # Credentials
        desktop_path = os.path.join(os.path.expanduser("~"), ".redis")
        load_dotenv(desktop_path)

        # Connect to Redis database
        r = redis.Redis(host=os.getenv("REDIS_HOST"),
                        port=os.getenv("REDIS_PORT"),
                        db  =os.getenv("REDIS_DB"),
                        password=os.getenv("REDIS_PASSPORT"),
                        username=os.getenv("REDIS_USERNAME"))

        # get objects from redis
        redis_objects = r.mget(r.keys(pattern="cic:*CIC*lastStat*"))
        results = []
        for obj, key in zip(redis_objects, r.keys(pattern="cic:*CIC*lastStat*")):
            try:
                data = json.loads(obj.decode())
                data['cic'] = key.decode().split(':')[1]
                results.append(data)
            except:
                pass
        df_redis = pd.json_normalize(results)

        return df_redis

    except Error as e:
        print("connect_redis error out.")



