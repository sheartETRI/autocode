from networks.codenet.nodes import *
from pydantic import BaseModel
from src.config import Config
from src.graph import Graph
from src.utils import registry  # isort:skip
# import json

class CodeNet(BaseModel):
    graph: Graph = None
    def __init__(self, **data):
        super().__init__(**data)

    def load_compile_graph(self):
        print('prepare network graph')
        # yaml 파일을 기반으로 그래프 구성
        
        # import pdb; pdb.set_trace()
        
        graph_config = Config(path="networks/codenet/codenet.yaml")
        nodes = graph_config.graph.nodes
        node_functions = {}
        for node in nodes:
            # print(f" - {node.name}: {node.type}")
            entry = {node.type : registry.node_registry[node.type](key=node.name)}
            node_functions.update(entry)
               
        # 그래프 구성을 기반으로 그래프를 실제 생성하고 컴파일
        self.graph = Graph(config=graph_config.graph).compose_and_compile(node_functions=node_functions)
        return self.graph
    
    def run(self, state: dict):
        print('run network graph')
        result = self.graph.invoke(state)

        return result

