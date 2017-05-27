#Click Game Server

import asyncio, websockets, json
from oauth2client import client, crypt

class Player:
    def __init__(self, userid, data):
        self.userid = userid
        self.clicks = data['clicks']

class Client:
    def __init__(self, ws, path):
        self.ws = ws
        self.path = path

    async def listen(self):
        try:
            while self.ws.open:
                #Process data from server to usable format
                data = await self.ws.recv()
                data = json.loads(data)
                key = list(data.keys())[0]
                data = data[key]

                #Call appropriate method
                method = getattr(self, key)
                execute = asyncio.ensure_future(method(data))

                try:
                    server.users[self.player.userid] = {
                        'clicks': self.player.clicks
                    }
                except:
                    pass

        except:
            pass

        finally:
            print(self.player.userid, "disconnected")
            self.ws.close()

            with open('users.json', 'w') as f:
                user = json.dump({
                    self.player.userid: {
                        'clicks': self.player.clicks
                    }
                }, f)
                f.close()

    async def login(self, data):
        try:
            idinfo = client.verify_id_token(data, None)

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")

            userid = idinfo['sub']

            print(userid, "connected")

            if userid not in server.users:
                #Creation of user in users.json
                server.users[userid] = {'clicks': 0}

                with open('users.json', 'w') as f:
                    json.dump(server.users, f)
                    f.close()

            with open('users.json') as file_users:
                server.users = json.load(file_users)
                file_users.close()

            print(server.users)

            self.player = Player(userid, server.users[userid])

            print(server.users, "DONE")

            await self.ws.send(json.dumps({'auth': True}))
            await self.ws.send(json.dumps(self.player, default = lambda o: o.__dict__))

        except crypt.AppIdentityError:
            print("failed to log-in")
            await self.ws.send(json.dumps({'auth': False}))

    async def click(self, data):
        print(self.player.userid, "clicked")
        self.player.clicks += 1
        await self.ws.send(json.dumps(self.player, default = lambda o: o.__dict__))


    """
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
        """

class Server(websockets.server.WebSocketServerProtocol):
    def __init__(self):
        with open('users.json') as file_users:
            self.users = json.load(file_users)
            file_users.close()

        print(self.users)

    async def handler(self, ws, path):
        client = Client(ws, path)
        listener = asyncio.ensure_future(client.listen())
        await asyncio.wait([listener])
        del client

    def run(self, host='192.168.1.9', port=25565):
        start_server = websockets.serve(self.handler, host, port)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    server = Server()
    server.run()
