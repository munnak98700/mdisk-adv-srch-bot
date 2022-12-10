from datetime import datetime
from configs import Config
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from TeamTeleRoid.database import db


@Client.on_message(filters.command("help") & filters.private)
async def help_handler(_, event: Message):
    await event.reply_text(Config.ABOUT_HELP_TEXT.format(event.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [
            InlineKeyboardButton('ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ', url=f'http://t.me/{Config.BOT_USERNAME}?startgroup=true')
            ],

             [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/Aksbackup"),
             InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="About_msg"),
             InlineKeyboardButton("ʜᴇʟᴘ", callback_data="Help_msg")
             ],[
             InlineKeyboardButton('ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ', url=f'http://t.me/{Config.BOT_USERNAME}?startgroup=true')     
        ])
    )                        

@Client.on_message(filters.command("total_users") & filters.private &  filters.chat(Config.BOT_OWNER))
async def total_users(_, event: Message):
    total_users = await db.total_users_count()
    msg = f"""
    Users: {total_users} users
    """
    await event.reply_text(msg)

@Client.on_message( filters.command("start") & filters.private)
async def start_handler(_,event: Message):
    await event.reply_photo(
        photo=Config.START_PHOTO,
        caption=Config.START_MSG.format(event.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [
            InlineKeyboardButton('ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ', url=f'http://t.me/{Config.BOT_USERNAME}?startgroup=true')
            ],

             [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/Aksbackup"),
             InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="About_msg"),
             InlineKeyboardButton("ʜᴇʟᴘ", callback_data="Help_msg")
             ],[
             InlineKeyboardButton('ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ', url=f'http://t.me/{Config.BOT_USERNAME}?startgroup=true')             
        ])
    )

VERIFY = {}
@Client.on_message(filters.command("request") & filters.group)
async def request_handler(c,m: Message):
    global VERIFY
    chat_id = m.chat.id
    user_id = m.from_user.id if m.from_user else None


    if VERIFY.get(str(chat_id)) == None: # Make Admin's ID List
        admin_list = []
        async for x in c.iter_chat_members(chat_id=chat_id, filter="administrators"):
            admin_id = x.user.id 
            admin_list.append(admin_id)
        admin_list.append(None)
        VERIFY[str(chat_id)] = admin_list

    if not user_id in VERIFY.get(str(chat_id)): # Checks if user is admin of the chat
        return

    group_id = m.chat.id
    group_info = await db.get_group(group_id)

    if not group_info["has_access"] or not await db.is_group_verified(group_id):
        REPLY_MARKUP = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('ʀᴇǫᴜᴇsᴛ ᴀᴄᴄᴇss', callback_data=f'request_access#{m.chat.id}#{m.from_user.id}'),
            ],

        ])

        return await m.reply_text(f"ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴍᴀʏ ɴᴏᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇss ᴛᴏ ᴀᴅᴅ ʏᴏᴜʀ ᴏᴡɴ ᴅʙ ᴄʜᴀɴɴᴇʟ ᴏʀ ᴍᴀʏ ʜᴀᴠᴇ ᴇxᴘɪʀᴇᴅ. ᴘʟᴇᴀsᴇ ʀᴇǫᴜᴇsᴛ ᴀᴄᴄᴇss ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴ" ,reply_markup=REPLY_MARKUP ,disable_web_page_preview=True)

    else:
        return await m.reply_text("ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀʟʀᴇᴀᴅʏ ʜᴀᴠᴇ ᴀᴄᴄᴇss ᴛᴏ /addb")


@Client.on_message(filters.command("addb") & filters.group)
async def addb_handler(c, m: Message):
    global VERIFY
    chat_id = m.chat.id
    user_id = m.from_user.id if m.from_user else None


    if VERIFY.get(str(chat_id)) == None: # Make Admin's ID List
        admin_list = []
        async for x in c.iter_chat_members(chat_id=chat_id, filter="administrators"):
            admin_id = x.user.id 
            admin_list.append(admin_id)
        admin_list.append(None)
        VERIFY[str(chat_id)] = admin_list

    if not user_id in VERIFY.get(str(chat_id)): # Checks if user is admin of the chat
        return

    group_id = m.chat.id
    group_info = await db.get_group(str(group_id))

    if group_info["has_access"] and await db.is_group_verified(group_id):
        if len(m.command) == 2:
            db_channel = m.command[1]


            try:
                invite_link =  await c.create_chat_invite_link(int(db_channel))
            except Exception as e:
                return await m.reply_text("Make sure you you have made the bot as admin in ur channel "+str(db_channel))
                

            REPLY_MARKUP = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('ᴀʟʟᴏᴡ ᴅʙ ᴄʜᴀɴɴᴇʟ', callback_data=f'dbgive_access#{group_id}#{m.from_user.id}#{db_channel}'),
            InlineKeyboardButton('ᴅᴇɴʏ', callback_data=f'dbdeny_access#{m.from_user.id}#{db_channel}'),
        ],
        [
            
            InlineKeyboardButton('ᴄʟᴏsᴇ', callback_data=f'delete'),
        ],

    ])      

            await c.send_message(Config.LOG_CHANNEL,  f"Join the channel and then alllow. \n\n#NewDBChannel\n\nDB Chnl Invite Link: {invite_link.invite_link}\nGroup:`{group_id}`\n\nNote: This group has been already has access", reply_markup=REPLY_MARKUP)
            return await m.reply_text("DB Channel added successfully. Wait for the admin to approve the channel. You will be notified", )
        else:
            return await m.reply_text("ᴍᴀᴋᴇ ᴛʜᴇ ʙᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ /addb -100xxx")
    else:
        return await m.reply_text("ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴅᴏᴇs ɴᴏᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇss ᴛᴏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴘʟᴇᴀsᴇ /request ᴀᴄᴄᴇss")
