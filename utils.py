import os
import gzip
import shutil
import datetime

def scan_directory(dirname):
    files = []
    for filename in os.listdir(dirname):
        files.append(os.path.join(dirname, filename))
    return files

def compress_file(filename):
    with open(filename, 'rb') as f_in, \
            gzip.open(filename + '.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def decompress_file(filename):
    with gzip.open(filename, "rb") as file, \
            open(filename[:-3], 'wb') as nfile:
        data = file.read()
        nfile.write(data)


def removeFile(file_name):
    os.remove(file_name)

def timestamp():
    return '{:%Y-%m-%d %H:%M:%S} | '.format(datetime.datetime.now())

def create_file(filename, content, wmode='w'):
    try:
        with open(filename, wmode) as file:
            file.write(content)
    except Exception as e:
        return "Error :", e
    return True

def read_file(filename, rmode='r'):
    try:
        with open(filename, rmode) as file:
            content = file.read()
    except Exception as e:
        return "Error :", e
    return content
