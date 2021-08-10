from pathlib import Path

def read_config():
    config = {}
    config_keys = ["token", "mysql_server", "mysql_db", "mysql_user", "mysql_password", "mysql_charset"]
    config_path = str(Path.home()) + "/.tusync_credentials"
    with open(config_path, "r") as f:
        for line in f.readlines():
            [k, v] = line.split('=')
            if k in config_keys:
                config[k] = v.rstrip()
        f.close()

    return config
