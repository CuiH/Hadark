#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import os
"""
Currently, no permission control is included in this module.
"""

base_url = 'http://172.18.231.84:50070/webhdfs/v1'

def delete_uploaded_file(file_path):
    os.remove(file_path)

def upload_file(username, local_file, remote_url):
    """
    Upload a local file to hdfs.
    """
    url = base_url + remote_url
    payload = {
        'op': 'CREATE',
        'user.name': username
    }
    files = {'file': open(local_file, 'rb')}
    r = requests.put(url, params=payload, files=files)
    print(r.headers)
    print('---------------')
    print(r.text)


def open_file(username, remote_url):
    """
    Return the content of a file.
    """
    url = base_url + remote_url
    payload = {
        'op' : 'OPEN',
        'user.name' : username,
    }
    r = requests.get(url, params=payload)
    return r.text

def make_dir(username, remote_url):
    """
    Return true if directory is made or present already.
    """
    url = base_url + remote_url
    payload = {
        'op': 'MKDIRS',
        'user.name': username,
    }
    r = requests.put(url, params=payload)
    print(r.headers)
    print(r.text)

def rename_object(username, remote_url, new_name):
    """
    Rename a file or directory in hdfs.
    """
    url = base_url + remote_url
    payload = {
        'op': 'RENAME',
        'user.name': username,
        'destination': new_name
    }
    r = requests.put(url, params=payload)
    print(r.text)

def delete_object(username, remote_url):
    """
    Delete a file or directory in hdfs.
    """
    url = base_url + remote_url
    payload = {
        'op': 'DELETE',
        'user.name': username
    }
    r = requests.delete(url, params=payload)
    print(r.text)

def get_status(username, remote_url):
    """
    Return the detailed info of a file or directory.
    """
    url = base_url + remote_url
    payload = {
        'op': 'GETFILESTATUS',
        'user.name': username
    }
    r = requests.get(url, params=payload)
    print(r.text)

def get_list(username, remote_url):
    """
    Get the file list of the url in hdfs.
    """
    op = 'LISTSTATUS'
    url = base_url + remote_url
    payload = {
        'op': 'LISTSTATUS',
        'user.name': username,
    }
    r = requests.get(url, params=payload)
    print(r.text)

def test():
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


