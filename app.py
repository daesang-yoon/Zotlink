import asyncio
import websockets

connected = dict()

async def server(websocket, path):
    # Register.

    #connected.add(websocket)
    #print(connected)
    
    try:
        async for message in websocket:
            if not websocket in connected:
                connected[websocket] = message
            #print('asdfasdfasdfasdfasdf')
            #for conn in connected:
                #if conn != websocket:
                #await conn.send(message)
            websockets.broadcast(set(connected.keys()), f'Got a new MSG FOR YOU from {connected[websocket]}: {message}')
            #await websocket.wait_closed()
    finally:
        # Unregister.
        del connected[websocket]
    

start_server = websockets.serve(server, "localhost", 5005)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()