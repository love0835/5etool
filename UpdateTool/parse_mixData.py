import json
import os
import book_key
import common



# 指定要掃描的資料夾
folder_path = "./parse_mixData/data"
class_path = './parse_mixData/data/class/'
outpath = "./parse_mixData/result"
class_outpath = "./parse_mixData/result/class/"

top_keys ={"feats":"feat" , "items":"item" , "legendarygroups":"legendaryGroup" , "races":"race" , "backgrounds":"background"}
top_keys["fluff-feats"] = "featFluff"
top_keys["fluff-items"] = "itemFluff"
top_keys["fluff-races"] = "raceFluff"
top_keys["fluff-backgrounds"] = "backgroundFluff"

class_top_keys = ["subclassFeature"]


out_put = []

out_class_put = {}

def GetJson(out, json_data):
    for index, value in enumerate(json_data):
        if "source" in value and value["source"] == book_key.SRC_BOOK:
            value.pop("_versions", 'No version')
            out.append(value)
    return out


# 讀取 sources.json
# sources_filepath = "sources.json"

# with open(sources_filepath, 'r',encoding="utf-8") as f:
    # sources_data = json.load(f)


# 列出資料夾下所有的文件
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    out_put = []
    #找出source為何


    # 檢查是否為 .json 檔案
    if filename.endswith(".json"):
        # 讀取 JSON 檔案
        with open(filepath, 'r',encoding="utf-8") as f:
            data = json.load(f)
            basename, extension = os.path.splitext(filename)
            if basename in top_keys:
                GetJson(out_put ,data[top_keys[basename]])
                common.add_eng_name_to_json(out_put)
                common.pop_version(out_put)
                

        outfliepath = os.path.join(outpath , filename)

        # 將修改後的資料寫回到 example.json
        with open(outfliepath, 'w',encoding='utf-8') as f:
            json.dump(out_put, f, indent=4, ensure_ascii=False)
    
# PARSE CLASS
for filename in os.listdir(class_path):
    filepath = os.path.join(class_path, filename)
    out_class_put = {}
    # 檢查是否為 .json 檔案
    if filename.endswith(".json"):
        # 讀取 JSON 檔案
        with open(filepath, 'r',encoding="utf-8") as f:
            data = json.load(f)
            
            common.add_eng_name_to_json(data)
            common.pop_version(data)
            for ckey in class_top_keys:
                out_class_put[ckey] = []
                if ckey in data:
                    out_class_put[ckey] =GetJson(out_class_put[ckey], data[ckey])
            
            sub_key = "subclasses"
            p = [{sub_key:[]}]
            temp_class_data ={} 
            temp_class_data[sub_key] = []
            
            if "subclass" in data:
                temp_class_data[sub_key] = GetJson(temp_class_data[sub_key], data["subclass"])
            
            out_class_put["class"] = []
            out_class_put["class"].append(temp_class_data)

        outfliepath = os.path.join(class_outpath , filename)

        # 將修改後的資料寫回到 example.json
        with open(outfliepath, 'w',encoding='utf-8') as f:
            json.dump(out_class_put, f, indent=4, ensure_ascii=False)