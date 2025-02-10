import os
from dotenv import load_dotenv

desktop_path = os.path.join(os.path.expanduser("~"), ".redis")
load_dotenv(desktop_path)
redis_host     = os.getenv("REDIS_HOST")
redis_port     = os.getenv("REDIS_PORT")
redis_db       = os.getenv("REDIS_DB")
redis_passport = os.getenv("REDIS_PASSPORT")
redis_username = os.getenv("REDIS_USERNAME")





