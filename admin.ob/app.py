import datetime
import telebot
import ssl
import certifi

API_TOKEN = '8191961162:AAGo_BkBhLTY7VbgMJ5DTeih5wBBq_l71mE'

# Обновление сертификатов SSL (если необходимо)
ssl._create_default_https_context = ssl.create_default_context
ssl._create_default_https_context().load_verify_locations(certifi.where())

bot = telebot.TeleBot(API_TOKEN)

# Функция логирования
def log_event(event):
    with open('admin_bot_logs.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(f"{datetime.datetime.now()} - {event}\n")

# Функция отправки сообщения администратору
def notify_admin(admin_chat_id, message):
    try:
        bot.send_message(admin_chat_id, message)
        log_event(f"Уведомление отправлено администратору {admin_chat_id}: {message}")
    except Exception as e:
        log_event(f"Ошибка при отправке уведомления администратору: {e}")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_message(
            message.chat.id,
            "Администраторский бот активен. Контролируйте действия пользователей."
        )
        log_event(f"Admin bot started by {message.chat.id}")
    except Exception as e:
        log_event(f"Ошибка при отправке стартового сообщения: {e}")

# Обработчик сообщений от пользователей
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        log_event(f"Получено сообщение от {message.chat.id}: {message.text}")
        bot.send_message(
            message.chat.id,
            f"Получено сообщение: {message.text}\nДанные записаны в логи."
        )

        # Уведомить администратора о сообщении пользователя
        admin_chat_id = 123456789  # Замените на ID администратора
        notify_admin(admin_chat_id, f"Сообщение от пользователя {message.chat.id}: {message.text}")

    except Exception as e:
        log_event(f"Ошибка обработки сообщения: {e}")
        bot.send_message(
            message.chat.id,
            "Произошла ошибка при обработке сообщения. Пожалуйста, попробуйте снова."
        )

# Обработчик команды /notify для отправки уведомлений пользователям
@bot.message_handler(commands=['notify'])
def notify_user(message):
    try:
        args = message.text.split(' ', 2)
        if len(args) < 3:
            bot.send_message(message.chat.id, "❌ Используйте формат: /notify <user_id> <сообщение>")
            return

        user_id = int(args[1])
        user_message = args[2]

        bot.send_message(user_id, user_message)
        bot.send_message(message.chat.id, f"✅ Сообщение отправлено пользователю {user_id}.")
        log_event(f"Сообщение пользователю {user_id}: {user_message}")

    except Exception as e:
        log_event(f"Ошибка при отправке уведомления пользователю: {e}")
        bot.send_message(message.chat.id, "❌ Ошибка при отправке сообщения. Проверьте ID пользователя и попробуйте снова.")

# Запуск бота
if __name__ == '__main__':
    try:
        log_event("Admin bot started.")
        bot.infinity_polling()
    except ssl.SSLError as ssl_error:
        log_event(f"Ошибка SSL: {ssl_error}")
        print("Проблема с SSL-сертификатом. Убедитесь, что сертификаты обновлены.")
    except Exception as e:
        log_event(f"Ошибка при запуске бота: {e}")
