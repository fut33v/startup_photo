import json
import os
from functools import partial
import vk_auth
import getpass


def load_configs(filename):
    if os.path.exists(filename):
        configs = open(filename).read()
        configs = json.loads(configs)
        return configs
    return None


json_pretty_dumps = partial(
    json.dumps,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
)


def save_configs(filename, configs):
    json_txt = json_pretty_dumps(configs)
    json_f = open(filename, 'w')
    json_f.write(json_txt)
    json_f.close()


def which(program):
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        return True
    else:
        return False


CLIENT_ID = "4599874"
ALBUM_TITLE = "vk-commits"
ALBUM_DESCRIPTION = (
    "Photos taken on committing, uploaded by vk-commits script"
)
ENTER_DEFAULT = "press ENTER for using default"


def no_configs(configs_filename):
    configs = {}

    print "Vkontakte authorization:"
    email = raw_input("E-mail: ")
    password = getpass.getpass("Password: ")

    album_title = raw_input("album title: ")
    if album_title == "":
        print "using default album title:", ALBUM_TITLE
        album_title = ALBUM_TITLE

    album_desc = raw_input("album description: ")
    if album_desc == "":
        print "using default album desc:", ALBUM_DESCRIPTION
        album_desc = ALBUM_DESCRIPTION

    client_id = raw_input(
        "client id (application id), " +
        ENTER_DEFAULT +
        "(" + CLIENT_ID + ")"
    )
    if not (client_id.isdigit() and client_id != ""):
        print "using default client id:", CLIENT_ID
        client_id = CLIENT_ID

    token, user_id = vk_auth.auth(
        email,
        password,
        client_id,
        "photos,offline"
    )

    configs['album_title'] = album_title
    configs['album_desc'] = album_desc
    configs['client_id'] = client_id
    configs['token'] = token
    configs['user_id'] = user_id
    save_configs(configs_filename, configs)
    return configs
