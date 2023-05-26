import pynng
import curio

address = "ipc:///tmp/pipeline.ipc"

# receiver
async def node0(sock):
    async def recv_eternally():
        while True:
            msg = await sock.arecv_msg()
            content = msg.bytes.decode()
            print(f'NODE0: RECEIVED "{content}"')

    sock.listen(address)
    return await curio.spawn(recv_eternally)


# sender
async def node1(message):
    with pynng.Push0() as sock:
        print(sock.dial(address))
        print(f'NODE1: SENDING "{message}"')
        await sock.asend(message.encode())
        await sock.asend(message.encode())
        await curio.sleep(1)  # wait for messages to flush before shutting down


async def main():
    with pynng.Pull0() as pull:

        n0 = await node0(pull)
        await curio.sleep(1)

        await node1("Hello, World!")
        await node1("Goodbye.")

        # another way to send
        async with curio.TaskGroup(wait=all) as g:
            for msg in ["A", "B", "C", "D"]:
                await g.spawn(node1, msg)

        await n0.cancel()

async def main_send():
    await node1("Hello, World!")
    await node1("Goodbye.")

    # another way to send
    async with curio.TaskGroup(wait=all) as g:
        for msg in ["A", "B", "C", "D"]:
            await g.spawn(node1, msg)


if __name__ == "__main__":
    try:
        curio.run(main_send)
    except KeyboardInterrupt:
        # that's the way the program *should* end
        pass