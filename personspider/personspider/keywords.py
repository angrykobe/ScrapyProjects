import xlrd

def read_excel():
    index = [7, 8, 9, 13, 15, 17]
    keywords = []
    excelfile =  xlrd.open_workbook('mingdan.xls')

    sheet = excelfile.sheet_by_index(0)

    for i in range(1, sheet.nrows-1):
        name = sheet.cell(i,2).value
        oneline = [name+' '+sheet.cell(i, x).value for x in index]
        oneline.insert(0,name)
        oneline.insert(1,name+' 北京大学')
        oneline.insert(2,name+' 软件与微电子学院')
        oneline.insert(3,name+' 领英')
        keywords.append(oneline);

    return keywords

if __name__ ==  '__main__':
    pass
    # k = utils()
    # print(k.read_excel())