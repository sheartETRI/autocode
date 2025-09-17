from typing import Callable
from typing import TypedDict, Callable, Dict, Type
from autoregistry import Registry

node_registry = Registry()

class BaseNode:
    key: str
    
    def __init__(self, **data):
        self.key = data.get('key', '')

    def print_nodename(self):
        print("node_name:", self.key)