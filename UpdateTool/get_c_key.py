import json
import os



def ReadJson(action , folder_path):
    # 列出資料夾下所有的文件
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        # 檢查是否為 .json 檔案
        if filename.endswith(".json"):
            # 讀取 JSON 檔案
            with open(filepath, 'r',encoding="utf-8") as f:
                data = json.load(f)
                action(data)


outpath = "./result"
# 讀取 sources.json
sources_filepath = "key_pare.json"  

RC_SPELL = "spell"
RC_bestiary = "monster"
RC_RACE = "race"
RC_Action = "action"
RC_ITEM = "item"
RC_LENG = "legendaryGroup"
RC_Feat = "feat"


out_data = {}
out_data["spell"] = {}  

dic_paths = {}
dic_paths[RC_bestiary] = r"D:/5etool_web/5etool/data/bestiary/"
dic_paths[RC_SPELL] = r"D:/5etool_web/5etool/data/spells/"
dic_filename_key = {}
dic_filename_key[RC_bestiary] = "bestiary-"
dic_filename_key[RC_SPELL] = "spells-"


single_files = {}
single_files[RC_RACE] = "D:/5etool_web/5etool/data/races.json"
single_files[RC_RACE] = "D:/5etool_web/5etool/data/races.json"
single_files[RC_Action] = "D:/5etool_web/5etool/data/actions.json"
single_files[RC_ITEM] = "D:/5etool_web/5etool/data/items.json"
single_files[RC_LENG] = "D:/5etool_web/5etool/data/bestiary/legendarygroups.json"
single_files[RC_Feat] = "D:/5etool_web/5etool/data/feats.json"



TOP_C = {}
TOP_C[RC_SPELL] = 0
TOP_C[RC_ITEM] = 0
TOP_C[RC_Action] = 0
TOP_C[RC_Feat] = 0

def is_english(char):
    return 'A' <= char <= 'Z' or 'a' <= char <= 'z'

def is_all_english(text):
    return all(is_english(char) for char in text if char.strip())

def PutInOutdata(key ,value , filename):
    key = key.lower()
    if key in out_data and value != out_data[key]:
        print("OUT ERROR KEY = "+key+"  old_value = "+out_data[key]+"  new_value = "+ value +"  filename = "+filename)
        return
    out_data[key] = value

def PutInOutdataTop(key ,value,topkey , filename):
    key = key.lower()
    if topkey not in out_data:
        out_data[topkey] = {}
    if key in out_data[topkey] and value != out_data[topkey][key]:
        print("OUT ERROR TopKey = "+topkey+"  KEY = "+key+"  old_value = "+out_data[topkey][key]+"  new_value = "+ value +"  filename = "+filename)
        return

    out_data[topkey][key] = value


def ParseAction_Name(json_data , filename):
    if isinstance(json_data, list):
        for index, value in enumerate(json_data):
            if not isinstance(value,str):
                ParseAction_Name(value , filename)
    elif isinstance(json_data,dict):
         for index, value in json_data.items():
            if isinstance(value,str):
                if index == "ENG_name":
                    if "name" in json_data:
                        if not is_all_english(json_data["name"]):
                            PutInOutdataTop(json_data["ENG_name"], json_data["name"],"name",filename)
                        else:
                            print("[ERR] NAME IS ENGLISH  ENG_name = "+json_data["ENG_name"]+" NAME =  "+json_data["name"]+"  filename = "+filename)
                    else:
                        print("[ERR] NO NAME  ENG_name = "+json_data["ENG_name"]+"  filename = "+filename)
            else:
                ParseAction_Name(value,filename)
    else:
        return
        
def ParseAction_TopName(json_data , key , filename):
    if key not in json_data:
        return
    for index, value in enumerate(json_data[key]):
        if "ENG_name" in value:
            if "name" in value:
                PutInOutdataTop(value["ENG_name"], value["name"],key,filename)
            else:
                print("[ERR] NO TOP NAME  ENG_name = "+value["ENG_name"]+"  filename = "+filename)
                   

def ParseAllSingleFile():
    for dicKey , filepath in single_files.items():
        if filepath.endswith(".json"):
             with open(filepath, 'r',encoding="utf-8") as f:
                 data = json.load(f)
                 if dicKey in TOP_C:
                    ParseAction_TopName(data,dicKey, filepath)
                 else:
                    ParseAction_Name(data , dicKey)

def ParseAllDiction():
    for dicKey , dic in dic_paths.items():
        for filename in os.listdir(dic):
            filepath = os.path.join(dic, filename)
            if filename.endswith(".json") and dic_filename_key[dicKey] in filename:
                with open(filepath, 'r',encoding="utf-8") as f:
                    data = json.load(f)
                    if dicKey in TOP_C:
                        ParseAction_TopName(data,dicKey, filename)
                    else:
                        ParseAction_Name(data , filename)

def main():
    #第一步
    #parse所有資料夾
    ParseAllDiction()
    #parese所有單檔
    ParseAllSingleFile()
    #寫出資料
    with open(sources_filepath, 'w',encoding='utf-8') as f:
        json.dump(out_data, f, indent=4, ensure_ascii=False)
        
        
main()