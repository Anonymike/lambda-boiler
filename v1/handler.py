import os
import base64
import json

# These modules are usually pip installed from git
from src.modules.custom_logger import logger
from src.modules.secrets import SecretManager
from src.modules.custom_redis import RedisConnection
from src.event_processor.event_processor import HomeFeedEvent

# Global initializations
ENV = os.environ['STAGE']
SECRET_MANAGER = SecretManager(os.environ['SECRET_ENDPOINT'],
                               os.environ['REGION_NAME'])
# Redis Cache Connection
REDIS_CREDS = SECRET_MANAGER.get_secret(os.environ['CACHE_SECRET'])
REDIS_CON = RedisConnection(REDIS_CREDS.get('url'),
                            REDIS_CREDS.get('port'))

GLOBALS = {
    'LOGGER': logger,
    'ENV': ENV,
    'REDIS_CON': REDIS_CON}


def handler(event, context):
    # Process api gateway event
    # Check auth, query params etc

    try:
        HomeFeedEvent(**GLOBALS).process_event(event)
    except Exception as e:
        logger.error('Error processing event.',
                      extra={'event': event,
                             'e': e})