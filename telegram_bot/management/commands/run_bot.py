from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram_bot import commands_handlers


class Command(BaseCommand):
    help = "Start telegram bot polling process"

    commands = [
        ("start", commands_handlers.start),
        ("astronomy_show", commands_handlers.astronomy_show),
        ("show_time", commands_handlers.show_time),
        ("theme_show", commands_handlers.theme_show),
    ]

    def __init__(self, *args, **kwargs):

        self.updater = Updater(settings.TELEGRAM_TOKEN)
        self.dispatcher = self.updater.dispatcher

        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        # parser.add_argument('sample', nargs='+')
        pass

    def handle(self, *args, **options):
        self.register_commands()

        bot_name = self.updater.bot.get_me()["username"]

        self.stdout.write(self.style.NOTICE(
            f"You can find me by name *{bot_name}* Hello!!!Ready to serve")
        )
        self.updater.start_polling()
        self.updater.idle()

    def register_commands(self):
        for cmd, handler in self.commands:
            self.dispatcher.add_handler(CommandHandler(cmd, handler))
