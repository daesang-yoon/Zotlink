import asyncio
import websockets
import json


class_dict = {}


async def filter_or_create(websocket):
    async for messages in websocket:
        key = messages[:6]
        messages = messages[9:].split(';;;')
        object_list = []
        if key == 'FILTER':
            print(messages)
            if len(messages) == 1:
                for keys, values in class_dict.items():
                    if messages[0] == keys:
                        for num, lists in class_dict[messages[0]].items():
                            # print(lists)
                            for posts in lists:
                                # print(f"FILTER> {messages[0] + ';;;' + num + ';;;' + posts}")
                                # await websocket.send(messages[0] + ';;;' + num + ';;;' + posts)
                                object_list.append({'school': messages[0], 'course_code': num, 'post': posts})
                            # break
                await websocket.send(json.dumps(object_list))

            elif len(messages) == 2:
                for keys, values in class_dict.items():
                    if messages[0] == keys:
                        for classes, posts in values.items():
                            if classes == messages[1]:
                                for post in posts:
                                    # print(f"> {messages[0]+ ';;;' + messages[1] + ';;;' + post}")
                                    # await websocket.send(messages[0]+ ';;;' + messages[1] + ';;;' + post)
                                    object_list.append({'school': messages[0], 'course_code': classes, 'post': posts})
                
                await websocket.send(json.dumps(object_list))

            await websocket.send('BREAK')

        elif key == 'CREATE':
            post = []
            if messages[0] in class_dict.keys():
                if messages[1] in class_dict[messages[0]].keys():
                    class_dict[messages[0]][messages[1]].append(messages[2])
                    print(f'CREATED> {class_dict}')
                    
                else:
                    class_dict[messages[0]][messages[1]] = [messages[2]]
                    print(f'CREATED> {class_dict[messages[0]][messages[1]]}')
                    
            else:
                class_dict[messages[0]] = {messages[1]: [messages[2]]}
                print(f'CREATED> {class_dict[messages[0]]}')
                
            for school, values in class_dict.items():
                # print(school)
                for classes, lists in values.items():
                    # print(classes)
                    for posts in lists:
                        # print(f"SENT> {school + ';;;' + classes + ';;;' + posts}")
                        # await websocket.send(school + ';;;' + classes + ';;;' + posts)
                        post.append({'school': school, 'course_code': classes, 'post': posts})

            await websocket.send(json.dumps(post))
            await websocket.send('BREAK')

        # else:
        #     for school, values in class_dict.items():
        #         print(school)
        #         for classes, lists in values.items():
        #             print(classes)
        #             for posts in lists:
        #                 print(f"SENT> {school + ';;;' + classes + ';;;' + posts}")
        #                 await websocket.send(school + ';;;' + classes + ';;;' + posts)
            
        #     await websocket.send('BREAK')


async def main():
    async with websockets.serve(filter_or_create, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
