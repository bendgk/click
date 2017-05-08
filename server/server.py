import asyncio
import websockets

users = set()

class Client:
    def __init__(self, ws, path):
        self.ws = ws
        self.ra = ws.remote_address
        self.path = path
        self.clicks = 0

    async def register(self):
        server.users.add(self.ws)
        print(self.ra, "joined")

        try:
            await asyncio.wait([ws.send(str(len(server.users))) for ws in server.users])

            while self.ws.open:
                await asyncio.sleep(0.01)

        except Exception as e:
            print(e)

        finally:
            print(self.ra, "left")
            server.users.remove(self.ws)
            try:
                await asyncio.wait([ws.send(str(len(server.users))) for ws in server.users])

            except Exception as e:
                print(e)
                print("NO USERS ON SERVER")

    async def click(self):
        try:
            while True:
                resp = await self.ws.recv()
                if resp == "click":
                    print(self.ra, "clicked")
                    self.clicks += 1

                    await self.ws.send(str(self.clicks))
                    print("sent response")

        except Exception as e:
            pass

class Server(websockets.server.WebSocketServerProtocol):
    def __init__(self):
        self.users = set()

    async def handler(self, ws, path):
        client = Client(ws, path)
        register = asyncio.ensure_future(client.register())
        click = asyncio.ensure_future(client.click())

        await asyncio.wait([register, click])

    def run(self, host='192.168.1.9', port=25565):
        start_server = websockets.serve(self.handler, host, port)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    server = Server()
    server.run()
