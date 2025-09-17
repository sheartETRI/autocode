from pydantic import BaseModel
from src.network.config import Config
from src.network.graph import Graph
from src.utils import registry

class Network(BaseModel):
    graph: Graph = None
    def __init__(self, **data):
        super().__init__(**data)
    
    # 그래프 구성을 위한 정보 수집
    def gather_graph_info(self, graph_path):
        graph_config = Config(path=graph_path)
        nodes = graph_config.graph.nodes
        node_functions = {}
        for node in nodes:
            # print(f" - {node.name}: {node.type}")
            entry = {node.type : registry.node_registry[node.type](key=node.name)}
            node_functions.update(entry)        
        return graph_config, node_functions
    
    # 그래프 구성 및 컴파일
    def compose_and_compile(self, graph, node_functions):
        self.graph = Graph(config=graph).compose_and_compile(node_functions=node_functions)
        return self.graph
    
    # 그래프 실행
    def run(self, state: dict):
        # print('run network graph')
        result = self.graph.invoke(state)
        return result
    
    # 그래프 구조 출력
    def print_graph(self):
        nx_graph = self.graph.get_graph()
        print("Nodes:")
        print(list(nx_graph.nodes))

        print("\nEdges:")
        for edge in nx_graph.edges:
            print(edge)
         
    # 특정 노드의 선행 노드 출력   
    def print_preds(self, node_name: str):
        nx_graph = self.graph.get_graph()
        preds = [source for (source, target, data, conditional) in nx_graph.edges if target == node_name]
        print("Predecessors:")
        for pred in preds:
            print(pred)
    
    # 특정 노드의 후행 노드 출력
    def print_succs(self, node_name: str):
        nx_graph = self.graph.get_graph()
        succs = [target for (source, target, data, conditional) in nx_graph.edges if source == node_name]
        print("Successors:")
        for succ in succs:
            print(succ)