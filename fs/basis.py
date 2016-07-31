#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'A remote file system abstraction implementation based on webhdfs api'

import json
import re
import requests


BASE_URL = 'http://172.18.231.84:50070/webhdfs/v1'


def upload_file(username, local_file, remote_url):
    """
    Upload a local file to hdfs.
    """
    url = BASE_URL + remote_url
    operation = 'CREATE'
    payload = {
        'op': operation,
        'user.name': username
    }
    files = {'file': open(local_file, 'rb')}
    response = requests.put(url, params=payload, files=files)

    result = None
    if response.headers['Content-Length'] != '0':
        data = json.loads(response.text)
        result = data['RemoteException']['exception']
    else:
        result = "Upload success"
    return result


def open_file(username, remote_url):
    """
    Return the content of a file.
    """
    url = BASE_URL + remote_url
    operation = 'OPEN'
    payload = {
        'op' : operation,
        'user.name' : username,
    }
    response = requests.get(url, params=payload)
    pattern = re.compile(r'[^\r\n]*\r\n')
    filter_text = pattern.sub("", response.text)
    return filter_text


def make_dir(username, remote_url):
    """
    Return true if directory is made or present already.
    """
    url = BASE_URL + remote_url
    operation = 'MKDIRS'
    payload = {
        'op': operation,
        'user.name': username,
    }
    response = requests.put(url, params=payload)

    data = json.loads(response.text)
    result = None
    if 'RemoteException' in data:
        result = data['RemoteException']['exception']
    else:
        result = "Create directory success"
    return result


def rename_object(username, remote_url, new_name):
    """
    Rename a file or directory in hdfs.
    """
    url = BASE_URL + remote_url
    operation = 'RENAME'
    payload = {
        'op': operation,
        'user.name': username,
        'destination': new_name
    }
    response = requests.put(url, params=payload)
    data = json.loads(response.text)
    result = None
    if data['boolean']:
        result = "success"
    else:
        result = "fail"
    return result


def delete_object(username, remote_url):
    """
    Delete a file or directory in hdfs.
    """
    url = BASE_URL + remote_url
    operation = 'DELETE'
    payload = {
        'op': operation,
        'user.name': username,
        'recursive': True
    }
    response = requests.delete(url, params=payload)
    data = json.loads(response.text)
    result = None
    if 'RemoteException' in data:
        result = data['RemoteException']['exception']
    else:
        result = "Remove object success"
    return result


def get_status(username, remote_url):
    """
    Return the detailed info of a file or directory.
    """
    url = BASE_URL + remote_url
    operation = 'GETFILESTATUS'
    payload = {
        'op': operation,
        'user.name': username
    }
    response = requests.get(url, params=payload)
    print(response.text)


def get_list(username, remote_url):
    """
    Get the file list of the url in hdfs.
    """
    operation = 'LISTSTATUS'
    url = BASE_URL + remote_url
    payload = {
        'op': operation,
        'user.name': username,
    }
    response = requests.get(url, params=payload)
    print(response.text)


def test():
    """
    Test above functions
    """
    user = 'vinzor'
    open_file(user, '/user/peter/test02')
    # get_status(user, '/user/vinzor/helloworld-new')
    # get_list(user, '/user/vinzor/')
    # rename_object(user, '/user/vinzor/helloworld', '/user/vinzor/helloworld-new')
    # delete_object(user, '/user/vinzor/input')
    # make_dir(user, '/user/vinzor/test1')
    # upload_file(user, './apps.py', '/user/vinzor/apps.py')


if __name__ == '__main__':
    test()
