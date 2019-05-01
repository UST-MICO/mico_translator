from translator.messages import CloudEvent
from translator.helpers import load_test_data
import json


class TranslatorTest:

    @staticmethod
    def _get_cloud_event_template(data):
        cloud_event = CloudEvent(json.loads(load_test_data('cloud_event_3.json')))
        cloud_event.data = data
        return cloud_event