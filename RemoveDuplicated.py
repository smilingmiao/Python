import os
import codecs


def get_file():
    zh_file = appending('zh')
    ja_file = appending('ja')
    en_file = appending('en')
    nl_file = appending('nl')
    it_file = appending('it')

    return [zh_file, ja_file, en_file, nl_file, it_file]


def appending(sub):
    base = os.path.expanduser('~/Desktop/NOT')
    return os.path.join(base, sub)


def remove_duplicate(_files):
    for f in _files:
        old = f + '.txt'
        new = f + '_new.txt'
        read_data(old, new)


def read_data(old, new):
    one = []
    with codecs.open(old, 'r', 'utf-8') as reader:
        line = reader.readline()
        while line:
            if one.count(line) != 0:
                line = reader.readline()
                continue

            one.append(line)

    reader.close()

    write_data(one, new)


def write_data(data, file):
    with codecs.open(file, 'a', 'utf-8') as writer:
        for line in data:
            line = line.strip()
            line = '\"' + line + '\"' + " = " + '\"\"' + ';' + '\n'
            writer.write(line)

    writer.close()


if __name__ == '__main__':
    files = get_file()
    remove_duplicate(files)
