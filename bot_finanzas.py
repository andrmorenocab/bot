import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN") or "TU_TOKEN_AQUI"

# Aquí guardaremos datos simples en memoria (puedes cambiar a archivo o DB luego)
movimientos = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy tu bot financiero.\n"
        "Usa /ingreso <cantidad> <categoria>\n"
        "Usa /gasto <cantidad> <categoria>\n"
        "Usa /saldo para ver tu saldo actual\n"
        "Usa /gasto_categoria <categoria> para ver gasto en categoría"
    )

async def ingreso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /ingreso <cantidad> <categoria>")
        return
    try:
        cantidad = float(context.args[0])
    except ValueError:
        await update.message.reply_text("Cantidad no válida.")
        return
    categoria = context.args[1]
    movimientos.append({"tipo": "ingreso", "cantidad": cantidad, "categoria": categoria})
    await update.message.reply_text(f"Ingreso registrado: {cantidad} en {categoria}")

async def gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /gasto <cantidad> <categoria>")
        return
    try:
        cantidad = float(context.args[0])
    except ValueError:
        await update.message.reply_text("Cantidad no válida.")
        return
    categoria = context.args[1]
    movimientos.append({"tipo": "gasto", "cantidad": cantidad, "categoria": categoria})
    await update.message.reply_text(f"Gasto registrado: {cantidad} en {categoria}")

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    saldo = 0
    for m in movimientos:
        if m["tipo"] == "ingreso":
            saldo += m["cantidad"]
        else:
            saldo -= m["cantidad"]
    await update.message.reply_text(f"Saldo actual: {saldo}")

async def gasto_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Uso: /gasto_categoria <categoria>")
        return
    categoria = context.args[0]
    total = sum(m["cantidad"] for m in movimientos if m["tipo"] == "gasto" and m["categoria"] == categoria)
    await update.message.reply_text(f"Gasto total en {categoria}: {total}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ingreso", ingreso))
    app.add_handler(CommandHandler("gasto", gasto))
    app.add_handler(CommandHandler("saldo", saldo))
    app.add_handler(CommandHandler("gasto_categoria", gasto_categoria))

    print("Bot iniciado...")
    app.run_polling()
