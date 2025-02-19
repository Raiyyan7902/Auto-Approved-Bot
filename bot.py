from os import environ
from pyrogram import Client, filters
from pyrogram.types import Message, ChatJoinRequest

# Bot configuration
BOT_TOKEN = environ.get("BOT_TOKEN")
API_ID = int(environ["API_ID"])
API_HASH = environ["API_HASH"]
CHAT_ID = int(environ["CHAT_ID"])
APPROVED_WELCOME_TEXT = environ.get("APPROVED_WELCOME_TEXT", "Hello {mention}\nWelcome To {title}\n\nYour Auto Approved")
APPROVED_WELCOME = environ.get("APPROVED_WELCOME", "off").lower()
PRIVATE_CHANNEL_ID = int(environ.get("PRIVATE_CHANNEL_ID", CHAT_ID))
OWNER_ID = int(environ.get("OWNER_ID"))

# Initialize Client
pr0fess0r_99 = Client(
    "Auto Approved Bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

# Set of bot administrators
admins = set()

# Set of approved channels/groups
approved_channels = set()

@pr0fess0r_99.on_message(filters.private & filters.command("start"))
async def start(client: pr0fess0r_99, message: Message):
    await client.send_message(chat_id=message.chat.id, text="Welcome to the X Automatic Request Approval Bot. I am capable of automatically approving all new requests in channels and groups. To utilize my services, kindly add me to your channels or groups with the invite users via link permission. Please note that only bot administrators can use this bot.", disable_web_page_preview=True)

@pr0fess0r_99.on_chat_join_request((filters.group | filters.channel) & filters.chat(CHAT_ID) if CHAT_ID else (filters.group | filters.channel))
async def autoapprove(client: pr0fess0r_99, message: ChatJoinRequest):
    chat = message.chat
    user = message.from_user
    print(f"{user.first_name} Joined 🤝")
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    if APPROVED == "on":
        await client.send_message(chat_id=chat.id, text=APPROVED_WELCOME_TEXT.format(mention=user.mention, title=chat.title))
    await client.send_message(chat_id=PRIVATE_CHANNEL_ID, text=f"{user.first_name} joined {chat.title}")

@pr0fess0r_99.on_message(filters.private & filters.command("addadmin"))
async def add_admin(client: pr0fess0r_99, message: Message):
    if message.from_user.id != OWNER_ID:
        await client.send_message(chat_id=message.chat.id, text="Only the bot owner can use this command.")
        return
    try:
        user_id = int(message.text.split()[1])
        admins.add(user_id)
        await client.send_message(chat_id=message.chat.id, text=f"User with ID {user_id} has been added as an administrator.")
    except (IndexError, ValueError):
        await client.send_message(chat_id=message.chat.id, text="Invalid command usage.")

@pr0fess0r_99.on_message(filters.private & filters.command("addchannel"))
async def add_channel(client: pr0fess0r_99, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID and user_id not in admins:
        await client.send_message(chat_id=message.chat.id, text="Only the bot owner and administrators can use this command.")
        return
    try:
        chat_id = int(message.text.split()[1])
        approved_channels.add(chat_id)
        await client.send_message(chat_id=message.chat.id, text=f"Channel with ID {chat_id} has been added to the approved list.")
    except (IndexError, ValueError):
        await client.send_message(chat_id=message.chat.id, text="Invalid command usage.")

@pr0fess0r_99.on_message(filters.private & filters.command("addgroup"))
async def add_group(client: pr0fess0r_99, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID and user_id not in admins:
        await client.send_message(chat_id=message.chat.id, text="Only the bot owner and administrators can use this command.")
        return
    try:
        chat_id = int(message.text.split()[1])
        approved_channels.add(chat_id)
        await client.send_message(chat_id=message.chat.id, text=f"Group with ID {chat_id} has been added to the approved list.")
    except (IndexError, ValueError):
        await client.send_message(chat_id=message.chat.id, text="Invalid command usage.")

print("Auto Approved Bot")
pr0fess0r_99.run()
