from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

async def get_fsub_btn(client):
    invite_link = await client.export_chat_invite_link(Config.FSUB)
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Join Channel", url=invite_link)],
         [InlineKeyboardButton("Try Again", callback_data="check_sub")]]
    )

@Client.on_message(filters.incoming & filters.private, group=-1)
async def fsub_check(client, message):
    if not Config.FSUB:
        return

    if message.text and message.text.startswith("/start"):
        return

    try:
        user = await client.get_chat_member(Config.FSUB, message.from_user.id)
        if user.status == "kicked":
            await message.reply_text("You are banned from our channel. Contact support.")
            message.stop_propagation()
    except UserNotParticipant:
        btn = await get_fsub_btn(client)
        await message.reply_text(
            f"You must join our channel to use this bot!",
            reply_markup=btn
        )
        message.stop_propagation()
    except Exception as e:
        print(f"FSub Error: {e}")

@Client.on_callback_query(filters.regex("check_sub"))
async def check_sub(client, query):
    try:
        user = await client.get_chat_member(Config.FSUB, query.from_user.id)
        await query.message.delete()
        await query.message.reply_text("Thank you for joining! Now you can use the bot.")
    except UserNotParticipant:
        await query.answer("You haven't joined yet!", show_alert=True)
    except Exception as e:
        await query.answer(f"Error: {e}")

@Client.on_chat_join_request()
async def join_request(client, request):
    # This handles "Request to Join" feature
    # In some bots, they auto-approve or just track it
    # Branding: Botskingdoms
    await client.approve_chat_join_request(request.chat.id, request.from_user.id)
    try:
        await client.send_message(request.from_user.id, f"Welcome to our channel! Your join request to {request.chat.title} has been approved.")
    except:
        pass
