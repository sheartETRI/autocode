import json
import os
from pathlib import Path
from pydantic import BaseModel
from networks.codenet.codenet import CodeNet

class Generator(BaseModel):
    def __init__(self, **data):
        super().__init__(**data)            
        self._load_api_keys()        

    def _load_api_keys(self):
        print('load_api_keys')
        api_keys = json.loads(Path("/home/sheart95/api_keys.json").read_text())
        for k, v in api_keys.items():
            os.environ[k] = v
            
    def _save_json(self, file_path: str, result: dict):
        # Save result as json file        
        with open(file_path, "w") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

    def run(self):
        # 입력 데이터 로드
        input_dir = "inputs"
        with open(f"{input_dir}/data.json", "r", encoding="utf-8") as f:
            input_data = json.load(f)
            
        # 네트워크 그래프 컴파일 및 실행
        network = CodeNet() # CodeNet 객체 생성
        network.load_compile_graph() # 그래프 로드 및 컴파일
        state = {'input_data': input_data} # 그래프에 전달할 초기 상태
        result = network.run(state=state) # 그래프 실행
 
        # 결과를 json 파일로 저장
        output_dir = "outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        file_path = f"{output_dir}/output.json"
        self._save_json(file_path, result)
               
        return self


