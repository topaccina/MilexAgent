import os
from dotenv import load_dotenv


# support functions to manage the env and retrieve video details and eval token counts
def getEnvVar():

    load_dotenv(override=True)
    API_KEY = os.environ.get("OPENAI_API_KEY")
    return API_KEY
