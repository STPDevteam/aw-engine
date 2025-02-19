from memory import EventMemoryNode
from aw_engine import Event
from generative_persona.generative_memory import GenerativeEventMemoryNode
import json
diction = {
    "key_id": "test",
    "event_count": 1,
    "type_event_count": 2,
    "event_type": "test",
    "depth": 3,
    "created": 4,
    "expiration": 5,
    "subject": "test",
    "predicate": "test",
    "object": "test",
    "description": "test",
    "embedding_key": "test",
    "poignancy": 6,
    "keywords": "test",
    "filling": "test",
    "location": "test",
    "last_accessed": None
}
event = GenerativeEventMemoryNode(diction)

print(event.to_json())
loaded = json.loads(event.to_json())

