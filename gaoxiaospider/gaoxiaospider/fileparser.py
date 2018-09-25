import codecs
import json
import locale
with codecs.open('spiders/gaoxiao.json','r','utf-8') as f:
    area_name ={}

    for line in f:
        ctx = json.loads(line)
        if ctx['sch_area'] not in area_name.keys():
            area_name[ctx['sch_area']] = []
        area_name[ctx['sch_area']].append(ctx['sch_name'])


area = []
with codecs.open('2.txt', 'r','utf-8') as f:
    for item in f:
        area.append(item.strip())
print(area)
items = area_name.items()
# locale.setlocale(locale.LC_COLLATE, "zh_CN.UTF-8")
# sorted(items,cmp=locale.strcoll ,key=lambda item:item[0],reverse=False)
sch_name = [0]*31
for item in items:
    # area.append(item[0])
    index = area.index(item[0])
    sch_name[index]  = item[1]

print(area)
print(sch_name)