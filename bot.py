import logging
import json
import requests
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN', "8173036082:AAHlrHaHnaXKNbQl7v3wm-y0djPP6ezFEV0")
DEVELOPER_NAME = "@h4ck3rspybot"
DEVELOPER_CHANNEL = "@h4ck3rspybot"

# Your Channels
CHANNELS = [
    {"name": "📢 Official Channel", "link": "https://t.me/Sumit_X_Developer", "id": "@Sumit_X_Developer"},
    {"name": "📚 Rose X Files", "link": "https://t.me/Owner_By_Sumit", "id": "@Owner_By_Sumit"},
    {"name": "🔐 Premium Files", "link": "https://t.me/ROSE_X_FILE", "id": "@ROSE_X_FILE"},
    {"name": "👨‍💻 Developer", "link": "https://t.me/Sumit_X_Developer", "id": "@Sumit_X_Developer"}
]

# Welcome Photo
WELCOME_PHOTO = "https://i.ibb.co/NnsHbxb8/Ag-ACAg-UAAxk-BAAM-a-O-ks-Wahgns5-Fdol-Wl-UL01pz-HMAAp-QMaxt-Dm3l-XDLx-Jye-W1hp8-BAAMCAAN5-AAM2-BA.jpg"

# Your Bot Link
YOUR_BOT_LINK = "https://t.me/Adhar_info100_bot?start=8242490858"

# APIs
VEHICLE_API_1 = "https://vehicle-info-api-five.vercel.app/vehicle={}"
VEHICLE_API_2 = "https://vehicle-5-api.vercel.app/vehicle_info?vehicle_no={}"
MOBILE_API_1 = "https://yahu.site/api/?number={}&key=The_ajay"
MOBILE_API_2 = "https://api.x10.network/numapi.php?action=api&key=thakurji&number={}"

def format_phone_number(number):
    if len(number) == 10:
        return f"+91 {number[:5]} {number[5:]}"
    return number

def is_vehicle_number(text):
    text = text.strip().upper().replace(" ", "")
    if 9 <= len(text) <= 11:
        if text[:2].isalpha():
            if text[2:4].isdigit():
                if any(c.isalpha() for c in text[4:7]):
                    return True
    return False

def check_subscription(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id
        for channel in CHANNELS:
            try:
                chat_member = context.bot.get_chat_member(chat_id=channel["id"], user_id=user_id)
                if chat_member.status in ['left', 'kicked']:
                    return False
            except:
                return False
        return True
    except:
        return False

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    is_subscribed = check_subscription(update, context)
    
    if not is_subscribed:
        keyboard = []
        for channel in CHANNELS:
            keyboard.append([InlineKeyboardButton(channel["name"], url=channel["link"])])
        keyboard.append([InlineKeyboardButton("✅ I Have Joined All", url=YOUR_BOT_LINK)])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_photo(
            photo=WELCOME_PHOTO,
            caption=f"👋 **Welcome to Dual Information Bot**\n\n📱 **Mobile Info** + 🚗 **Vehicle Info**\n\n🔒 **Join all channels first:**\n\n1️⃣ {CHANNELS[0]['name']}\n2️⃣ {CHANNELS[1]['name']}\n3️⃣ {CHANNELS[2]['name']}\n4️⃣ {CHANNELS[3]['name']}\n\n📢 **After joining, click below**\n\n👨‍💻 **Developer:** {DEVELOPER_NAME}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("📱 Mobile Info", callback_data='mobile_info')],
        [InlineKeyboardButton("🚗 Vehicle Info", callback_data='vehicle_info')],
        [InlineKeyboardButton("ℹ️ Help", callback_data='help')],
        [InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{DEVELOPER_NAME[1:]}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "🤖 **Dual Information Bot**\n\n📌 *I can fetch information from two sources:*\n\n📱 **Mobile Database** - Get complete mobile number details\n🚗 **Vehicle Database** - Get complete vehicle RC details\n\n🔍 **How to use:**\n• For Mobile: Send any 10-digit Indian number\n• For Vehicle: Send vehicle number (e.g., UP26R4005)\n\n📊 *Powered by dual APIs*\n\n✅ **Subscription Verified**",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def help_command(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📱 Mobile Examples", callback_data='mobile_examples')],
        [InlineKeyboardButton("🚗 Vehicle Examples", callback_data='vehicle_examples')],
        [InlineKeyboardButton("🔙 Back to Main", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        f"🆘 **Help Guide**\n\n**📱 MOBILE INFORMATION:**\n• Send 10-digit Indian mobile number\n• Returns: Name, Father, Address, Alternate Number, Circle\n\n**🚗 VEHICLE INFORMATION:**\n• Send vehicle registration number\n• Returns: Owner Details, RC Info, Insurance, PUC, Vehicle Details\n\n👨‍💻 **Developer:** {DEVELOPER_NAME}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    user_id = query.from_user.id
    is_subscribed = check_subscription(update, context)
    if not is_subscribed:
        query.answer("❌ Please subscribe to all channels first!", show_alert=True)
        return
    
    if query.data == 'mobile_info':
        query.edit_message_text(
            f"📱 **Mobile Information**\n\nSend 10-digit Indian mobile number\n\n**Examples:**\n• `9876543210`\n• `98765 43210`\n• `+91 98765 43210`\n\n⏳ *Note: May take 10-15 seconds*\n\n👨‍💻 **Developer:** {DEVELOPER_NAME}",
            parse_mode='Markdown'
        )
    elif query.data == 'vehicle_info':
        query.edit_message_text(
            f"🚗 **Vehicle Information**\n\nSend vehicle registration number\n\n**Examples:**\n• `UP26R4005`\n• `DL1CAB1234`\n• `MH12AB1234`\n\n👨‍💻 **Developer:** {DEVELOPER_NAME}",
            parse_mode='Markdown'
        )
    elif query.data == 'mobile_examples':
        query.edit_message_text(
            f"📱 **Mobile Examples:**\n\n`9876543210`\n`98765 43210`\n`+91 98765 43210`\n\n👨‍💻 **Developer:** {DEVELOPER_NAME}",
            parse_mode='Markdown'
        )
    elif query.data == 'vehicle_examples':
        query.edit_message_text(
            f"🚗 **Vehicle Examples:**\n\n`UP26R4005`\n`DL1CAB1234`\n`MH12AB1234`\n\n👨‍💻 **Developer:** {DEVELOPER_NAME}",
            parse_mode='Markdown'
        )
    elif query.data == 'main_menu':
        keyboard = [
            [InlineKeyboardButton("📱 Mobile Info", callback_data='mobile_info')],
            [InlineKeyboardButton("🚗 Vehicle Info", callback_data='vehicle_info')],
            [InlineKeyboardButton("ℹ️ Help", callback_data='help')],
            [InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{DEVELOPER_NAME[1:]}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "🤖 **Dual Information Bot**\n\n📌 *I can fetch information from two sources:*\n\n📱 **Mobile Database** - Get complete mobile number details\n🚗 **Vehicle Database** - Get complete vehicle RC details\n\n🔍 **How to use:**\n• For Mobile: Send any 10-digit Indian number\n• For Vehicle: Send vehicle number (e.g., UP26R4005)\n\n📊 *Powered by dual APIs*\n\n✅ **Subscription Verified**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

def about_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"🤖 **Dual Information Bot**\n\n📱 Mobile + 🚗 Vehicle Info\n\n👨‍💻 **Developer:** {DEVELOPER_NAME}\n📢 **Channel:** {DEVELOPER_CHANNEL}",
        parse_mode='Markdown'
    )

def make_api_request(url):
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.json()
    except:
        return None
    return None

def fetch_mobile_info(phone_number):
    result = make_api_request(MOBILE_API_2.format(phone_number))
    if not result:
        result = make_api_request(MOBILE_API_1.format(phone_number))
    return result

def fetch_vehicle_info(vehicle_number):
    vehicle_clean = vehicle_number.upper().replace(" ", "")
    api1 = make_api_request(VEHICLE_API_1.format(vehicle_clean))
    api2 = make_api_request(VEHICLE_API_2.format(vehicle_clean))
    return {"api1": api1, "api2": api2, "vehicle": vehicle_clean}

def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    is_subscribed = check_subscription(update, context)
    
    if not is_subscribed:
        update.message.reply_text("❌ Please subscribe to all channels first using /start")
        return
    
    text = update.message.text.strip()
    
    if is_vehicle_number(text):
        vehicle = text.upper().replace(" ", "")
        msg = update.message.reply_text(f"🚗 **Searching Vehicle:** `{vehicle}`\n⏳ *Fetching details...*", parse_mode='Markdown')
        
        result = fetch_vehicle_info(vehicle)
        
        response = f"✅ **VEHICLE INFO: {vehicle}**\n\n"
        if result['api1']:
            if 'challan_info' in result['api1']:
                data = result['api1']['challan_info']
                response += f"👤 **Owner:** {data.get('owner_name', 'N/A')}\n"
                response += f"🚘 **Model:** {data.get('maker_model', 'N/A')}\n"
                response += f"🎨 **Color:** {data.get('vehicle_color', 'N/A')}\n"
                response += f"⛽ **Fuel:** {data.get('fuel_type', 'N/A')}\n"
            else:
                response += "✅ API 1: Connected\n"
        
        if result['api2']:
            response += "✅ API 2: Connected\n"
        
        if not result['api1'] and not result['api2']:
            response = f"❌ **No Vehicle Found:** `{vehicle}`"
        
        msg.edit_text(response + f"\n\n👨‍💻 **Developer:** {DEVELOPER_NAME}", parse_mode='Markdown')
    else:
        digits = ''.join(filter(str.isdigit, text))
        if len(digits) < 10:
            update.message.reply_text("❌ **Invalid Input**\n\nSend 10-digit mobile number or vehicle number")
            return
        
        phone = digits[-10:]
        msg = update.message.reply_text(f"📱 **Searching Mobile:** `{format_phone_number(phone)}`\n⏳ *Fetching details...*", parse_mode='Markdown')
        
        result = fetch_mobile_info(phone)
        
        if result:
            if result.get('success') and result.get('result'):
                data = result['result'][0] if result['result'] else {}
                response = f"✅ **MOBILE INFO: {format_phone_number(phone)}**\n\n"
                response += f"👤 **Name:** {data.get('name', 'N/A')}\n"
                response += f"👨 **Father:** {data.get('father_name', 'N/A')}\n"
                response += f"📍 **Address:** {data.get('address', 'N/A')[:50]}...\n"
                response += f"📞 **Alt:** {data.get('alt_mobile', 'N/A')}\n"
                response += f"🌍 **Circle:** {data.get('circle', 'N/A')}\n"
            elif result.get('success') and result.get('data'):
                data = result['data'][0] if result['data'] else {}
                response = f"✅ **MOBILE INFO: {format_phone_number(phone)}**\n\n"
                response += f"👤 **Name:** {data.get('name', 'N/A')}\n"
                response += f"👨 **Father:** {data.get('fname', 'N/A')}\n"
                response += f"📍 **Address:** {data.get('address', 'N/A')[:50]}...\n"
                response += f"📞 **Alt:** {data.get('alt', 'N/A')}\n"
                response += f"🌍 **Circle:** {data.get('circle', 'N/A')}\n"
            else:
                response = f"❌ **No Mobile Found:** `{format_phone_number(phone)}`"
        else:
            response = f"❌ **No Mobile Found:** `{format_phone_number(phone)}`"
        
        msg.edit_text(response + f"\n\n👨‍💻 **Developer:** {DEVELOPER_NAME}", parse_mode='Markdown')

def main():
    print("🤖 DUAL INFORMATION BOT STARTING...")
    print(f"📱 Mobile + 🚗 Vehicle Info")
    print(f"👨‍💻 Developer: {DEVELOPER_NAME}")
    
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("about", about_command))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    print("✅ Bot running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
