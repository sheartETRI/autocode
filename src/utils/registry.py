from typing import Callable
from typing import TypedDict, Callable, Dict, Type
from autoregistry import Registry

node_registry = Registry()

class BaseNode:
    def run(self, data):
        raise NotImplementedError("run() must be implemented.")

    def __call__(self, data):
        result = self.run(data=data)
        return result
