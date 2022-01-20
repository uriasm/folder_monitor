# -*- coding: utf-8 -*-
from watchdog.events import FileSystemEvent
from dataclasses import dataclass
from datetime import datetime
import os


@dataclass
class Event:
    """
    Class that contains the attributes of the events that will be sent
    to Firebase
    """
    name: str
    is_file: int
    updated: str
    created: str
    path: str
    r_path: str
    event_type: str
    operation: dict

    def __init__(self, event: FileSystemEvent):
        self.name = os.path.basename(event.src_path)
        self.is_file = 0 if event.is_directory else 1
        self.updated = str(datetime.utcnow())
        self.created = str(datetime.utcnow())
        self.path = os.path.abspath(event.src_path)
        self.r_path = event.src_path
        self.event_type = event.event_type
        self.operation = {'detail': self.__get_details(event)}

    def __get_details(self, event: FileSystemEvent) -> str:
        """
        Function that obtains the details of the event, it varies according
        to the type of event.
        """
        details = f'{self.name} has been {self.event_type}!'
        if self.event_type == 'moved':
            details = f'{self.name} has been {self.event_type} to ' \
                      f'{event.dest_path}!'
        return details
