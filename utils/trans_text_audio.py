from utils.logger_utils import get_logger
logger = get_logger()

import subprocess
def edge_tts(text, voice_pth):
    """
    调用edge-tts生成mp3
    """
    process = subprocess.Popen(['edge-tts', '--text', text, '--write-media', voice_pth],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    logger.debug(f'stdout: {stdout.decode()}')
    logger.debug(f'stderr: {stderr.decode()}')
    logger.debug(f'exit code: {process.returncode}')
