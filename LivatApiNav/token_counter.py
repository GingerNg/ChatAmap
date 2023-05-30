import pynng
import curio
import asyncio
address = "ipc:///tmp/pipeline.ipc"


async def node0(sock):
    async def recv_eternally():
        while True:
            msg = await sock.arecv_msg()
            content = msg.bytes.decode()
            print(f'NODE0: RECEIVED "{content}"')

    sock.listen(address)
    return await curio.spawn(recv_eternally)

async def main():
    with pynng.Pull0() as pull:
        await node0(pull)
        while True:
            await curio.sleep(1)

if __name__ == "__main__":
    try:
        curio.run(main)
    except KeyboardInterrupt:
        # that's the way the program *should* end
        pass