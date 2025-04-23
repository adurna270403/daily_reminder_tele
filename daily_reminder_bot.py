from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import os
import pytz

current_timezone = pytz.timezone("Asia/Ho_Chi_Minh")

load_dotenv()
TOKEN = os.getenv("TELEBOT1")


book = [
    "Chương 1: Ngày xưa có một chàng chăn cừu...",
    "Chàng trai đó hay mơ về kho báu...",
    "Một hôm, anh quyết định bắt đầu cuộc hành trình..."
]

user_state = {}

async def daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    # Gửi thông điệp nhắc nhở vào mỗi ngày
    for user_id in context.bot_data['user_ids']:  # Giả sử bạn lưu các user_id ở đây
        await context.bot.send_message(user_id, "ĐM m đọc sách nhanh lên!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    context.user_data[user_id] = 0
    await update.message.reply_text("📚 Chào mừng đến với Bot Đọc Sách!\nGõ /next để bắt đầu đọc.")

async def next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    index = context.user_data.get(user_id, 0)  
    
    if index >= len(book): 
        await update.message.reply_text("🎉 Bạn đã đọc hết sách rồi!")
    else:
        await update.message.reply_text(f"📖 {book[index]}")
        context.user_data[user_id] = index + 1


app = ApplicationBuilder().token(TOKEN).build()

scheduler = AsyncIOScheduler()

# Thiết lập nhắc nhở hàng ngày lúc 8:00 sáng
scheduler.add_job(daily_reminder, CronTrigger(hour=8, minute=0, timezone= current_timezone), kwargs={'context': app.bot_data} )

# Bắt đầu scheduler
scheduler.start()


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("next", next))

if __name__ == '__main__':
    app.run_polling()
