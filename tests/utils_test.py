from utils.gaode_utils import GaoDe
import logging
import yaml

def test_env():
    from utils.env_utils import env_conf
    print(env_conf)
    with open('conf/env.dev.yaml') as file:
        env_conf = yaml.safe_load(file)
        print(env_conf)


def test_logger():
    from utils.logger_utils import get_logger
    logger = get_logger()
    logger.error("test")
    logger = get_logger()
    logger.error("test2")