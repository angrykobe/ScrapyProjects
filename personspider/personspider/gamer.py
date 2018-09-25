import xlrd
import os, os.path
import json
base_path = 'D:/game'

def getDupGamer():

    files = os.listdir(base_path);

    gamer = {}
    total = 0;
    for filename in files:
        file_path = os.path.join(base_path, filename)
        excelfile = xlrd.open_workbook(file_path)
        sheet = excelfile.sheet_by_index(0)

        nums = sheet.nrows
        total += nums - 1;
        for i in range(1, nums):
            name = sheet.cell(i,0).value
            if name in gamer.keys():
                count = gamer[name] + 1
            else:
                count = 1
            gamer[name] = count

    return gamer, total

def statistics():

    gamer, total = getDupGamer()
    dupgamer = {item[0]:item[1] for item in gamer.items() if item[1]>1 }
    print("官方查出作弊次数： {}".format(total))
    print("多次查出作弊的人数： {}".format(len(dupgamer)))
    print("二次查出作弊的人数： {}".format(len({item[0]: item[1] for item in dupgamer.items() if item[1]==2})))
    print("三次查出作弊的人数： {}".format(len({item[0]: item[1] for item in dupgamer.items() if item[1]==3})))
    print({item[0]: item[1] for item in dupgamer.items() if item[1] == 3})
    print("四次查出作弊的人数： {}".format(len({item[0]: item[1] for item in dupgamer.items() if item[1]==4})))
    print({item[0]: item[1] for item in dupgamer.items() if item[1] == 4})
    print("五次查出作弊的人数： {}".format(len({item[0]: item[1] for item in dupgamer.items() if item[1]==5})))
    print({item[0]: item[1] for item in dupgamer.items() if item[1] == 5})
    print("六次查出作弊的人数： {}".format(len({item[0]: item[1] for item in dupgamer.items() if item[1]==6})))

    print("4次作弊被查的大佬")
    for item in {item[0]: item[1] for item in dupgamer.items() if item[1] == 4}.items():
        print(item[0])
    print("5次作弊被查的大佬")
    for item in {item[0]: item[1] for item in dupgamer.items() if item[1] == 5}.items():
        print(item[0])
    # pro = duplen / (total - duplen * 2)
    # print("重复被封禁的人数占比{:.2f}".format(pro))
    # print(dupgamer)

def jsonload():
    person = []
    with open('spiders/result_nodoc.json', 'r', encoding='utf-8') as f:
        for line in f:
            person.append(dict(json.loads(line)))
    return person
if __name__ == '__main__':
    # statistics()
    # getFiles()
    jsonload()