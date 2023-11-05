import os
import openai
import json
import re
import ctext
import common
import get_c_key
import OPENAI_KEY

openai.api_key = OPENAI_KEY.key




pare_json_path = "key_pare.json"
# 定义一个生成器函数来产生唯一的占位符
def unique_placeholder():
    count = 0
    while True:
        yield f"CHINESE_PLACEHOLDER_{count}"
        count += 1

# 函数用于替换匹配到的中文并记录下来
def replace_with_placeholder(match, placeholder_generator, placeholders_map):
    placeholder = next(placeholder_generator)
    placeholders_map[placeholder] = match.group(0)
    return placeholder




with open(pare_json_path, 'r',encoding="utf-8") as f:
        pare_json_data = json.load(f)
trans = 0
record_name = {}
#讀檔案
def Translate_Send(p_str , isName):


    #如果是名字，就找原生裡面有沒有
    if isName:
       lowp = p_str.lower()
       if lowp in pare_json_data["name"]:
           record_name[p_str] = pare_json_data["name"][lowp]
           return pare_json_data["name"][lowp]
    
    #先判斷字串中有沒有法術關鍵字 要取代
    p_str = ReplaceMent(r"{@spell\s+([^}|]+)" ,p_str ,pare_json_data["spell"] )
    #先判斷字串中有沒有法術關鍵字 要取代
    p_str = ReplaceMent(r"{@skill\s+([^}|]+)" ,p_str ,ctext.skillKeyToDisplay)
    p_str = ReplaceMent(r"{@condition\s+([^}|]+)",p_str ,ctext.condKeyToDisplay)
    p_str = ReplaceMent(r"{@action\s+([^}|]+)" ,p_str ,pare_json_data[get_c_key.RC_Action])
    p_str = ReplaceMent(r"{@feat\s+([^}|]+)" ,p_str ,pare_json_data[get_c_key.RC_Feat])
    p_str = ReplaceMent(r"{@item\s+([^}|]+)",p_str ,pare_json_data[get_c_key.RC_ITEM])


    # spell_match = re.search(r'\{@spell\s+([^\}]+)\}', p_str)
    # if spell_match:
    #     keyword = spell_match.group(1)
    #     if keyword in pare_json_data["spell"]:
    #         p_str.replace(keyword,pare_json_data["spell"][keyword])

    #取代字串
    for n,v in record_name.items():
        patten = re.escape(n)
        p_str = re.sub(patten, v, p_str, flags=re.IGNORECASE)
        if p_str == v:
            return p_str
        
    
    
    for n,v in ctext.baseToDisplay.items():
        patten = re.escape(n)
        p_str = re.sub(patten, v, p_str, flags=re.IGNORECASE)
        if p_str == v:
            return p_str
    
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
    placeholder_generator = unique_placeholder()
    placeholders_map = {}
     # 替换中文为占位符
    json_with_placeholders = chinese_pattern.sub(
        lambda match: replace_with_placeholder(match, placeholder_generator, placeholders_map), 
        p_str
    )

    if trans == 2:
        return "%VALUE%"
    
    if trans == 1:
         return p_str
     # 構造請求
    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
         {"role": "system", "content": "You will be provided with a sentence or a set of terms in English related to Dungeons & Dragons gameplay, and your task is to translate it into traditional Chinese. The translation should be in accordance with the terminology commonly used in D&D contexts. Do not translate anything inside curly braces and adhere to any specific instructions related to D&D terms, such as translating 'bonus action' as '附贈動作'."},
         {"role": "user", "content": json_with_placeholders}
     ],
    )
    rstr = completion.choices[0].message.content.strip()
    
    
 # 使用placeholders_map将占位符替换回原来的中文
    for placeholder, chinese in placeholders_map.items():
        rstr = rstr.replace(placeholder, chinese)
    
    if isName:
        record_name[p_str] = rstr
    return rstr


def ReplaceMent(keyplace , all_str , diction):

    matchs = re.findall(keyplace,all_str)
    if matchs:
        for index ,keyword in enumerate(matchs):
            lower_key = keyword.lower()
            if lower_key in diction:
                all_str = all_str.replace(keyword,diction[lower_key]) 
    return all_str

def ParseFilter(str):
    #處理filter
    
    # 處理每個匹配
    # 正則表達式來匹配@filter後的文字，並且捕獲直到下一個|為止的來源
    matches = re.finditer(r'\{@filter ([^\|]+)\|([^|]+)((?:\|[^|]+)*)', str)
    if matches:
       # 處理每個匹配
        for match in matches:
            text = match.group(1)
            type = match.group(2)
            options_str = match.group(3)

            # 將選項按|分隔並進一步分隔=為字典，如果值中包含;則將其轉為列表
            options = {}
            for opt in options_str.strip('|').split('|'):
                if '=' in opt:
                    key, value = opt.split('=')
                    options[key] = []
                    # 如果值中包含分號，則將值轉換為列表
                    if ';' in value:
                        value = value.split(';')
                        options[key]= value
                    else:
                        options[key].append(value)

def GetFilterContent(txt , type, options):
    retxt = txt
    # if type == "items":
    #     key = "item"
    #     if txt.lower() in pare_json_data[key]:
    #         retxt = pare_json_data[key]
    
    # if type == "spells":
        
        
        
    

def ParseToSendTranslate(json_data, parse_key , topkey):
    if isinstance(json_data, list):
        for index, value in enumerate(json_data):
            if isinstance(value,str):
                json_data[index] = Translate_Send(value , False)
                print("[List] topkey ="+ topkey+" value = "+json_data[index])
            else:
                ParseToSendTranslate(value,parse_key,"")
    elif isinstance(json_data,dict):

        if common.SRC_ENG_NAME in json_data and common.SRC_NAME in json_data:
             json_data[common.SRC_NAME] = Translate_Send(json_data[common.SRC_ENG_NAME], True)
             print("[NAME]  value = "+json_data[common.SRC_NAME])
        for index, value in json_data.items():
            if index in parse_key :
                if index == common.SRC_ENG_NAME or index == common.SRC_NAME:
                    continue
                if isinstance(value,str):
                    json_data[index] = Translate_Send(value,False)
                    print("[DICT] key = "+index+"  value = "+json_data[index])
                else:
                    ParseToSendTranslate(value,parse_key , index)         
    else:
        return
    

