# Note for Visual Studio: After adding CONFIG_MODE to the environment, need to close and restart Visual Studio for setting to take effect

config_dict = {'DEFAULT' : 'gatekeeper_config.Config', 
               'DEBUG'   : 'gatekeeper_config.DevelopmentConfig',
               'TEST'    : 'gatekeeper_config.TestingConfig'
               }

class Config(object):
    ERROR_404_HELP = False
    PROPAGATE_EXCEPTIONS = True
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True