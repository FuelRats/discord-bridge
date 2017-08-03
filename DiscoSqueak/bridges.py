import configparser

from exceptions import ConfigError

log = logging.getLogger(__name__)


class DefBridge:
    file_path = 'conf/bridges.ini'

    DiscordChannel = None
    IrcChannel = None

    IrcCommandPrefixes = set()
    DiscordCommandPrefixes = set()

    IrcIgnoredNicks = set()
    DiscordIgnoredUsers = set()


class BridgeConfig:
    def __init__(self, bridge_name, bridge_config):
        self.name = bridge_name

        self.DiscordChannel = bridge_config.get('DiscordChannel', fallback=DefBridge.DiscordChannel)
        self.IrcChannel = bridge_config.get('IrcChannel', fallback=DefBridge.IrcChannel)
        self.IrcCommandPrefixes = bridge_config.get('IrcCommandPrefixes', fallback=DefBridge.IrcCommandPrefixes)
        self.DiscordCommandPrefixes = bridge_config.get('DiscordCommandPrefixes', fallback=DefBridge.DiscordCommandPrefixes)
        self.IrcIgnoredNicks = bridge_config.get('IrcIgnoredNicks', fallback=DefBridge.IrcIgnoredNicks)
        self.DiscordIgnoredUsers = bridge_config.get('DiscordIgnoredUsers', fallback=DefBridge.DiscordIgnoredUsers)


class Bridges:
    def __init__(self, file_path):
        self.file_path = file_path
        if self.file_path is None:
            self.file_path = DefBridge.file_path
        self.bridge_file = configparser.ConfigParser()

        if not self.bridge_file.read(self.file_path, encoding=utf-8):
            log.error('bridges file cannot be found.')
            raise ConfigError('bridges file was not found.')

        self.bridges = set()

        for section in self.config.sections():
            self.bridges.add(BridgeConfig)
