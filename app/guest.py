# -*- coding: utf-8 -*-
from dataclasses import dataclass
from app.firebase import Firebase
import websockets
import asyncio
import json


@dataclass
class Guest:
    """
    Class containing the socket server to receive messages from the file
    monitor and write the metadata to a json file.
    """
    def __init__(self):
        self.firebase_service = Firebase()
        self.json_path = 'src/events.json'

    async def handler(self, websocket, path):
        """
        Asynchronous function in charge of receiving client messages
        through sockets
        """
        print('==> GUEST: Receiving data on websockets server')
        data = await websocket.recv()
        event_data = self.get_event_data(key=data)
        self.write_event(event=event_data, key=data)

    def start_server(self):
        """
        Initialize the socket server
        """
        print('==> Starting websocket serve')
        start_server = websockets.serve(self.handler, "localhost", 8000)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def get_event_data(self, key: str) -> dict:
        """
        Once the message is received from the socket client, this function
        takes care of taking the key and getting the event from Firebase
        """
        return self.firebase_service.get_data(key)

    def write_event(self, event: dict, key: str):
        """
        Write the event that has been obtained from Firebase in a json file
        """
        print('==> GUEST: Writing json file')
        try:
            with open(self.json_path, 'r') as fp:
                events = json.load(fp)
        except IOError:
            print('==> Json file not found, creating a new one.')
            events = {}

        events[key] = event
        with open(self.json_path, 'w') as fp:
            json.dump(events, fp, indent=4)
