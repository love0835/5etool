import os
import openai

# 設定你的API密鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

# 構造請求
completion = openai.ChatCompletion.create(
  model="gpt-4",
   messages=[
    {"role": "system", "content": "You will be provided with a sentence in English, and your task is to translate it into traditional chinese"},
    {"role": "system", "content": "Translate the result with reference to DND as much as possible."},
    {"role": "user", "content": "{@atk mw} {@hit 7} to hit, reach 20 ft., one target. {@h}11 ({@damage 2d6 + 4}) slashing damage. If the target is a creature, it is {@condition grappled} (escape {@dc 15}). Until the grapple ends, the target is {@condition restrained}. The plant has four vines, each of which can grapple one target."}
  ],
  
  completion.choices[0].message.content.strip()
)

# 輸出響應的內容
print(completion.choices[0].message.content.strip())