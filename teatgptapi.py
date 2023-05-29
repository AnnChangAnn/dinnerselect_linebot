import openai
import os

openai.api_key = 'sk-K !xu.4 kWMEw !ur.3 wP4yBQrXfjduT !n0  BlbkFJT !-4 FExcB !xu.4 BRioP !fu hHqq !xu/6 J'
#openai.api_key = os.getenv('AI_APIKEY', None)

completion = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': 'Hello!'}
    ],
    temperature=0
)

print(completion['choices'][0]['message']['content'].replace('\n', ''))
