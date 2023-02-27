#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Telegram bot to play UNO in group chats
# Copyright (c) 2016 Jannes Höke <uno@jhoeke.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from telegram import ParseMode, Update
from telegram.ext import CommandHandler, CallbackContext

from user_setting import UserSetting
from utils import send_async
from shared_vars import dispatcher
from internationalization import _, user_locale

@user_locale
def help_handler(update: Update, context: CallbackContext):
    """Handler for the /help command"""
    help_text = _("👋🏻 HALO AKU ADALAH UNO GAME BOT 🤖\n"
      " Jika ingin memainkan Bot ini silahkan ikuti langkah dibawah ini :\n\n"
      "1. Tambahkan bot ini ke grup\n"
      "2. Di grup, mulai permainan baru dengan /new\n"
      "3. Untuk bergabung ke lobi, klik : /join\n"
      "4. Setelah setidaknya dua pemain bergabung, mulailah permainan dengan menekan /start \n\n"
      "📑 Perintah Lainnya :\n\n"
      " /Leave : Untuk meninggalkan permainan\n"
      " /skip  : untuk melewati pemain lain\n"
      " /settings : Untuk Melihat pengaturan group\n\n"
      "📚 Perintah lainnya (Hanya untuk pembuat game):\n\n"
      "/close : Tutup lobi\n"
      "/open : Buka lobi\n"
      "/kill : Hentikan permainan\n"
      "/kick : Pilih pemain untuk ditendang\n"
      "/enable_translations : Terjemahkan teks yang relevan ke semua\n"
      "/disable_translations - Gunakan bahasa Inggris untuk teks tersebut\n\n"
      "👨‍💻 About : \n"
      "<a href=\"https://t.me/rexaprivateroom\">👥 update group</a>\n"
      "<a href=\"https://t.me/tirexgugel\">🚀 update channel</a>\n"
      "<a href=\"https://t.me/JustRex\">👨‍💻 Owner</a>\n\n"
      " Selamat Bermain :).")

    send_async(context.bot, update.message.chat_id, text=help_text,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)

@user_locale
def modes(update: Update, context: CallbackContext):
    """Handler for the /help command"""
    modes_explanation = _("This UNO bot has four game modes: Classic, Sanic, Wild and Text.\n\n"
      " 🎻 The Classic mode uses the conventional UNO deck and there is no auto skip.\n"
      " 🚀 The Sanic mode uses the conventional UNO deck and the bot automatically skips a player if he/she takes too long to play its turn\n"
      " 🐉 The Wild mode uses a deck with more special cards, less number variety and no auto skip.\n"
      " ✍️ The Text mode uses the conventional UNO deck but instead of stickers it uses the text.\n\n"
      "To change the game mode, the GAME CREATOR has to type the bot nickname and a space, "
      "just like when playing a card, and all gamemode options should appear.")
    send_async(context.bot, update.message.chat_id, text=modes_explanation,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)

@user_locale
def source(update: Update, context: CallbackContext):
    """Handler for the /help command"""
    source_text = _("Bot ini adalah Hasil Kang dari Mau Mau uno bot saya hanya merubah sedikit tampilan. "
      "Kode tersedia di sini: \n"
      "https://github.com/jh0ker/mau_mau_bot")
    attributions = _("Attributions:\n"
      'Draw icon by '
      '<a href="http://www.faithtoken.com/">Faithtoken</a>\n'
      'Pass icon by '
      '<a href="http://delapouite.com/">Delapouite</a>\n'
      "Asli tersedia di http://game-icons.net\n"
      "Ikon diedit oleh ɳick")

    send_async(context.bot, update.message.chat_id, text=source_text + '\n' +
                                                 attributions,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@user_locale
def news(update: Update, context: CallbackContext):
    """Handler for the /news command"""
    send_async(context.bot, update.message.chat_id,
               text=_("All news here: https://telegram.me/unobotupdates"),
               disable_web_page_preview=True)


@user_locale
def stats(update: Update, context: CallbackContext):
    user = update.message.from_user
    us = UserSetting.get(id=user.id)
    if not us or not us.stats:
        send_async(context.bot, update.message.chat_id,
                   text=_("You did not enable statistics. Use /settings in "
                          "a private chat with the bot to enable them."))
    else:
        stats_text = list()

        n = us.games_played
        stats_text.append(
            _("{number} game played",
              "{number} games played",
              n).format(number=n)
        )

        n = us.first_places
        m = round((us.first_places / us.games_played) * 100) if us.games_played else 0
        stats_text.append(
            _("{number} first place ({percent}%)",
              "{number} first places ({percent}%)",
              n).format(number=n, percent=m)
        )

        n = us.cards_played
        stats_text.append(
            _("{number} card played",
              "{number} cards played",
              n).format(number=n)
        )

        send_async(context.bot, update.message.chat_id,
                   text='\n'.join(stats_text))


def register():
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(CommandHandler('source', source))
    dispatcher.add_handler(CommandHandler('news', news))
    dispatcher.add_handler(CommandHandler('stats', stats))
    dispatcher.add_handler(CommandHandler('modes', modes))
