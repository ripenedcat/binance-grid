import logging

class Logger():
    def __init__(self):
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        #logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
        self.logger = logging.getLogger()
    def get(self):
        return self.logger