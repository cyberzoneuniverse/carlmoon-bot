from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import uuid
from datetime import datetime

TOKEN = "8811474118:AAHz40f6n20q93UV9Txhpj4TaIm54a1WK88"

deals = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌙 Welcome to Carl Moon Escrow Services\n\n"
        "Secure crypto deals with only 5% commission.\n\n"
        "Use /newdeal to start a new escrow deal.\n"
        "Type /help to see all commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Carl Moon Escrow – Command List\n\n"
        "/newdeal – Create a new escrow deal\n"
        "/mydeals – View your deals\n"
        "/status – Check deal status\n"
        "/seller – Set seller wallet address\n"
        "/buyer – Set buyer wallet address\n"
        "/description – Add deal description\n"
        "/balance – Check deal balance & 5% fee\n"
        "/pay_seller – Release funds to seller\n"
        "/refund_buyer – Refund to buyer\n"
        "/dispute – Open a dispute\n"
        "/terms – View terms\n"
        "/support – Contact support\n"
        "/cancel – Cancel current deal"
    )
    await update.message.reply_text(text)

async def newdeal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deal_id = str(uuid.uuid4())[:8]
    user_id = update.effective_user.id

    deals[deal_id] = {
        "creator": user_id,
        "buyer": None,
        "seller": None,
        "buyer_address": None,
        "seller_address": None,
        "amount": 0,
        "description": "No description yet",
        "status": "created",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "fee_percent": 5
    }

    context.user_data["current_deal"] = deal_id

    await update.message.reply_text(
        f"✅ New escrow deal created!\n\n"
        f"Deal ID: {deal_id}\n"
        f"Status: Created\n"
        f"Commission: 5%\n\n"
        f"Next steps:\n"
        f"1. /description – Add deal details\n"
        f"2. /buyer or /seller – Set roles & addresses\n"
        f"3. Share the Deal ID with the other party"
    )

async def mydeals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    found = False
    text = "Your Deals:\n\n"

    for deal_id, deal in deals.items():
        if deal["creator"] == user_id or deal["buyer"] == user_id or deal["seller"] == user_id:
            text += f"• {deal_id} – {deal['status']} – {deal['description'][:30]}\n"
            found = True

    if not found:
        text = "You have no deals yet. Use /newdeal to create one."

    await update.message.reply_text(text)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deal_id = context.user_data.get("current_deal")
    if not deal_id or deal_id not in deals:
        await update.message.reply_text("No active deal. Use /newdeal first.")
        return

    deal = deals[deal_id]
    fee = deal["amount"] * 0.05
    net = deal["amount"] - fee

    text = (
        f"Deal Status\n\n"
        f"ID: {deal_id}\n"
        f"Status: {deal['status']}\n"
        f"Description: {deal['description']}\n"
        f"Amount: {deal['amount']}\n"
        f"5% Fee: {fee:.2f}\n"
        f"Seller receives: {net:.2f}\n"
        f"Created: {deal['created_at']}"
    )
    await update.message.reply_text(text)

async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /description Your deal details here")
        return

    deal_id = context.user_data.get("current_deal")
    if not deal_id or deal_id not in deals:
        await update.message.reply_text("No active deal. Use /newdeal first.")
        return

    deals[deal_id]["description"] = " ".join(context.args)
    await update.message.reply_text(f"✅ Description updated:\n{deals[deal_id]['description']}")

async def seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /seller YOUR_WALLET_ADDRESS")
        return

    deal_id = context.user_data.get("current_deal")
    if not deal_id or deal_id not in deals:
        await update.message.reply_text("No active deal. Use /newdeal first.")
        return

    deals[deal_id]["seller"] = update.effective_user.id
    deals[deal_id]["seller_address"] = context.args[0]
    await update.message.reply_text(f"✅ Seller address set: {context.args[0]}")

async def buyer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /buyer YOUR_WALLET_ADDRESS")
        return

    deal_id = context.user_data.get("current_deal")
    if not deal_id or deal_id not in deals:
        await update.message.reply_text("No active deal. Use /newdeal first.")
        return

    deals[deal_id]["buyer"] = update.effective_user.id
    deals[deal_id]["buyer_address"] = context.args[0]
    await update.message.reply_text(f"✅ Buyer address set: {context.args[0]}")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deal_id = context.user_data.get("current_deal")
    if not deal_id or deal_id not in deals:
        await update.message.reply_text("No active deal.")
        return

    deal = deals[deal_id]
    fee = deal["amount"] * 0.05
    await update.message.reply_text(
        f"Deal Balance\n"
        f"Amount: {deal['amount']}\n"
        f"Carl Moon Fee (5%): {fee:.2f}\n"
        f"Net to Seller: {deal['amount'] - fee:.2f}"
    )

async def pay_seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deal_id = context.user_data.get("current_deal")
    if not deal_id or deal_id not in deals:
        await update.message.reply_text("No active deal.")
        return

    deals[deal_id]["status"] = "released_to_seller"
    await update.message.reply_text("✅ Payment released to seller (simulated). Deal completed.")

async def refund_buyer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deal_id = context.user_data.get("current_deal")
    if not deal_id or deal_id not in deals:
        await update.message.reply_text("No active deal.")
        return

    deals[deal_id]["status"] = "refunded_to_buyer"
    await update.message.reply_text("✅ Payment refunded to buyer (simulated).")

async def dispute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deal_id = context.user_data.get("current_deal")
    if not deal_id or deal_id not in deals:
        await update.message.reply_text("No active deal.")
        return

    deals[deal_id]["status"] = "disputed"
    await update.message.reply_text("⚠️ Dispute opened. An admin will review this deal shortly.")

async def terms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Carl Moon Escrow Terms\n\n"
        "• Commission: Fixed 5%\n"
        "• Funds are held until both parties confirm\n"
        "• Disputes are reviewed by Carl Moon admin\n"
        "• Do not release funds until you receive the goods/service"
    )

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("For support, contact the Carl Moon admin directly or open a /dispute.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deal_id = context.user_data.get("current_deal")
    if deal_id and deal_id in deals:
        deals[deal_id]["status"] = "cancelled"
        await update.message.reply_text("Deal cancelled.")
    else:
        await update.message.reply_text("No active deal to cancel.")

def main():
    app = Application.builder().token(TOKEN).connect_timeout(30).read_timeout(30).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("newdeal", newdeal))
    app.add_handler(CommandHandler("mydeals", mydeals))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("description", description))
    app.add_handler(CommandHandler("seller", seller))
    app.add_handler(CommandHandler("buyer", buyer))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("pay_seller", pay_seller))
    app.add_handler(CommandHandler("refund_buyer", refund_buyer))
    app.add_handler(CommandHandler("dispute", dispute))
    app.add_handler(CommandHandler("terms", terms))
    app.add_handler(CommandHandler("support", support))
    app.add_handler(CommandHandler("cancel", cancel))

    print("Carl Moon Escrow Bot is now active...")
    app.run_polling()

if __name__ == "__main__":
    main()