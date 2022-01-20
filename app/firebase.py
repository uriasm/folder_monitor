# -*- coding: utf-8 -*-
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class Firebase:
    """
    Class that is responsible for establishing connections to Firebase
    """
    def __init__(self):
        self.db_url = 'https://observer-9ab26-default-rtdb.firebaseio.com/'
        self.__start_firebase()
        self.ref = db.reference("/events")

    def __start_firebase(self):
        """
        Initialize the Firebase app
        """
        if not firebase_admin._apps:
            credential_object = credentials.Certificate(
                'src/firebase/observer-9ab26-firebase-adminsdk.json')
            firebase_admin.initialize_app(credential_object, {
                'databaseURL': self.db_url
            })

    def push_data(self, data: dict) -> str:
        """
         Save event information
        """
        response = self.ref.push(data)
        return response.key

    def get_data(self, key: str) -> dict:
        """
        Get event information by key
        """
        result = self.ref.order_by_key().equal_to(key).limit_to_first(1).get()
        result = result.popitem()
        return result[1]
