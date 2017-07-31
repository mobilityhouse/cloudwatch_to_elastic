from elasticsearch import Elasticsearch

import base64
import datetime
import gzip
import json
import logging
import time

from .config import ELASTIC_URL, ELASTIC_INDEX

es_host = ELASTIC_URL
es_port = 9200

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    # unzip the CloudWatch log data
    logger.info(event)
    parsed_event = json.loads(gzip.decompress(base64.b64decode(event['awslogs']['data'])))

    es = Elasticsearch(host=es_host, port=es_port)

    logger.info(parsed_event)

    try:
        real_message = json.loads(parsed_event['logEvents'][0]['message'])
        logger.info("Converted message")
        logger.info(real_message)
    except KeyError:
        pass

    res = False

    for i in range(20):
        try:
            res = es.index(index=ELASTIC_INDEX, doc_type='logs', body=real_message)
            return res
        except Exception as E:
            logger.info(E)
            time.sleep(0.5)
        return res

    return ('nothing to process')
