import os
import dotenv

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_SAMPLE_RATE = os.getenv("SENTRY_SAMPLE_RATE")
SENTRY_ENV = os.getenv("SENTRY_ENV")
