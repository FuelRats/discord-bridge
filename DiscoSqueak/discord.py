import sys
import logging
import discord

from .config import Config
from .constants import VERSION as BOTVERSION

log = logging.getLogger('discord')


class DiscordBot(Client):
    def __init__(self, config: Config):
        self.config = config
        self.init = False

        self._setup_logs()

        super().__init__()
        self.http.user_agent += ' DiscoSqueak/%s' % BOTVERSION

    def _setup_log_handlers(self):
        if len(logging.getLogger(__name__).handlers) > 1:
            return

        chandler.setLevel(self.config.log_level)
        chandler = logging.StreamHandler(stream=sys.stdout)
        chandler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
        log.addHandler(chandler)

        fhandler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
        fhandler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        log.addHandler(fhandler)

    async def safe_send_message(self, dest, content):
        msg = None
        try:
            if content is not None:
                msg = await self.send_message(dest, content)
            else:
                log.warning("no")
        except discord.errors.Forbidden:
            log.warning("No permission to send messages to: {}".format(dest.name))
        except discord.errors.NotFound:
            log.warning("Cannot send message to {}, It might be invalid.".format(dest.name))
        except discord.errors.HTTPException:
            log.warning("Unable to send message, is it over character limit?")
        finally:
            log.debug("sent message with the return msg: {}".format(msg))

    def run(self):
        try:
            self.loop.run_until_complete(self.start(*self.config.discord_token))
        except discord.errors.LoginFailure:
            raise log.error("Unable to login to discord.")
        finally:
            try:
                self._cleanup()
            except Exception:
                log.error("Something went wrong ")

            self.loop.close()
            if self.exit_signal:
                raise self.exit_signal

    async def on_resumed(self):
        log.info("\nReconnected to discord.\n")

    async def on_ready(self):
        log.debug("Discord end, ready to go!")

        if self.init:
            log.debug("That shouldn't happen. Received extra on_ready event.")
            return

        log.info('Connected to Discord.')

        self.init = True

    async def on_server_join(self, server: discord.Server):
        log.info("Server {}: Bot joined".format(server.name))

    async def on_server_remove(self, server: discord.Server):
        log.info("Server {}: Bot removed".format(server.name))

    async def on_server_available(self, server: discord.Server):
        if not self.init:
            return
        log.debug("Server {}: is available.".format(server.name))

    async def on_server_unavailable(self, server: discord.Server):
        log.debug("Server {}: is unavailable.".format(server.name))
