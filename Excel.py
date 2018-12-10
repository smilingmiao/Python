#coding:utf-8

import xlrd
import os
import codecs


def op_file(cwd):

    dp = os.path.join(cwd, 'it.txt')
    keys, values = get_file_keys_and_values(dp)

    xp = os.path.join(cwd, 'it.xlsx')
    chinese, others = get_excel_keys_and_values(xp)

    for ch in chinese:
        for k in keys:
            if ch == k:
                val = str(others[chinese.index(ch)]) + ";"
                values[keys.index(k)] = val

    idxs = []
    i = 0
    for idx1 in range(0, len(keys)):
        for idx2 in range(idx1 + 1, len(keys) - 1 - idx1):
            if idx1 != idx2:
                if keys[idx1] == keys[idx2]:
                    i = i + 1
                    print('INDEX ========= ' + str(i))
                    idxs.append(idx2)
                    del values[idx2]

    for k in idxs:
        del keys[k]

    f = codecs.open(os.path.join(cwd, 'new_it.txt'), 'a', 'utf-8')

    if len(keys) == len(values):
        for obj in keys:

            cur_index = keys.index(obj)

            val = values[cur_index]
            join = obj + ' = ' + val
            join = str(join)

            if len(join) == 0:
                continue
            else:
                f.write(join)
                f.write('\n')
                print(join)

        f.close()


def get_excel_keys_and_values(file):

    book = xlrd.open_workbook(file, formatting_info=False)
    sheet = book.sheet_by_index(13)
    # for col_idx in range(1, 6):
    #     if col_idx == 2 or col_idx == 3:
    #         continue
    #
    #     print('col = ' + str(col_idx) + sheet.cell_value(1, col_idx))

    chinese = []
    others = []

    is_nl = False

    #  遍历放到内存中
    for row_idx in range(1, 2183):
        row_values = sheet.row_values(row_idx)
        chinese.append('\"' + str(row_values[1]) + '\"')

        if is_nl:  #是荷兰语
            others.append('\"' + str(row_values[5]) + '\"')
        else:
            others.append('\"' + str(row_values[4]) + '\"')

    return chinese, others


def get_file_keys_and_values(file):
        keys = []
        values = []
        with codecs.open(file, 'r+', 'utf-8') as f:
            line = f.readline()
            while line:
                if len(line.strip()) == 0:
                    line = f.readline()
                else:
                    sp = line.split('=')
                    keys.append(str(sp[0]))
                    if len(sp) > 1:
                        values.append(str(sp[1]))
                    else:
                        values.append(' ')

                    line = f.readline()

        return keys, values


if __name__ == '__main__':
    op_file(os.path.expanduser('~/desktop/work'))