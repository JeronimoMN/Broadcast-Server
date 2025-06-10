import asyncio
import json
import time
import websockets
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout


class BroadcastClient:
    def __init__(self, name):
        self.name = name
        self.uri = 'ws://localhost:8765'
        self.session = PromptSession()

    #TODO: CONNECT VALIDATOR: It have to consult if the server is active or not. If is not active, close wit no error and give context


    async def send_message(self, ws):
        while True:
            with patch_stdout():
                msg = await self.session.prompt_async("Enter Message: ")
            if msg:
                await ws.send(msg)

    async def receive_message(self, ws):
        while True:
            try:
                rs = await ws.recv()
                print(f"\nReceived: {rs}")
            except websockets.exceptions.ConnectionClosedError as e:
                print("Connection Closed", e)
                break


    async def chat(self):
        try:
            async with websockets.connect(self.uri) as ws:
                #Execute Send and Receive in Parallel
                await asyncio.gather(
                    self.send_message(ws),
                    self.receive_message(ws)
                )

        except Exception as e:
            print("Error: ", e)
        """
        try:
            async with websockets.connect(self.uri) as ws:
                while True:
                    #Problem: The flow of the code is bloked by the msg Input. It has to be Asyncronymus
                    msg = input("Enter Message: ")
                    message = {
                        "msg": msg,
                        "info": {
                            "type": "message",
                            "author": self.name,
                            "time": time.time()
                        }
                    }
                    if msg is not None:
                        await ws.send(msg)
                    print(f"Received: {await ws.recv()}")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection Closed: {e}")

    async def disconnect_server(self):
        try:
            await self.ws.close(1000, 'Good')
            print('Disconnected from server')
        except Exception as e:
            print(e)
    """


if __name__ == '__main__':
    client = BroadcastClient('clientPP')
    asyncio.run(client.chat())
    #asyncio.run(client.disconnect_server())