import os
import dotenv

dotenv.load_dotenv()

SQLITE_PATH    = "./sqlite.db"
FOLDER_ID      = os.environ["FOLDER_ID"]
YA_GPT_API_KEY = os.environ["YA_GPT_KEY_API"]