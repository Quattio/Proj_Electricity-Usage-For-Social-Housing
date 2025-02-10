import os
from dotenv import load_dotenv

desktop_path = os.path.join(os.path.expanduser("~"), ".snowflake")
load_dotenv(desktop_path)

snowflake_user     = os.getenv("SNOWFLAKE_USER") 
snowflake_password = os.getenv("SNOWFLAKE_PASSWORD")













