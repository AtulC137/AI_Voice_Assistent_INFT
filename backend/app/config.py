from dotenv import load_dotenv
import os

load_dotenv()

SARVAM_API_KEY = os.getenv(
    "SARVAM_API_KEY"
)

if not SARVAM_API_KEY:

    raise Exception(
        "SARVAM_API_KEY missing"
    )