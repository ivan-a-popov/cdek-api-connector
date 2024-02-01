"""Модуль логирования
Change file_handler.setLevel from ERROR to DEBUG when tracing issues
"""
import logging
import sys


# create logger
log = logging.getLogger('delivery_connector')
log.setLevel(logging.INFO)

# create file handler which logs even debug messages (set to 'error' when ran in production)
file_handler = logging.FileHandler('logs/test.log')
file_handler.setLevel(logging.INFO)

# create console handler with a higher log level
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# add the handlers to the logger
log.addHandler(file_handler)
log.addHandler(console_handler)
