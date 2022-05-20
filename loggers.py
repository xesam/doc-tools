import logging
import sys

logging.basicConfig(filename='app.log',
                    format='%(levelname) s%(asctime)s %(message)s',
                    level=logging.NOTSET,
                    encoding='utf-8')
logger = logging.getLogger('std')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
