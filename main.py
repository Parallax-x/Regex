from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)

pattern = re.compile(r'(\+7|8)\s?\(?(\d{3})\)?(\s|-)?(\d{3})-?(\d{2})-?(\d{2})(\s\(?(доб\.)\s(\d{4})\)?)?')
subst_pattern = r'+7(\2)\4-\5-\6'
subst_pattern1 = r' \8\9'

contacts_dict = {}
for contact in contacts_list[1:]:
    lf_name = ' '.join(contact[:3]).split(' ')[:3]
    if len(contact[5]) > 18:
        number = pattern.sub(subst_pattern, contact[5]) + pattern.sub(subst_pattern1, contact[5])
    else:
        number = pattern.sub(subst_pattern, contact[5])
    lf_name_key = ' '.join(lf_name[:2])
    contact_dict = {lf_name_key: {}}
    if lf_name[2] != '':
        contact_dict[lf_name_key].update({'surname': lf_name[2]})
    if contact[3] != '':
        contact_dict[lf_name_key].update({'organization': contact[3]})
    if contact[4] != '':
        contact_dict[lf_name_key].update({'position': contact[4]})
    if number != '':
        contact_dict[lf_name_key].update({'phone': number})
    if contact[6] != '':
        contact_dict[lf_name_key].update({'email': contact[6]})
    # print(contact_dict)
    if contacts_dict.get(lf_name_key):
        contacts_dict[lf_name_key].update(contact_dict[lf_name_key])
    else:
        contacts_dict[lf_name_key] = contact_dict[lf_name_key]
# pprint(contacts_dict)

list_for_write = []
for key, value in contacts_dict.items():
    list_for_write.append({
        'lastname': key.split(' ')[0],
        'firstname': key.split(' ')[1],
        'surname': value.get('surname'),
        'organization': value.get('organization'),
        'position': value.get('position'),
        'phone': value.get('phone'),
        'email': value.get('email')
    })
pprint(list_for_write)

with open("phonebook.csv", "w", encoding='utf-8') as f:
    columns = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
    datawriter = csv.DictWriter(f, delimiter=',', fieldnames=columns)
    datawriter.writeheader()
    for data in list_for_write:
        datawriter.writerow(data)
