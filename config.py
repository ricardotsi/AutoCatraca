from configparser import ConfigParser


def config_parser(section):
    """read params based on section"""
    parser = ConfigParser()
    # read file
    parser.read('/home/ricardo/Documentos/AutoCatraca/config.ini')
    # get params from file section and add to config
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, 'config.ini'))
    return config


def postgres(section='postgresql'):
    """Read config.ini and retrieve connection params"""
    return config_parser(section)


def catraca(section='catraca'):
    """Read config.ini and retrieve catraca params"""
    return config_parser(section)
