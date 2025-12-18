import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3

# ===== CONFIG =====
TOKEN = "8294830242:AAFx5i9JAkzOh7d5xu4JcGiEyDG7pF9kYfk"
ADMIN_ID = 6888317721
MIN_DEPOSIT = 140

# ===== LOGGING =====
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ===== DATABASE =====
conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0
)
""")

conn.commit()

# ===== KEYBOARDS =====
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(
    KeyboardButton("💰 Balance"),
    KeyboardButton("💳 Deposit")
)
main_kb.add(
    KeyboardButton("🌐 Buy Proxy"),
    KeyboardButton("❓ Help")
)

deposit_kb = ReplyKeyboardMarkup(resize_keyboard=True)
deposit_kb.add(
    KeyboardButton("💳 Bkash (৳)")
)
deposit_kb.add(
    KeyboardButton("❌ Cancel Deposit")
)

# ===== START =====
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (message.from_user.id,))
    conn.commit()

    await message.answer(
        "🎉 Welcome to Proxy Store Bot!\n\n"
        "এখানে তুমি:\n"
        "💰 Balance দেখতে পারো\n"
        "💳 Deposit করতে পারো\n"
        "🌐 Proxy কিনতে পারো\n\n"
        "নিচের মেনু ব্যবহার করো 👇",
        reply_markup=main_kb
    )

# ===== BALANCE =====
@dp.message_handler(lambda m: m.text == "💰 Balance")
async def balance(message: types.Message):
    cur.execute("SELECT balance FROM users WHERE user_id=?", (message.from_user.id,))
    bal = cur.fetchone()[0]
    await message.answer(f"💰 Your balance: {bal}৳")

# ===== DEPOSIT =====
@dp.message_handler(lambda m: m.text == "💳 Deposit")
async def deposit(message: types.Message):
    await message.answer(
        "💳 Welcome to Deposit Gateway\n\n"
        "📌 bKash Personal:\n"
        "01314519073\n\n"
        "⚠️ Fake request করলে BAN করা হবে\n\n"
        "👉 Deposit method সিলেক্ট করো:",
        reply_markup=deposit_kb
    )

@dp.message_handler(lambda m: m.text == "💳 Bkash (৳)")
async def bkash(message: types.Message):
    await message.answer(
        f"💳 bKash Deposit\n\n"
        f"🔻 Minimum deposit: {MIN_DEPOSIT}৳\n\n"
        "👉 টাকা পাঠিয়ে নিচের তথ্য পাঠাও:\n"
        "1️⃣ Amount\n"
        "2️⃣ Transaction ID\n"
        "3️⃣ Screenshot"
    )

# ===== ADMIN APPROVE =====
@dp.message_handler(commands=["approve"])
async def approve(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        _, user_id, amount = message.text.split()
        user_id = int(user_id)
        amount = int(amount)

        cur.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (amount, user_id))
        conn.commit()

        await bot.send_message(user_id, f"✅ Deposit approved!\n💰 Balance added: {amount}৳")
        await message.answer("✔️ Approved successfully")

    except:
        await message.answer("❌ Format: /approve user_id amount")

# ===== HELP =====
@dp.message_handler(lambda m: m.text == "❓ Help")
async def help_cmd(message: types.Message):
    await message.answer("📞 Support: @YourSupportID")

# ===== RUN =====
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
