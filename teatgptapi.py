import openai
import os

chatGPT_key = os.getenv('AI_APIKEY', None)

completion = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': 'Hello!'}
    ],
    temperature=0
)

print(completion['choices'][0]['message']['content'])
