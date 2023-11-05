import re
import os
import json
import common

SRC_PATH = "./parse_mixData/translate_result"
SRC_PROJECT_DATA_PATH = "D:/5etool_web/5etool/data"
SRC_C_FEAT = "feats"
SRC_C_ITEM = "items"
SRC_C_LENG = "leng"
SRC_C_RACE = "race"
SRC_C_BACKGROUND = "background"

SRC_C_fluf_race = "frace"
SRC_C_fluf_item = "fitem"
SRC_C_fluf_feat = "ffeat"
SRC_C_fluf_bg = "fbg"

S_FILENAME = "filename"
S_TOPKEY = "topkey"
S_OUTPUT = "output"


SRC_PROJECT_CLASS_DATA_PATH = "D:/5etool_web/5etool/data/class/"



out_path = {}
out_path[SRC_C_FEAT]={}
out_path[SRC_C_FEAT][S_FILENAME] = "feats.json"
out_path[SRC_C_FEAT][S_OUTPUT] = "feats.json"
out_path[SRC_C_FEAT][S_TOPKEY] = "feat"

out_path[SRC_C_ITEM]={}
out_path[SRC_C_ITEM][S_FILENAME] = "items.json"
out_path[SRC_C_ITEM][S_OUTPUT] = "items.json"
out_path[SRC_C_ITEM][S_TOPKEY] = "item"


out_path[SRC_C_RACE]={}
out_path[SRC_C_RACE][S_FILENAME] = "races.json"
out_path[SRC_C_RACE][S_OUTPUT] = "races.json"
out_path[SRC_C_RACE][S_TOPKEY] = "race"


out_path[SRC_C_LENG]={}
out_path[SRC_C_LENG][S_FILENAME] = "legendarygroups.json"
out_path[SRC_C_LENG][S_OUTPUT] = "bestiary/legendarygroups.json"
out_path[SRC_C_LENG][S_TOPKEY] = "legendaryGroup"

out_path[SRC_C_BACKGROUND]={}
out_path[SRC_C_BACKGROUND][S_FILENAME] = "backgrounds.json"
out_path[SRC_C_BACKGROUND][S_OUTPUT] = "backgrounds.json"
out_path[SRC_C_BACKGROUND][S_TOPKEY] = "background"

out_path[SRC_C_fluf_race]={}
out_path[SRC_C_fluf_race][S_FILENAME] = "fluff-races.json"
out_path[SRC_C_fluf_race][S_OUTPUT] = "fluff-races.json"
out_path[SRC_C_fluf_race][S_TOPKEY] = "raceFluff"

out_path[SRC_C_fluf_item]={}
out_path[SRC_C_fluf_item][S_FILENAME] = "fluff-items.json"
out_path[SRC_C_fluf_item][S_OUTPUT] = "fluff-items.json"
out_path[SRC_C_fluf_item][S_TOPKEY] = "itemFluff"

out_path[SRC_C_fluf_feat]={}
out_path[SRC_C_fluf_feat][S_FILENAME] = "fluff-feats.json"
out_path[SRC_C_fluf_feat][S_OUTPUT] = "fluff-feats.json"
out_path[SRC_C_fluf_feat][S_TOPKEY] = "featFluff"


out_path[SRC_C_fluf_bg]={}
out_path[SRC_C_fluf_bg][S_FILENAME] = "fluff-backgrounds.json"
out_path[SRC_C_fluf_bg][S_OUTPUT] = "fluff-backgrounds.json"
out_path[SRC_C_fluf_bg][S_TOPKEY] = "backgroundFluff"


def CombineSource(out_data,topkey_name,out_put_name):
    filepath = os.path.join(SRC_PROJECT_DATA_PATH, out_put_name)
    with open(filepath, 'r',encoding="utf-8") as f:
            data = json.load(f)

    if not data:
        return
    if topkey_name not in data:
        return
    
    for index, content in enumerate(out_data):
        print("data : "+ content[common.SRC_NAME])
        ori_engname = content[common.SRC_ENG_NAME]
        ori_source =  content[common.SRC_SOURCE]
        get_data = False
        for ni, nc in enumerate(data[topkey_name]):
            if common.SRC_ENG_NAME in nc:
                if nc[common.SRC_ENG_NAME] == ori_engname and nc[common.SRC_SOURCE] == ori_source:
                    data[topkey_name][ni] = content
                    get_data = True
                    break
        
        if not get_data:
            data[topkey_name].append(content)
            
    with open(filepath, 'w',encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)  

#職業合併
def CombineSource_Class(out_data,topkey_name,out_put_name):
    filepath = os.path.join(SRC_PROJECT_DATA_PATH, out_put_name)
    with open(filepath, 'r',encoding="utf-8") as f:
            data = json.load(f)

    if not data:
        return
    if topkey_name not in data:
        return
    
    for index, content in enumerate(out_data):
        print("data : "+ content[common.SRC_NAME])
        ori_engname = content[common.SRC_ENG_NAME]
        ori_source =  content[common.SRC_SOURCE]
        get_data = False
        for ni, nc in enumerate(data[topkey_name]):
            if common.SRC_ENG_NAME in nc:
                if nc[common.SRC_ENG_NAME] == ori_engname and nc[common.SRC_SOURCE] == ori_source:
                    data[topkey_name][ni] = content
                    get_data = True
                    break
        
        if not get_data:
            data[topkey_name].append(content)
            
    with open(filepath, 'w',encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)  



for k,v in out_path.items():
    fp = os.path.join(SRC_PATH , v[S_FILENAME])
    if not os.path.exists(fp):
        continue
    with open(fp, 'r',encoding="utf-8") as f:
        data = json.load(f)
        if data:
            print("combine : "+ v[S_FILENAME])
            CombineSource(data  , v[S_TOPKEY], v[S_OUTPUT])
    
        