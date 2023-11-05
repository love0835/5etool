import re
import os
import json
import common

SRC_PATH = "./parse_mixData/translate_result/class"
SRC_PROJECT_DATA_PATH = "D:/5etool_web/5etool/data/class"
class_top_keys = ["subclassFeature"]



def CombineSource(out_data , filename):
    filepath = os.path.join(SRC_PROJECT_DATA_PATH, filename)
    with open(filepath, 'r',encoding="utf-8") as f:
            data = json.load(f)

    if not data:
        return
    
    #先合併外部變數
    for ckey in class_top_keys:
        if ckey in data:
            for out_c in out_data[ckey]:
                if common.SRC_ENG_NAME in out_c:
                    get_value = False
                    for ori_i, ori_c in  enumerate(data[ckey]):
                        if common.SRC_ENG_NAME in ori_c and ori_c[common.SRC_ENG_NAME] == out_c[common.SRC_ENG_NAME]:
                            get_value = True
                            data[ckey][ori_i] = out_c
                    if not get_value:
                        data[ckey].append(out_c)
    
    
    ckey = "class"
    sub_key = "subclasses"
    
    for out_c in out_data[ckey][0][sub_key]:
        if common.SRC_ENG_NAME in out_c:
            get_value = False
            for ori_i, ori_c in  enumerate(data[ckey][0][sub_key]):
                if common.SRC_ENG_NAME in ori_c and ori_c[common.SRC_ENG_NAME] == out_c[common.SRC_ENG_NAME]:
                    get_value = True
                    data[ckey][0][sub_key][ori_i] = out_c
            if not get_value:
                data[ckey][0][sub_key].append(out_c)
                
    with open(filepath, 'w',encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)  


for filename in os.listdir(SRC_PATH):
    filepath = os.path.join(SRC_PATH, filename)
    if filename.endswith(".json"):
         # 讀取 JSON 檔案
        with open(filepath, 'r',encoding="utf-8") as f:
            data = json.load(f)
            CombineSource(data , filename)
            
