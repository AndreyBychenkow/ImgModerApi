# 🐍 Image Moderation API

**Сервер на FastAPI для проверки изображений на NSFW-контент через DeepAI.**

## 🖋 Описание

Это backend-приложение на FastAPI, которое принимает изображения и проверяет их на наличие нежелательного контента (NSFW) с помощью DeepAI API.

## 🛠 Установка и настройка

### 📌 1. Клонирование репозитория

```bash
git clone https://github.com/AndreyBychenkow/ImgModerApi
cd ImgModerApi
```

### 📌 2. Создание виртуального окружения

```bash
python -m venv venv

# Активация на Windows
venv\Scripts\activate

# Активация на macOS/Linux
source venv/bin/activate
```

### 📌 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 📌 4. Настройка API ключа

1. Зарегистрируйтесь на [DeepAI](https://deepai.org/) и получите API ключ
2. Создайте файл `.env` и вставьте ваш API ключ:

```
DEEPAI_API_KEY=your_actual_api_key_here
```

## 🚀 Запуск сервера

```bash
python main.py
```

Сервис будет доступен по адресу **http://localhost:8000/** (Swagger UI — **/docs**).

## 🧷 Эндпоинты

| Метод | Путь        | Описание                                  |
|-------|-------------|-------------------------------------------|
| POST  | /moderate   | Принимает изображение (.jpg/.jpeg/.png)   |
| GET   | /           | Проверка работоспособности сервера        |
| GET   | /health     | Проверка «здоровья» сервиса               |


### 🔗 Примеры ответов

#### 🟢 Безопасное изображение:

```json
{
    "status": "OK"
}
```

#### ⛔ Изображение с нежелательным контентом:

```json
{
    "status": "REJECTED",
    "reason": "NSFW content"
}
```

## 📝 Логика модерации

- Если `nsfw_score > 0.7` → изображение отклоняется (REJECTED)
- В противном случае → изображение одобрено (OK)

## 📝 Поддерживаемые форматы

- `.jpg`
- `.jpeg`
- `.png`

## ⚠ Требования

- Python 3.8+
- Активный API ключ от DeepAI

## 🌐 API документация

После запуска сервера, автоматическая документация доступна по адресам:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## ⏳ Обработка ошибок

API возвращает следующие коды ошибок:
- `400` - Неверный формат файла
- `500` - Ошибка сервера или API DeepAI

## ⚡ Важно

* Нужен актуальный **DEEPAI_API_KEY** — получи его на https://deepai.org/
* При исчерпании лимита DeepAI вернёт ошибку «Out of API credits».