import configparser
import os
import tempfile
import pathlib
import hashlib


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        cwd = pathlib.Path(__file__).parent.absolute()
        config_path = cwd.joinpath(r"config.ini")
        self.config.read(config_path)

    @staticmethod
    def get_temp_path(path=""):
        if path == "":
            return tempfile.gettempdir()
        return os.path.join(tempfile.gettempdir(), path)

    @staticmethod
    def get_work_dir_path(path=""):
        cwd = pathlib.Path(Config.extend_path(__file__)).parent.absolute()
        if path == "":
            return cwd
        return cwd.joinpath(path)

    @staticmethod
    def assert_dir_exists(dir_path):
        path = pathlib.Path(dir_path)
        path.mkdir(parents=True, exist_ok=True)
        return dir_path

    @staticmethod
    def get_versions_short_name(versions):
        return Config.get_short_name(list(map(lambda t: getattr((t.__dict__.get("version") or t), "_name"), versions)))

    @staticmethod
    def get_short_name(names):
        name = "_".join(sorted(list(map(lambda t: os.path.normpath(t).replace(".", '').replace(os.path.sep, '_'), names))))
        return hashlib.sha1(name.encode('utf-8')).hexdigest()

    @staticmethod
    def extend_path(path):
        if os.name == 'nt':
            return "\\\\?\\" + path
        return path

    # TODO make get_work_dir receive N arguments and join them together with the home repo
