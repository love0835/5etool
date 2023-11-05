import os
import openai
import json
import re
import ctext
import common
import get_c_key
import OPENAI_KEY

openai.api_key = OPENAI_KEY.key



record_name = {}


pare_json_path = "key_pare.json"
with open(pare_json_path, 'r',encoding="utf-8") as f:
        pare_json_data = json.load(f)
trans = 0
#讀檔案
def Translate_Send(p_str , isName):

    #如果是名字，就找原生裡面有沒有
    if isName:
       lowp = p_str.lower()
       if lowp in pare_json_data["name"]:
           record_name[p_str] = pare_json_data["name"][lowp]
           return pare_json_data["name"][lowp]
    
    #先判斷字串中有沒有法術關鍵字 要取代
    p_str = ReplaceMent(r'\{@spell\s+([^\}]+)\}' ,p_str ,pare_json_data["spell"] )
    #先判斷字串中有沒有法術關鍵字 要取代
    p_str = ReplaceMent(r'\{@skill\s+([^\}]+)\}' ,p_str ,ctext.skillKeyToDisplay)
    p_str = ReplaceMent(r'\{@condition\s+([^\}]+)\}' ,p_str ,ctext.condKeyToDisplay)
    p_str = ReplaceMent(r'\{@action\s+([^\}]+)\}' ,p_str ,pare_json_data[get_c_key.RC_Action])
    p_str = ReplaceMent(r'\{@feat\s+([^\}]+)\}' ,p_str ,pare_json_data[get_c_key.RC_Feat])
    p_str = ReplaceMent(r'\{@item\s+([^\}]+)\}' ,p_str ,pare_json_data[get_c_key.RC_ITEM])


    # spell_match = re.search(r'\{@spell\s+([^\}]+)\}', p_str)
    # if spell_match:
    #     keyword = spell_match.group(1)
    #     if keyword in pare_json_data["spell"]:
    #         p_str.replace(keyword,pare_json_data["spell"][keyword])

    #取代字串
    for n,v in record_name.items():
        p_str = p_str.replace(n, v)
    
    if trans == 2:
        return "%VALUE%"
    
    if trans == 1:
         return p_str
     # 構造請求
    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
         {"role": "system", "content": "You will be provided with a sentence in English, and your task is to translate it into traditional chinese, but do not translate anything inside curly braces"},
         {"role": "user", "content": p_str}
     ],
    )
    rstr = completion.choices[0].message.content.strip()
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