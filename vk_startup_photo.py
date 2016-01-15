#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import urllib2
from urllib import urlencode
import os
import requests
from datetime import datetime
from os.path import expanduser
from os.path import exists

from vk_common import which


API_VERSION = 5.25


def call_api(method, params, token):
    params.append(("access_token", token))
    params.append(("v", API_VERSION))
    url = "https://api.vk.com/method/%s?%s" % (method, urlencode(params))
    response = urllib2.urlopen(url).read()
    if 'response' in response:
        return json.loads(response)['response']
    else:
        print response


def upload_photo(album_id, filename, description, token):
    upload = call_api(
        'photos.getUploadServer',
        [
            ('album_id', album_id)
        ],
        token
    )
    upload_url = upload['upload_url']
    files = {'file1': (filename, open(filename, 'rb'))}
    res = requests.post(upload_url, files=files)
    res = json.loads(res.text)
    photos_list = res['photos_list']
    server = res['server']
    hash_ = res['hash']
    upload = call_api(
        'photos.save',
        [
            ('album_id', album_id),
            ('photos_list', photos_list),
            ('server', server),
            ('hash', hash_),
            ('caption', description)
        ],
        token
    )


SECRETS_FILENAME = "secrets"


if __name__ == "__main__":

    if not exists(SECRETS_FILENAME):
        print "there is no file " + SECRETS_FILENAME + " with token and shit"
        exit(-1)

    secrets = open(SECRETS_FILENAME).readlines()
    if len(secrets) < 3:
        print "not much data so wow"
        exit(-1)

    ALBUM_ID = secrets[0][:-1]
    token = secrets[1][:-1]
    user_id = secrets[2][:-1]

    home = expanduser("~") + "/"
    PHOTOS_DIR = home + ".startphotos/"
    if not os.path.exists(PHOTOS_DIR):
        os.makedirs(PHOTOS_DIR)

    now = datetime.now()
    now = now.strftime('%d_%m_%Y__%H_%M_%S')
    filename = PHOTOS_DIR + now + ".jpg"

    if which('fswebcam') is None:
        print (
            "seems like fswebcam is not installed," +
            "on debian/ubuntu you can run sudo apt-get install fswebcam" +
            "for fixing the problem"
        )
    else:
        os.system('fswebcam -r 640x480 ' + filename)

    upload_photo(ALBUM_ID, filename, now, token)
