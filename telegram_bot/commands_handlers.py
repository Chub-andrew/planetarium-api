import telegram
from telegram import Update, ParseMode
from telegram.ext import CommandHandler, CallbackContext, Updater
from telegram.utils.helpers import escape_markdown
from planetarium_api.models import AstronomyShow, ShowSession, ShowTheme


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    print(f"Hello, {user}!!!")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, "
                                               "please talk to me! "
                                               "My commands:\n /astronomy_show"
                                               " \n /show_time \n /theme_show"
    )


def astronomy_show(update: Update, context: CallbackContext):
    astronomy_shows = AstronomyShow.objects.all()
    if astronomy_shows.exists():
        message = ""
        for show in astronomy_shows:
            message += (f"*{escape_markdown(show.title, version=2)}*\n"
                        f"{escape_markdown(show.description, version=2)}\n\n")

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No astronomy shows available at the moment.",
            parse_mode=ParseMode.MARKDOWN_V2
        )


def show_time(update: Update, context: CallbackContext):
    time_show = ShowSession.objects.all()
    if time_show.exists():
        message = ""
        for show in time_show:
            show_title = escape_markdown(show.astronomy_show.title, version=2)
            dome_name = escape_markdown(show.planetarium_dome.name, version=2)
            show_time_str = escape_markdown(show.show_time.strftime(
                '%Y-%m-%d %H:%M:%S'), version=2)
            message += (f"*{show_title}*\nDome: {dome_name}\nTime: "
                        f"{show_time_str}\n\n")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No sessions available at the moment.",
            parse_mode=ParseMode.MARKDOWN_V2
        )


def theme_show(update: Update, context: CallbackContext):
    theme_sh = ShowTheme.objects.all()
    if theme_sh.exists():
        message = "Theme of shows:\n\n"
        for show in theme_sh:
            theme = escape_markdown(show.name, version=2)
            message += f"*`*{theme}`*\n\n"

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No theme shows available at the moment.",
            parse_mode=ParseMode.MARKDOWN_V2
        )
