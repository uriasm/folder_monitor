# -*- coding: utf-8 -*-
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from app.firebase import Firebase
from app.event import Event
import websocket
import time


class Monitor:
    """
    Class in charge of monitoring the changes made in a specific folder
    """

    def __init__(self, path):
        self.path = path
        self.observer = False
        self.firebase_service = Firebase()
        self.event_handler = self.__set_event_handler()

    def __set_event_handler(self) -> PatternMatchingEventHandler:
        """
        Create the event handler to notify when something happens in the
        filesystem
        """
        patterns = ["*"]
        ignore_patterns = None
        event_handler = PatternMatchingEventHandler(
            patterns=patterns, ignore_patterns=ignore_patterns,
            ignore_directories=False, case_sensitive=True)
        event_handler.on_created = self.on_created
        event_handler.on_deleted = self.on_deleted
        event_handler.on_modified = self.on_modified
        event_handler.on_moved = self.on_moved
        return event_handler

    def start_observer(self):
        """
        Create and initialize the observer
        """
        print('==> Starting Watchdog observer')
        self.observer = Observer()
        self.observer.schedule(
            self.event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            self.observer.join()

    def on_created(self, event):
        """
        On create event in file system
        """
        print(f"==> MONITOR: {event.src_path} has been created!")
        event_object = Event(event)
        key = self.firebase_service.push_data(data=event_object.__dict__)
        self.send_event(key=key)

    def on_deleted(self, event):
        """
        On deleted event in file system
        """
        print(f"==> MONITOR: {event.src_path} has been deleted!")
        event_object = Event(event)
        key = self.firebase_service.push_data(data=event_object.__dict__)
        self.send_event(key=key)

    def on_modified(self, event):
        """
        On modified event in file system
        """
        print(f"==> MONITOR: {event.src_path} has been modified!")
        event_object = Event(event)
        key = self.firebase_service.push_data(data=event_object.__dict__)
        self.send_event(key=key)

    def on_moved(self, event):
        """
        On moved event in file system
        """
        print(f'==> MONITOR: {event.src_path} has been moved to '
              f'{event.dest_path}!')
        event_object = Event(event)
        key = self.firebase_service.push_data(data=event_object.__dict__)
        self.send_event(key=key)

    @staticmethod
    def send_event(key: str):
        """
        Function that sends messages to the socket server
        """
        print('==> MONITOR: Sending data to websocket serve')
        ws = websocket.WebSocket()
        ws.connect("ws://localhost:8000")
        ws.send(key)
        ws.close()
