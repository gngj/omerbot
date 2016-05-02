#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to send timed Telegram messages
# This program is dedicated to the public domain under the CC0 license.

"""
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

Done! Congratulations on your new bot. You will find it at telegram.me/OmerCountBot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands.

Use this token to access the HTTP API:
207443777:AAGuMP5nIJMqbFKILRmVuuAz8in7PfiWdjA

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
"""

from telegram.ext import Updater, CommandHandler
import logging

from convertdate import holidays
from datetime import date
# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)
job_queue = None


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi! Use /set <seconds> to '
                                                 'set a timer')


def set(bot, update):
    """ Adds a job to the queue """
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id,text=str((date.today() - holidays.passover()).days))
    return
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
                bot.sendMessage(chat_id, text='Sorry we can not go back to future!')
        def alarm(bot):
            """ Inner function to send the alarm message """
            bot.sendMessage(chat_id, text='Beep!')

        # Add job to queue
        job_queue.put(alarm, due, repeat=False)
        bot.sendMessage(chat_id, text='Timer successfully set!')

    except IndexError:
        bot.sendMessage(chat_id, text='Usage: /set <seconds>')
    except ValueError:
        bot.sendMessage(chat_id, text='Usage: /set <seconds>')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    global job_queue

    updater = Updater("207443777:AAGuMP5nIJMqbFKILRmVuuAz8in7PfiWdjA")
    job_queue = updater.job_queue

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", start))
    dp.addHandler(CommandHandler("set", set))

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    import time
    time.sleep(60 * 20)
    #updater.idle()

if __name__ == '__main__':
    main()
