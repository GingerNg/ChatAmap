import pynng
import curio
address = "ipc:///tmp/pipeline.ipc"
class Sender(object):
    def __init__(self) -> None:
        pass

    @staticmethod
    def ping():
        try:
            with pynng.Push0() as sock:
                sock.dial(address, block=True)
            return True
        except Exception as e:
            return False

    @staticmethod
    async def send(message: str):
        with pynng.Push0() as sock:
            sock.dial(address)
            print(f'NODE1: SENDING "{message}"')
            await sock.asend(message.encode())
            # await curio.sleep(1)  # wait for messages to flush before shutting down

