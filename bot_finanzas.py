import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Guarda aquí tu token de BotFather
TOKEN = "7954065938:AAGkdLjU1JC8iJ74jVK_sw-Xg73BOhZpURE"

# Diccionario donde se almacenan los datos por usuario
usuarios = {}

def obtener_mes_actual():
    hoy = datetime.datetime.now()
    return hoy.strftime("%Y-%m")

def init_usuario(user_id):
    if user_id not in usuarios:
        usuarios[user_id] = {"movimientos": []}

async def ingreso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    init_usuario(user_id)

    if len(context.args) < 2:
        await update.message.reply_text("Uso: /ingreso cantidad concepto")
        return

    try:
        cantidad = float(context.args[0])
        concepto = " ".join(context.args[1:])
        usuarios[user_id]["movimientos"].append({
            "tipo": "ingreso",
            "cantidad": cantidad,
            "concepto": concepto,
            "fecha": datetime.datetime.now()
        })
        await update.message.reply_text(f"Ingreso registrado: +{cantidad} ({concepto})")
    except ValueError:
        await update.message.reply_text("La cantidad debe ser un número.")

async def gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    init_usuario(user_id)

    if len(context.args) < 2:
        await update.message.reply_text("Uso: /gasto cantidad categoría")
        return

    try:
        cantidad = float(context.args[0])
        categoria = " ".join(context.args[1:])
        usuarios[user_id]["movimientos"].append({
            "tipo": "gasto",
            "cantidad": cantidad,
            "concepto": categoria,
            "fecha": datetime.datetime.now()
        })
        await update.message.reply_text(f"Gasto registrado: -{cantidad} ({categoria})")
    except ValueError:
        await update.message.reply_text("La cantidad debe ser un número.")

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    init_usuario(user_id)

    movimientos = usuarios[user_id]["movimientos"]
    saldo = sum(m["cantidad"] if m["tipo"] == "ingreso" else -m["cantidad"] for m in movimientos)
    await update.message.reply_text(f"Saldo actual: {saldo:.2f} €")

async def gasto_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    init_usuario(user_id)

    if len(context.args) < 1:
        await update.message.reply_text("Uso: /gasto_categoria nombre_categoria")
        return

    categoria = " ".join(context.args).lower()
    mes_actual = obtener_mes_actual()

    total = 0
    for m in usuarios[user_id]["movimientos"]:
        if m["tipo"] == "gasto" and m["concepto"].lower() == categoria:
            if m["fecha"].strftime("%Y-%m") == mes_actual:
                total += m["cantidad"]

    await update.message.reply_text(f"Este mes has gastado {total:.2f} € en {categoria}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy tu bot financiero personal.\n\n"
        "Comandos disponibles:\n"
        "/ingreso cantidad concepto\n"
        "/gasto cantidad categoría\n"
        "/saldo\n"
        "/gasto_categoria nombre_categoria"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ingreso", ingreso))
    app.add_handler(CommandHandler("gasto", gasto))
    app.add_handler(CommandHandler("saldo", saldo))
    app.add_handler(CommandHandler("gasto_categoria", gasto_categoria))

    print("Bot iniciado...")
    app.run_polling()
