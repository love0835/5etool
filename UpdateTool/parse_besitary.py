import json
import os
import common



# 指定要掃描的資料夾
folder_path = "./parse_besitary/data"
outpath = "./parse_besitary/result"

# 讀取 sources.json
# sources_filepath = "sources.json"

# with open(sources_filepath, 'r',encoding="utf-8") as f:
    # sources_data = json.load(f)

# 列出資料夾下所有的文件
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    
    # 檢查是否為 .json 檔案
    if filename.endswith(".json"):
        # 讀取 JSON 檔案
        with open(filepath, 'r',encoding="utf-8") as f:
            data = json.load(f)
            common.add_eng_name_to_json(data)
            common.pop_version(data)
            # Parse(data["monster"],"")

        outfliepath = os.path.join(outpath , filename)

        # 將修改後的資料寫回到 example.json
        with open(outfliepath, 'w',encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
