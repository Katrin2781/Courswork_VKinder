import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
bottoken = config["Tokens"]["vk_group"]
perstoken = config["Tokens"]["vk_pers"]
user_db = config['access_DB']['user']
password_db = config['access_DB']['password']