import os
import requests
import sys

# 从环境变量获取API_KEY
API_KEY = os.getenv('API_KEY')
API_ENDPOINT = os.getenv('API_ENDPOINT')

def translate_text(text):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # 请求体
    data = {
        'model': 'gpt-4o-mini',  # 或其他模型
        'messages': [
            {
                'role': 'system',
                'content': f'Act as an Chinese translator, user will sent you Mikrotik Change log to you in English, translate to Chinese. Keep the meaning same. Do not stop until finished.'
            },
            {
                'role': 'user',
                'content': f'{text}'
            }
        ]
    }
    
    # 发送请求
    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def main(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        english_text = f.read()

    # 翻译文本
    #每20行翻译一次
    translated_text = ''
    for i in range(0, len(english_text.split('\n')), 20):
        text = '\n'.join(english_text.split('\n')[i:i+20])
        translated_text += translate_text(text) + '\n\n'
    

    if translated_text:
        # 将翻译后的文本和原文写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("This is a Patched Version of routerOS.For Educational Purpose Only\n\n Refer to https://github.com/fujr/MikroTikPatch\n\n" + translated_text + '\n\n' + english_text)

if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]
    main(input, output)
