import json
import os
import common

# 指定要掃描的資料夾
folder_path = "./parse_skill/data"
outpath = "./parse_skill/result"
# 讀取 sources.json
sources_filepath = "./parse_skill/sources.json"

# def add_eng_name_to_json(data):
#     if isinstance(data, list):  # 如果是列表，对每一个元素递归调用此函数
#         for item in data:
#             add_eng_name_to_json(item)
#     elif isinstance(data, dict):  # 如果是字典
#         if "name" in data and "ENG_name" not in data:  # 如果有"name"键而没有"ENG_name"
#             data["ENG_name"] = data["name"]  # 复制"name"的值到"ENG_name"
#         for key in data:  # 对字典中的每个键
#             if isinstance(data[key], (dict, list)):  # 如果键对应的值是列表或字典
#                 add_eng_name_to_json(data[key])  # 递归调用

def ParseSkill(json_data ,source):
    for index, value in enumerate(json_data["spell"]):
        r_name = value["ENG_name"]
        s_main = source[value["source"]][r_name]
        value["classes"] = {}
        if "class" in s_main:
            value["classes"]["fromClassList"] = s_main["class"]
        if "classVariant" in s_main:
            value["classes"]["fromClassListVariant"] = s_main["classVariant"]

        



with open(sources_filepath, 'r',encoding="utf-8") as f:
    sources_data = json.load(f)

# 列出資料夾下所有的文件
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    
    #找出source為何


    # 檢查是否為 .json 檔案
    if filename.endswith(".json"):
        # 讀取 JSON 檔案
        with open(filepath, 'r',encoding="utf-8") as f:
            data = json.load(f)
            common.add_eng_name_to_json(data)
            common.pop_version(data)
            ParseSkill(data , sources_data)

        outfliepath = os.path.join(outpath , filename)

        # 將修改後的資料寫回到 example.json
        with open(outfliepath, 'w',encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
