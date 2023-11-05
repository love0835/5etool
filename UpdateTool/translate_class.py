import os
import openai
import json
import re
import translate


parse_key = {}
parse_key["name"] = 0 
parse_key["languages"] = 0
parse_key["trait"] = 0
parse_key["entries"] = 0
parse_key["action"] = 0
parse_key["senses"] = 0
parse_key["legendary"] = 0
parse_key["resist"] = 0
parse_key["spellcasting"] = 0
parse_key["variant"] = 0
parse_key["entriesHigherLevel"] = 0
parse_key["components"] = 0
parse_key["m"] = 0
parse_key["text"] = 0
parse_key["items"] = 0
parse_key["colLabels"] = 0
parse_key["caption"] = 0
parse_key["rows"] = 0

parse_key["class"] = 0
parse_key["subclasses"] = 0
parse_key["shortName"] = 0
parse_key["entry"] = 0
parse_key["subclassFeature"] = 0


# 指定要掃描的資料夾
folder_path = "./parse_mixData/result/class"
outpath = "./parse_mixData/translate_result/class"


# 列出已輸出資料夾下所有的文件

for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    
    # 檢查是否為 .json 檔案
    if filename.endswith(".json"):
        # 讀取 JSON 檔案
        with open(filepath, 'r',encoding="utf-8") as f:
            data = json.load(f)
            print(filename)
            translate.ParseToSendTranslate(data,parse_key,"")

        outfliepath = os.path.join(outpath , filename)

        # 將修改後的資料寫回到 example.json
        with open(outfliepath, 'w',encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
