from elasticsearch import Elasticsearch

import base64
import gzip
import json
import logging
import time


from config import ELASTIC_URL, ELASTIC_INDEX
try:
    import custom_filter
except ImportError:
    custom_filter = None

es_host = ELASTIC_URL
es_port = 9200

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    # unzip the CloudWatch log data
    logger.info(event)
    parsed_event = json.loads(gzip.decompress(base64.b64decode(event['awslogs']['data'])))  # noqa

    es = Elasticsearch(host=es_host, port=es_port)

    logger.info(parsed_event)

    for message in parsed_event['logEvents']:
        try:
            real_message = message['message']
            logger.info("Converted message:" + str(real_message))
        except KeyError:
            return ('nothing to process')

        if custom_filter:
            real_message = custom_filter.run(real_message, logger)

        for i in range(20):
            try:
                logger.info(real_message)
                res = es.index(index=ELASTIC_INDEX, doc_type='logs', body=real_message)  # noqa
                logger.info(res)
            except Exception as E:
                logger.info("Failed for the {}".format(i))
                time.sleep(0.5)

    return ('nothing to process')
