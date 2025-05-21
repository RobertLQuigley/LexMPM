import json
import secrets


class Configuration(object):
    _filename: str
    dbhost: str
    dbport: int
    dbname: str
    dbpasword: str
    dbuser: str
    dbpassword: str
    dbuser: str
    secret_key: str
    access_token_expires: int

    def __init__(self):
        self._filename = ""
        self.dbhost = ""
        self.dbport = 0
        self.dbname = ""
        self.dbpassword = ""
        self.dbuser = ""
        self.secret = ""
        self.access_token_expires = 0

    @classmethod
    def default(cls: 'Configuration') -> 'Configuration':
        conf = Configuration()
        conf._filename = "lexmpmapi.json"
        conf.dbhost = "localhost"
        conf.dbport = 5432
        conf.dbname = "lexmpm"
        conf.dbuser = "postgres"
        conf.dbpassword = "<PASSWORD>"
        conf.secret_key = secrets.token_hex(32)
        conf.access_token_expires = 30
        return conf

    @classmethod
    def from_file(cls: 'Configuration', filename:str) -> 'Configuration':
        conf = Configuration()
        conf._filename = filename
        conf._parse()
        return conf

    def _parse(self):
        with open(self._filename) as json_file:
            json_data = json.load(json_file)
            self.dbhost = json_data["dbhost"]
            self.dbport = json_data["dbport"]
            self.dbname = json_data["dbname"]
            self.dbuser = json_data["dbuser"]
            self.dbpassword = json_data["dbpassword"]
            self.secret_key = json_data["secret_key"]
            self.access_token_expires = json_data["access_token_expires"]

    def write(self):
        with open(self._filename, "w", encoding='utf-8') as json_file:
            json.dump(self, json_file, ensure_ascii=False, indent=4,default=vars)
