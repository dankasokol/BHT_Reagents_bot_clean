from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from inventory import search_reagents, format_reagent
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import MessageHandler, filters

import os

TOKEN = os.getenv("BOT_TOKEN")

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🔍 Найти реагент")],

        [KeyboardButton("❓ Помощь")],
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-склад БХТ! Подчиняюсь вам и Наталии Вадимовне! 🧪\nВыбери действие на клавиатуре:",
        reply_markup=MAIN_KEYBOARD
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "🔍 Найти реагент":
        context.user_data["mode"] = "search"
        await update.message.reply_text("Введите название или формулу реагента:")
        return

    if text == "❓ Помощь":
        context.user_data["mode"] = None
        await update.message.reply_text(
            "Команды:\n"
            "🔍 Найти реагент — поиск по таблице\n"
            "📦 Показать всё — список всех реагентов\n"
            "❓ Помощь — это сообщение"
        )
        return

    # ====== РЕЖИМ ПОИСКА (бесконечный) ======
    if context.user_data.get("mode") == "search":
        query = text

        from inventory import search_reagents, format_reagent
        results = search_reagents(query)

        if results.empty:
            await update.message.reply_text("❌ Ничего не найдено. Введите другое название:")
            return

        msgs = [format_reagent(row) for _, row in results.iterrows()]
        reply = "\n\n——————————\n\n".join(msgs)

        await update.message.reply_html(reply)

        # ВАЖНО:
        # НЕ ВЫХОДИМ ИЗ РЕЖИМА ПОИСКА!
        await update.message.reply_text("Введите следующий реагент:")
        return

    # ====== ЕСЛИ ТЕКСТ НЕ РАСПОЗНАН ======
    await update.message.reply_text("Не понимаю. Нажмите кнопку или /start.")



async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Использование: /find <название или формула>")
        return

    query = " ".join(context.args)
    results = search_reagents(query)

    if results.empty:
        await update.message.reply_text("❌Ничего не найдено.")
        return

    msgs = [format_reagent(row) for _, row in results.iterrows()]
    reply = "\n\n——————————\n\n".join(msgs)

    await update.message.reply_html(reply)  # html позволяет жирный текст / emoji

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("find", find_command))

    # ОБРАБОТКА КНОПОК
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    print("Бот запущен.")
    app.run_polling(stop_signals=None)

if __name__ == "__main__":
    main()




