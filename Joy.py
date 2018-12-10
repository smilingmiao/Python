"""不要在这里执行，不要在这里执行，不要在这里执行"""

import os


def rename_batch_files(cwd, old_ext, new_ext):
    src_dir = os.listdir(cwd)
    for i in src_dir:
        if os.path.isdir(i):
            cur_path = os.path.join(cwd, i)
            rename_batch_files(cur_path, old_ext, new_ext)
        else:
            filename = os.path.basename(i)
            filename_split = filename.split(i)
            fname = filename_split[0]
            ext = filename_split[1]

            if ext == old_ext:
                new_file = filename[0] + new_ext
                os.rename(os.path.join(cwd, i),
                          os.path.join(cwd, new_file))



if __name__ == '__main__':
    path = os.getcwd()
    rename_batch_files(path, 'png', 'jpg')