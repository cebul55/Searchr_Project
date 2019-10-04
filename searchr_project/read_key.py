def read_secret_key():
    secret_key = read_any_key('conf/secret.key', '../conf/secret.key', 'secret.key')
    return secret_key


def read_db_key():
    secret_key = read_any_key('conf/searchrDB.key', '../conf/searchrDB.key', 'searchrDB.key')
    return secret_key


def read_bing_key():
    secret_key = read_any_key('conf/bing.key', '../conf/bing.key', 'searchrDB.key')
    return secret_key


def read_any_key(path1, path2, key_name):
    secret_key = None
    try:
        with open(path1, 'r') as f:
            secret_key = f.readline().strip()
    except:
        try:
            with open(path2, 'r') as f:
                secret_key = f.readline().strip()
        except:
            raise IOError(key_name + ' file not found')

    if not secret_key:
        raise KeyError(key_name + ' not found')

    return secret_key