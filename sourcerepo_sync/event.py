import base64
import json


class IrrelevantEvent(Exception):
    pass


class Event:
    def __init__(self, event):
        decoded = base64.b64decode(event['data']).decode('utf-8')
        self.data = json.loads(decoded)


    @property
    def owner(self):
        return self._full_name.split('/')[0]


    @property
    def repo(self):
        return self._full_name.split('/')[1]


    @property
    def clone_url(self):
        return self._repository['clone_url']


    @property
    def _repository(self):
        return self.data['repository']


    @property
    def _full_name(self):
        return self._repository['full_name']
