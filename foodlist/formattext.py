#import urllib
#import re
#import random
#import datetime
#
## 請 pixabay 幫我們找圖
#def get_img_url(img_source, target):
#
#    img_source_dict = {
#        'google': [f"https://www.google.com/search?{urllib.parse.urlencode(dict([['tbm', 'isch'], ['q', target]]))}/",
#                   'img data-src="\S*"',
#                   14,
#                   -1],
#        'pixabay': [f"https://pixabay.com/images/search/{urllib.parse.urlencode(dict([['q', target]]))[2:]}/",
#                    'img srcset="\S*\s\w*,',
#                    12,
#                    -3],
#        'unsplash': [f"https://unsplash.com/s/photos/{urllib.parse.urlencode(dict([['q', target]]))[2:]}/",
#                     'srcSet="\S* ',
#                     8,
#                     -1]}
#
#    url = img_source_dict[img_source][0]
#    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
#
#    req = urllib.request.Request(url, headers = headers)
#    conn = urllib.request.urlopen(req)
#
#    print('fetch page finish')
#
#    img_list = []
#
#    for match in re.finditer(img_source_dict[img_source][1], str(conn.read())):
#        img_list.append(match.group()[img_source_dict[img_source][2]:img_source_dict[img_source][3]])
#
#    random_img_url = random.choice(img_list)
#    print('fetch img url finish')
#    print(random_img_url)
#
#    return random_img_url



def prepare_record(text):
    text_list = text.split('\n')
    
    record_list = []
    
    for i in text_list[1:]:
        temp_list = i.split(' ')
        
        temp_foodtype = temp_list[0]
        temp_foodname = temp_list[1]
        
        record = (temp_foodtype, temp_foodname)
        record_list.append(record)
        
    return record_list

def prepare_reply(text):
    text_list = text.split('\n')

    record_list = []

    for i in text_list[1:]:
        temp_list = i.split(' ')
        
        temp_foodtype = temp_list[0]
        temp_replyfront = temp_list[1]
        temp_replyend = temp_list[2]
        
        record = (temp_foodtype, temp_replyfront, temp_replyend)
        record_list.append(record)
        
    return record_list


