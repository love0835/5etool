import json
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
parse_key = {"name":0,"languages":0,"trait":0,"entries":0,"action":0,"senses":0,"legendary":0 ,"resist":0 , "spellcasting":0 , "variant":0}
#記錄有那些用到的key
record_name = {}
trans = 1

def pop_version(data):
    if "_versions" in data:
        del data["_versions"]

def SendTranslate(p_str):
    #取代字串
    for n,v in record_name.items():
        p_str.replace(n, v)
        
    if trans != 1:
        return "@TEST_VALUE@"
    # 構造請求
    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You will be provided with a sentence in English, and your task is to translate it into traditional chinese"},
        {"role": "system", "content": "Translate the result with reference to DND as much as possible."},
        {"role": "user", "content": p_str}
    ],
    )
    return completion.choices[0].message.content.strip()

def add_eng_name_to_json(data):
    if isinstance(data, list):  # 如果是列表，对每一个元素递归调用此函数
        for item in data:
            add_eng_name_to_json(item)
    elif isinstance(data, dict):  # 如果是字典
        if "name" in data and "ENG_name" not in data:  # 如果有"name"键而没有"ENG_name"
            data["ENG_name"] = data["name"]  # 复制"name"的值到"ENG_name"
        for key in data:  # 对字典中的每个键
            if isinstance(data[key], (dict, list)):  # 如果键对应的值是列表或字典
                add_eng_name_to_json(data[key])  # 递归调用    

def Parse(json_data , topkey):
    if isinstance(json_data, list):
        for index, value in enumerate(json_data):
            if isinstance(value,str):
                json_data[index] = SendTranslate(value)
                print("[List] topkey ="+ topkey+" value = "+json_data[index])
            else:
                Parse(value,"")
    elif isinstance(json_data,dict):
        for index, value in json_data.items():
            if index in parse_key :
                if isinstance(value,str):
                    json_data[index] = SendTranslate(value)
                    if index == "name":
                        record_name[json_data["ENG_name"]] = json_data[index]
                    print("[DICT] key = "+index+"  value = "+json_data[index])
                else:
                    Parse(value , index)
                   
    else:
        return



        
# 指定要掃描的資料夾
folder_path = "./data"
outpath = "./result"
# 讀取 sources.json
# sources_filepath = "sources.json"

# with open(sources_filepath, 'r',encoding="utf-8") as f:
    # sources_data = json.load(f)

# 列出資料夾下所有的文件
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    
    #找出source為何


    # 檢查是否為 .json 檔案
    if filename.endswith(".json"):
        # 讀取 JSON 檔案
        with open(filepath, 'r',encoding="utf-8") as f:
            data = json.load(f)
            add_eng_name_to_json(data)
            pop_version(data)
            Parse(data,"")

        outfliepath = os.path.join(outpath , filename)

        # 將修改後的資料寫回到 example.json
        with open(outfliepath, 'w',encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
