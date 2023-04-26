import os
root_dir = os.path.dirname(os.path.dirname(__file__))

import logging

logger = None

def init_logger(name=__name__, file_name="error", file_level=logging.ERROR, console_level=logging.DEBUG):
    # 创建一个 logger 实例
    global logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 创建一个控制台 handler 并设置其级别为 DEBUG
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)

    # 创建一个文件 handler，并设置其级别为 ERROR
    file_handler = logging.FileHandler(f'{root_dir}/logs/{file_name}.log')
    file_handler.setLevel(file_level)

    # 将 handler 添加到 logger 中
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def get_logger():
    if logger is None:
        init_logger() # 默认logger
    return logger

