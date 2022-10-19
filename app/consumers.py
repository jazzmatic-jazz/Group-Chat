import json
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from .models import Group, Chat
from app.models import Chat, Group
from channels.db import database_sync_to_async


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        # print('websocket Connected', event)
        
        # to see the channel layer, it gets the default channel layer of the app
        # print('Channel Layer:', self.channel_layer)

        # to see the channel name of the app
        # print('Channel Name:', self.channel_name)

        # ---Dynamic---------------------
        # print("Group name:",self.scope['url_route']['kwargs']['group_name']) #new

        self.groupname = self.scope['url_route']['kwargs']['group_name'] #new
        # print("Group Name:", self.groupname)

    # add a channel to new and existing group
# This perform the async task so as it is a sync so we need to convert it to sync
        async_to_sync(self.channel_layer.group_add)(
            # 'buddies', #static
            self.groupname, #dynamic #new
            self.channel_name 
        )

        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        # print('Message received from client', event)
        # print('Type:', type(event['text']))
        # To find the user
        print(self.scope['user'])
        self.groupname = self.scope['url_route']['kwargs']['group_name'] #new

        data = json.loads(event['text']) 
        print("data:", data)
        print('Chat:', data['msg'])
        
        # finding group object   
        group = Group.objects.get(name=self.groupname)
        if self.scope['user'].is_authenticated:

            # create new chat object
            chat = Chat(content= data['msg'], group=group)
            chat.save()

            # to show the user
            data['user'] = self.scope['user'].username
            print('Complete Data:', data)
            print('type of Complete Data', type(data))

            async_to_sync(self.channel_layer.group_send)(
                # 'buddies', #static
                self.groupname, #dynamic
            {
                'type': 'chat.message', #it is an event
                # 'message': event['text']
                'message': json.dumps(data)
            })
        
        else:
            self.send(
                {
                    'type': 'websocket.send',
                    # it will turn string to dict and will be sent to the client
                    'text': json.dumps({
                        'msg': 'LoginRequired', 
                        "user": "Guest"
                    })
                }
            )

        # to send the message to the client to make it available on the text area
        # creating an event handler for type
    def chat_message(self, event):
        # print('Event is', event)
        # print('Data:', event['message'])

        # server to client
        self.send({
            'type': 'websocket.send',
            'text': event['message']

        })

    def websocket_disconnect(self, event):
        print('websocket disconnected..', event)
        print('Channel Layer:', self.channel_layer)
        print('Channel Name:', self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(
            # 'buddies',
            self.groupname,
            self.channel_name)
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # print('websocket Connected', event)
        
        # to see the channel layer, it gets the default channel layer of the app
        # print('Channel Layer:', self.channel_layer)

        # to see the channel name of the app
        print('Channel Name:', self.channel_name)
        self.groupname = self.scope['url_route']['kwargs']['group_name'] #new
        print("Group Name:", self.groupname)


    # add a channel to new and existing group
# This perform the async task so as it is a sync so we need to convert it to sync
        await self.channel_layer.group_add(
            # 'buddies', 
            self.groupname,
            self.channel_name # static group name
        )

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('Message received from client', event)
        print('Text:', event['text'])
        print('Type:', type(event['text']))
        # self.groupname = self.scope['url_route']['kwargs']['group_name'] #new

        data = json.loads(event['text']) 
        print("data:", data)
        print('Chat:', data['msg'])
        
        # finding group object   
        group = await database_sync_to_async( Group.objects.get)(name=self.groupname)

        if self.scope['user'].is_authenticated:

        # create new chat object
            chat = Chat(content= data['msg'], group=group)
            await database_sync_to_async(chat.save)()

            data['user'] = self.scope['user'].username
            print('Complete Data:', data)
            print('type of Complete Data', type(data))
            
            await self.channel_layer.group_send(
                # 'buddies', #static group name
                self.groupname,
            {
                'type': 'chat.message', #it is an event
                'message': json.dumps(data)
            })

        else:
            await self.send(
                {
                    'type': 'websocket.send',
                    # it will turn string to dict and will be sent to the client
                    'text': json.dumps({'msg': 'LoginRequired', "user": "Guest"})
                }
            )

        # to send the message to the client to make it available on the text area
        # creating an event handler for type
    async def chat_message(self, event):
        print('Event is', event)
        print('Data:', event['message'])

        # server to client
        await self.send({
            'type': 'websocket.send',
            'text': event['message']

        })

    async def websocket_disconnect(self, event):
        print('websocket disconnected..', event)
        print('Channel Layer:', self.channel_layer)
        print('Channel Name:', self.channel_name)
        await self.channel_layer.group_discard(
            # 'buddies', 
            self.groupname,
            self.channel_name)
        raise StopConsumer()