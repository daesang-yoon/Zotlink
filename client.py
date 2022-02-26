from ast import excepthandler
import asyncio
import websockets

first = True
loaded_messages = []

async def hello():
    async with websockets.connect('ws://localhost:5005') as websocket:
        global first
        while True:
            name = None
            if first:
                name = input("What's your name: ")
                first = False
            else:
                name = input("Send a message: ")
            await websocket.send(name)
            print("> {}".format(name))
            
        # while True:

        #     while len(loaded_messages)>0:
        #         print("sent message: " + loaded_messages[0])
        #         await websocket.send(loaded_messages[0])
            
            msg = await websocket.recv()
            print("< {}".format(msg))

            

def get_text(msg):
    loaded_messages.append(msg)


asyncio.get_event_loop().run_until_complete(hello())