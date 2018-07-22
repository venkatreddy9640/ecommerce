import logging

def get_logger(filename):
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)
	handler = logging.FileHandler(filename)
	handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	return logger


