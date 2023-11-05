import json
import os

SRC_ENG_NAME = "ENG_name"
SRC_NAME = "name"
SRC_SOURCE = "source"
SRC_PROJECT_DATA_PATH = "D:/5etool_web/5etool/data"

def pop_version(data):
    if "_versions" in data:
        del data["_versions"]
    if isinstance(data, list):  # 如果是列表，对每一个元素递归调用此函数
        for item in data:
            add_eng_name_to_json(item)
    elif isinstance(data, dict):  # 如果是字典
        if "_versions" in data:
            del data["_versions"]
        for key in data:  # 对字典中的每个键
            if isinstance(data[key], (dict, list)):  # 如果键对应的值是列表或字典
                pop_version(data[key])  # 递归调用    

def add_eng_name_to_json(data):
    if isinstance(data, list):  # 如果是列表，对每一个元素递归调用此函数
        for item in data:
            add_eng_name_to_json(item)
    elif isinstance(data, dict):  # 如果是字典
        if "name" in data and "ENG_name" not in data:  # 如果有"name"键而没有"ENG_name"
            data["ENG_name"] = data["name"]  # 复制"name"的值到"ENG_name"
        if "shortName" in data and "ENG_shortName" not in data:  # 如果有"name"键而没有"ENG_name"
            data["ENG_shortName"] = data["shortName"]  # 复制"name"的值到"ENG_name"
        for key in data:  # 对字典中的每个键
            if isinstance(data[key], (dict, list)):  # 如果键对应的值是列表或字典
                add_eng_name_to_json(data[key])  # 递归调用   





def CombineSource(out_data,topkey_name,file_name):
    filepath = os.path.join(SRC_PROJECT_DATA_PATH, file_name)
    with open(filepath, 'r',encoding="utf-8") as f:
            data = json.load(f)

    if not data:
        return
    if topkey_name not in data:
        return
    
    for index, content in enumerate(out_data):
        ori_engname = out_data[SRC_ENG_NAME]
        ori_source =  out_data[SRC_SOURCE]
        get_data = False
        for ni, nc in enumerate(data[topkey_name]):
            if SRC_ENG_NAME in nc:
                if nc[SRC_ENG_NAME] == ori_engname and nc[SRC_SOURCE] == ori_source:
                    data[topkey_name][ni] = content
                    get_data = True
                    break
        
        if not get_data:
            data[topkey_name].append(content)
            
    with open(filepath, 'w',encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)  
    




    
    

            