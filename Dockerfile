FROM python:3.11-slim

WORKDIR /app

# Копируем весь проект в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем бота из папки /app/bot/
CMD ["python", "-m", "bot.main"]

