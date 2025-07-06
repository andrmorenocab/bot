import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Token desde variable de entorno o directo
TOKEN = os.getenv("BOT_TOKEN") or "PON_AQUI_TU_TOKEN"

# Lista para almacenar movimientos (temporal)
movimientos = []

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy tu bot financiero.\n"
        "Usa:\n"
        "/ingreso <cantidad> <categoria>\n"
        "/gasto <cantidad> <categoria>\n"
        "/saldo\n"
        "/gasto_categoria <categoria>"
    )

# Comando /ingreso
async def ingreso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /ingreso <cantidad> <categoria>")
        return
    try:
        cantidad = float(context.args[0])
    except ValueError:
        await update.message.reply_text("Cantidad inválida.")
        return
    categoria = context.args[1]
    movimientos.append({"tipo": "ingreso", "cantidad": cantidad, "categoria": categoria})
    await update.message.reply_text(f"Ingreso registrado: {cantidad} en {categoria}")

# Comando /gasto
async def gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /gasto <cantidad> <categoria>")
        return
    try:
        cantidad = float(context.args[0])
    except ValueError:
        await update.message.reply_text("Cantidad inválida.")
        return
    categoria = context.args[1]
    movimientos.append({"tipo": "gasto", "cantidad": cantidad, "categoria": categoria})
    await update.message.reply_text(f"Gasto registrado: {cantidad} en {categoria}")

# Comando /saldo
async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    saldo_total = sum(m["cantidad"] if m["tipo"] == "ingreso" else -m["cantidad"] for m in movimientos)
    await update.message.reply_text(f"Saldo actual: {saldo_total}")

# Comando /gasto_categoria
async def gasto_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Uso: /gasto_categoria <categoria>")
        return
    categoria = context.args[0]
    total = sum(m["cantidad"] for m in movimientos if m["tipo"] == "gasto" and m["categoria"] == categoria)
    await update.message.reply_text(f"Gasto total en {categoria}: {total}")

# Arranque del bot
if __name__ == '__main__':
    app =
