existing_entries = set()
existing_list = open("/Users/alex.rosen/personal/xword/dicts/XwiWordList_updated3456.dict").readlines()
for word in existing_list:
    existing_entries.add(word.split(';')[0])

new_list = open("/Users/alex.rosen/Downloads/XwiWordList.dict").readlines()

with open("/Users/alex.rosen/personal/xword/dicts/XwiWordList_delta_June2020.dict", "w") as delta:
    for word in new_list:
        if word.split(';')[0] not in existing_entries:
            delta.write(word.replace(" ", ""))

