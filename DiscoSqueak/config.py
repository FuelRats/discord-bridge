import os
import logging
import configparser

from .exceptions import ConfigError

log = logging.getLogger(__name__)


class Config:
    def __init__(self, file_path):
        self.file_path = file_path

        if not os.path.isfile(self.file_path):
            log.error("Config file not found. Woops!")
            raise ConfigError(message="Config File Not Found")  # TODO add error info

        config = configparser.ConfigParser()
        config.read(file_path, encoding='utf-8')
        if {"bot"}.difference(config.sections()):
            raise ConfigError(message="Bot section is missing from config file.")

        self.log_level = config.get('bot', 'log_level', fallback=DefConfig.log_level)
        if not self.log_level:
            raise ConfigError('Option is null', 'log_level')

        self.discord_token = config.get('bot', 'discord_token', fallback=DefConfig.discord_token)
        if not self.discord_token:
            raise ConfigError('Option is null', 'discord_token')

        self.irc_server = config.get('bot', 'irc_server', fallback=DefConfig.irc_server)
        if not self.irc_server:
            raise ConfigError('Option is null', 'irc_server')

        self.irc_port = config.get('bot', 'irc_port', fallback=DefConfig.irc_port)
        if not self.irc_port:
            raise ConfigError('Option is null', 'irc_port')

        self.irc_useSSL = config.get('bot', 'irc_useSSL', fallback=DefConfig.irc_useSSL)
        if not self.irc_useSSL:
            raise ConfigError('Option is null', 'irc_useSSL')

        self.irc_nick = config.get('bot', 'irc_nick', fallback=DefConfig.irc_nick)
        if not self.irc_nick:
            raise ConfigError('Option is null', 'irc_nick')
        
        self.irc_IdentPW = config.get('bot', 'irc_IdentPW', fallback=DefConfig.irc_IdentPW)
        if not self.irc_IdentPW:
            raise ConfigError('Option is null', 'irc_IdentPW')

        self.irc_DebugChan = config.get('bot', 'irc_DebugChan', fallback=DefConfig.irc_DebugChan)
        if not self.irc_DebugChan:
            raise ConfigError('Option is null', 'irc_DebugChan')


class DefConfig:
    log_level = 'INFO'
    discord_token = None
    irc_server = 'irc.us.fuelrats.com'
    irc_port = 6697
    irc_useSSL = True
    irc_nick = 'Discord'
    irc_IdentPW = None
    irc_DebugChan = None
    file_path = 'conf/conf.ini'