import sentry_sdk
from sentry_sdk.integrations.asyncio import AsyncioIntegration


from src.config import SENTRY_DSN, SENTRY_SAMPLE_RATE, SENTRY_ENV


def init_sentry():
    if SENTRY_DSN is not None and SENTRY_ENV != "local":
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            traces_sample_rate=SENTRY_SAMPLE_RATE,
            profiles_sample_rate=SENTRY_SAMPLE_RATE,
            integrations=[AsyncioIntegration(), AioHttpIntegration()],
            environment=SENTRY_ENV
    )
