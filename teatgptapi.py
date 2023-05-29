import openai
import os
from datetime import datetime

#openai.api_key = 'sk-K !xu.4 kWMEw !ur.3 wP4yBQrXfjduT !n0  BlbkFJT !-4 FExcB !xu.4 BRioP !fu hHqq !xu/6 J'
openai.api_key = os.getenv('AI_APIKEY', None)
print(datetime.now())
completion = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': 'hello!'}
    ],
    temperature=1.2,
    max_tokens = 2000
)
print(datetime.now())
print(completion['choices'][0]['message']['content'].replace('\n', ''))
