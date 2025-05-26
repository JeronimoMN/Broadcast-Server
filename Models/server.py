import asyncio
import websockets
from websockets import broadcast

class BroadcastServer:
    def __init__(self):
        self.clients = set()
        self.server = None

    #STATIC CONFIGURATION
    CONFIG = {
        'host': 'localhost',
        'port' : 8765,
    }

    async def broadcast(self, websocket):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                for client in self.clients:
                    if client != websocket:
                        await client.send(message)
        except websockets.exceptions.ConnectionClosed as e:
            print('Client disconnected', e)
        finally:
            self.clients.remove(websocket)


    async def start_server(self):
        try:
            self.server = await websockets.serve(self.broadcast, self.CONFIG['host'], self.CONFIG['port'] )
            print("Server started")
            await asyncio.Future() #Run Forever. Always listening
        except websockets.exceptions.ConnectionClosedError:
            print("Server closed")

    async def closed_server(self):
        try:
            await self.server
            self.server = None
            print('Prueba')

        except Exception as e:
            print(e)


async def main():
    server = BroadcastServer()
    await server.start_server()


if __name__ == "__main__":
    asyncio.run(main())