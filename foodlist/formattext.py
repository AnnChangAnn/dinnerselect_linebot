
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


