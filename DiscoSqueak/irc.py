import sys
import ssl
import irc.client

from .config import Config


class IrcClient(irc.client.SimpleIRCClient):
    def __init__(self, config: Config):
        self.config = config
        self.debug_chan = config.irc_DebugChan
        super().__init__()

    def on_welcome(self, connection, event):
        if self.debug_chan is not None:
            if irc.client.is_channel(self.debug_chan):
                connection.join(self.debug_chan)
                self.connection.privmsg(self.debug_chan, 'This is now my debug output channel while in debug mode. '
                                                         'If this is incorrect, Kick me!')
