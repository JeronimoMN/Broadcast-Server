import asyncio
from pyexpat.errors import messages

import websockets

class BroadcastClient:
    def __init__(self, name):
        self.name = name
        self.uri = 'ws://localhost:8765'
        self.ws = None


    async def chat(self):
        async with websockets.connect(self.uri) as self.ws:
            while True:
                message = input("Enter Message: ")
                await self.ws.send(message)
                rs = await self.ws.recv()
                print(f"Received: {rs}")


    async def connect_server(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                self.ws = websocket

                print('Connected to server')
                await websocket.send("Hello, world!")
                greeting = await websocket.recv()
                print(greeting)

        except websockets.exceptions.ConnectionClosedError as e:
            print(e)


    async def disconnect_server(self):
        try:
            await self.ws.close(1000, 'Good')
            print('Disconnected from server')
        except Exception as e:
            print(e)



if __name__ == '__main__':
    client = BroadcastClient('clientPP')
    asyncio.run(client.chat())
    #asyncio.run(client.disconnect_server())