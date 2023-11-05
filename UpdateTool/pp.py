import re

# 你的輸入字串
input_string = "一種{@filter musical instrument|items|source=phb|miscellaneous=mundane|type=instrument}或{@filter artisan's tools|items|source=phb|miscellaneous=mundane|type=artisan's tools}"

# 正則表達式來匹配@filter後的文字，並且捕獲直到下一個|為止的來源
matches = re.finditer(r'\{@filter ([^\|]+)\|([^|]+)', input_string)

# 打印出所有匹配的部分
for match in matches:
    text, source = match.groups()
    print(f'文字: {text}, 來源: {source}')