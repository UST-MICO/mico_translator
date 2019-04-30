from re import compile
from json import loads, dumps
from json.decoder import JSONDecodeError
from base64 import b64decode, b64encode
from binascii import Error as Base64Error
from uuid import uuid1
from datetime import datetime, time
from typing import Any

MIMETYPE_JSON = compile(r'\w*/(\w+\+)?json')
BASE64_HEURISTIC = compile(r'^\w')


class CloudEvent():
    """
    Cloud event message object following spec 0.2.
    """

    def __init__(self, message: dict):
        if message:
            self.init_from_dict(message)

    def init_from_dict(self, message: dict):
        self.message = {
            'type': message['type'],
            'specversion': message['specversion'],
            'source': message['source'],
            'id': message['id'],
            'time': message.get('timestamp'),
            'schemaurl': message.get('schemaurl'),
            'contenttype': message.get('contenttype'),
            'data': message.get('data'),
        }
        if (self.specversion != '0.2'):
            Warning('This implementation only supports CloudEvents with spec version 0.2!')

        if self.data and isinstance(self.data, str):
            if self.contenttype and MIMETYPE_JSON.match(self.contenttype):
                if BASE64_HEURISTIC.match(self.data):
                    try:
                        self.data = b64decode(self.data, validate=True).decode()
                    except Base64Error:
                        pass
                try:
                    self.data = loads(self.data)
                except JSONDecodeError:
                    Warning('Data should be of type json but parsing failed!')

        for key in message:
            if key in ('type', 'specversion', 'source', 'id', 'timestamp', 'schemaurl', 'contenttype', 'data'):
                continue
            self.message[key] = message[key]

    def create_new_message(self) -> 'CloudEvent':
        """
        Create a new message as answer to this message copying most attributes.
        """
        new_event = CloudEvent(self.message)
        new_event.id = None
        new_event.time = None
        new_event['created_from'] = self.id
        return new_event

    def serialize_message(self) -> str:
        """
        Serialize the message and generate id and time if not set.
        """
        if not self.id:
            self.id = uuid1().hex
        if not self.time:
            self.time = datetime.now().isoformat()
        return dumps(self.message)

    @property
    def type(self) -> str:
        return self.message.get('type')

    @type.setter
    def type(self, type: str):
        self.message['type'] = type

    @property
    def specversion(self):
        return self.message.get('spectversion')

    @specversion.setter
    def specversion(self, specversion: str):
        self.message['spectversion'] = specversion

    @property
    def source(self) -> str:
        return self.message.get('source')

    @source.setter
    def source(self, source: str):
        self.message['source'] = source

    @property
    def id(self) -> str:
        return self.message.get('id')

    @id.setter
    def id(self, id: str):
        self.message['id'] = id

    @property
    def time(self) -> str:
        return self.message.get('time')

    @time.setter
    def time(self, time: str):
        self.message['time'] = time

    @property
    def schemaurl(self) -> str:
        return self.message.get('schemaurl')

    @schemaurl.setter
    def schemaurl(self, schemaurl: str):
        self.message['schemaurl'] = schemaurl

    @property
    def contenttype(self) -> str:
        return self.message.get('contenttype')

    @contenttype.setter
    def contenttype(self, contenttype: str):
        self.message['contenttype'] = contenttype

    @property
    def data(self) -> Any:
        return self.message.get('data')

    @data.setter
    def data(self, data: Any):
        self.message['data'] = data

    def __getitem__(self, key):
        return self.message[key]

    def __setitem__(self, key, value):
        self.message[key] = value

    def __delitem__(self, key):
        del self.message[key]

    def __iter__(self):
        return iter(self.message)

    def __contains__(self, value):
        return value in self.message

    def __getattr__(self, name):
        if name in ('clear', 'copy', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values'):
            return getattr(self.message, name)
        try:
            return self.message[name]
        except KeyError:
            raise AttributeError
