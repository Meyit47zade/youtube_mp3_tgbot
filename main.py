from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import yt_dlp
import os
import tempfile


# BY WAVE ACADEMY
# 2024

# Функция для отправки аудиофайла в формате mp3 через Telegram бот
def send_audio(update, context, audio_file_path):
    try:
        # Отправляем аудиофайл пользователю
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio_file_path, 'rb'))
    except Exception as e:
        print("Ses gönderilirken bir hata oluştu:", e)
    finally:
        # Удаляем временный файл после отправки
        os.remove(audio_file_path)

# Функция для загрузки видео с YouTube и извлечения аудиодорожки в формате mp3


def download_and_convert_audio(update, context):
    try:
        print("ok")
        print(update.message.text.split(' '))
        # Получаем ссылку на YouTube видео из сообщения пользователя
        video_url = update.message.text.split(' ')[0]

        print("Video bağlantısı:", video_url)  # Добавляем логирование

        # Создаем временный каталог для сохранения аудиофайла
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Настройки для youtube_dl

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': f'{tmp_dir}/audio'  # Remove the .mp3 extension
            }

            # Загружаем видео с YouTube и извлекаем аудиодорожку
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            # Отправляем аудиофайл пользователю
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(f'{tmp_dir}/audio.mp3', 'rb'))
    except IndexError as e:
        print("bir hata oluştu IndexError:", e)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bu video ile ses bulunamadı.")
    except Exception as e:
        print("Video yüklenirken veya ses çıkartılırken bir hata oluştu:", e)


# Функция для обработки команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Merhaba! Bana YouTube videosunun bağlantısını gönderin, böylece size sesi mp3 formatında gönderebileyim.')

def main():
    # Инициализация бота с вашим токеном
    updater = Updater("7218232167:AAHiNANcjt6PggG-92Hijy2Jx5GMUW7BCqo", use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Регистрируем обработчик команды /start
    dp.add_handler(CommandHandler("start", start))

    # Регистрируем обработчик для обработки ссылок на YouTube видео
    dp.add_handler(MessageHandler(Filters.regex(r'https?://(?:www\.)?youtube\.com/\S+'), download_and_convert_audio))

    # Стартуем бота
    updater.start_polling()

    # Ожидаем завершения бота
    updater.idle()

if __name__ == '__main__':
    main()
