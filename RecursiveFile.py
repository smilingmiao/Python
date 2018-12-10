import os
import re
import codecs


paths = []
keys = []
languages = []
ens = []
nls = []
its = []
jas = []
zhs = []


def find_text(text):
    subs = text.split('NSLocalizedString')
    for o in subs:
        if '@"' not in o:
            continue
        start = o.index('@"')
        end = o.index('nil')

        if end - start < 3:
            continue

        sub_str = ''
        for index in range(start + 2, end - 3):
            sub_str += o[index]

        if len(sub_str) == 0:
            continue

        keys.append(sub_str)


def compare_ls(all_keys):
    file_pos = os.path.expanduser('~/desktop/NOT')

    for k in all_keys:

        if ens.count(k) == 0:
            p_e = compose_p(file_pos, 'en.txt')
            write_to_file(k, p_e)

        if nls.count(k) == 0:
            p_n = compose_p(file_pos, 'nl.txt')
            write_to_file(k, p_n)

        if its.count(k) == 0:
            p_i = compose_p(file_pos, 'it.txt')
            write_to_file(k, p_i)

        if jas.count(k) == 0:
            pj = compose_p(file_pos, 'ja.txt')
            write_to_file(k, pj)

        if zhs.count(k) == 0:
            p_z = compose_p(file_pos, 'zh.txt')
            write_to_file(k, p_z)


def compose_p(p1, p2):
    return os.path.join(p1, p2)


def write_to_file(data, file_path):
    with codecs.open(file_path, 'a', 'utf-8') as f:
        f.write(data)
        f.write('\n')

    f.close()


def get_all_ls(ls):
    for l in ls:
        if 'Base.lproj' in l or 'en-GB.lproj' in l or 'MJRefresh' in l:
            continue

        with codecs.open(l, 'r', 'utf-8') as f:
            line = f.readline()

            while line:
                if len(line.strip()) > 0:
                    line_sp = line.split('=')
                    l_line = line_sp[0]
                    l_line = l_line.lstrip()
                    l_line = l_line.rstrip()
                    sp_l_l = l_line.split('\"')

                    length = len(sp_l_l)

                    if length < 3:
                        line = f.readline()
                        continue

                    need_s = ''
                    if length == 3:
                        need_s = need_s.join(sp_l_l[1])
                    else:
                        for i in range(1, length - 1):
                            need_s = need_s.join(sp_l_l[i])

                    if 'en.lproj' in l:
                        ens.append(need_s)
                    elif 'nl.lproj' in l:
                        nls.append(need_s)
                    elif 'it.lproj' in l:
                        its.append(need_s)
                    elif 'zh-Hans.lproj' in l:
                        zhs.append(need_s)
                    elif 'ja.lproj':
                        jas.append(need_s)

                line = f.readline()

        f.close()


def get_all(path):
    if os.path.isdir(path):

        for o in os.listdir(path):
            sub = os.path.join(path, o)
            if os.path.isdir(sub):
                lan_sp = os.path.splitext(sub)
                ext = lan_sp[1]
                if ext == '.lproj':
                    for x in os.listdir(sub):
                        if x == 'Localizable.strings':
                            lan = os.path.join(sub, x)
                            languages.append(lan)

                get_all(sub)

            else:
                split = os.path.splitext(sub)
                ext = split[1]
                if ext == '.m':
                    paths.append(sub)


def op_file(files):
    for each in files:
        read_file(each)


def read_file(des_file):
    with codecs.open(des_file, 'r', 'utf-8') as f:
        line = f.readline()
        while line:
            _line = line.rstrip()
            if 'NSLocalizedString' in _line:

                re_obj = re.search('(NSLocalizedString(.*?)nil\)(.*)).*?', line, re.M|re.I)
                if re_obj is None:
                    print('======================' + line)
                    return

                result = re_obj.group()
                count = result.count('NSLocalizedString')

                if count == 0:
                    line = f.readline()
                    continue

                else:
                    find_text(result)

            line = f.readline()

    f.close()


def find_duplicate(ps):
    _ens = []
    _zhs = []
    _jas = []
    _nls = []
    _its = []

    du_ens = []
    du_zhs = []
    du_jas = []
    du_nls = []
    du_its = []

    c_nl = 0
    c_it = 0
    c_ja = 0
    c_en = 0
    c_zh = 0

    base_pos = os.path.expanduser('~/desktop/DU')

    for l in ps:
        if 'Base.lproj' in l or 'en-GB.lproj' in l or 'MJRefresh' in l:
            continue

        with codecs.open(l, 'r', 'utf-8') as f:
            line = f.readline()

            while line:
                line = str(line).strip()
                if len(line) < 1:
                    line = f.readline()
                    continue

                if 'en.lproj' in l:
                    if _ens.count(line) == 1:
                        c_en = c_en + 1
                        if du_ens.count(line) == 0:
                            du_ens.append(line)
                            p = compose_p(base_pos, 'du_en.txt')
                            _write(line, p)
                        else:
                            line = f.readline().rstrip()
                            continue

                    else:
                        _ens.append(line)
                        p = compose_p(base_pos, 'en.txt')
                        _write(line, p)

                elif 'nl.lproj' in l:
                    if _nls.count(line) == 1:
                        c_nl = c_nl + 1
                        if du_nls.count(line) == 0:
                            du_nls.append(line)
                            p = compose_p(base_pos, 'du_nl.txt')
                            _write(line, p)
                        else:
                            line = f.readline().rstrip()
                            continue

                    else:
                        _nls.append(line)
                        p = compose_p(base_pos, 'nl.txt')
                        _write(line, p)

                elif 'it.lproj' in l:
                    if _its.count(line) == 1:
                        c_it = c_it + 1
                        if du_its.count(line) == 0:
                            du_its.append(line)
                            p = compose_p(base_pos, 'du_it.txt')
                            _write(line, p)
                        else:
                            line = f.readline().rstrip()
                            continue

                    else:
                        _its.append(line)
                        p = compose_p(base_pos, 'it.txt')
                        _write(line, p)

                elif 'zh-Hans.lproj' in l:
                    if _zhs.count(line) == 1:
                        c_zh = c_zh + 1
                        if du_zhs.count(line) == 0:
                            du_zhs.append(line)
                            p = compose_p(base_pos, 'du_zh.txt')
                            _write(line, p)

                        else:
                            line = f.readline()
                            continue

                    else:
                        _zhs.append(line)
                        p = compose_p(base_pos, 'zh.txt')
                        _write(line, p)

                elif 'ja.lproj':
                    if _jas.count(line) == 1:
                        c_ja = c_ja + 1
                        if du_jas.count(line) == 0:
                            du_jas.append(line)
                            p = compose_p(base_pos, 'du_ja.txt')
                            _write(line, p)

                        else:
                            line = f.readline()
                            continue

                    else:
                        _jas.append(line)
                        p = compose_p(base_pos, 'ja.txt')
                        _write(line, p)

                line = f.readline

    print()


def _write(line, path):
    write_to_file(line, path)


if __name__ == '__main__':
    file = os.path.expanduser('~/Oversea/IOS/iCleanPower')
    get_all(file)
    # op_file(paths)
    # print(len(keys))
    # get_all_ls(languages)
    # compare_ls(keys)
    find_duplicate(languages)