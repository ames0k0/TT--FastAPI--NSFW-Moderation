# Сервис модерации изображений
Сервер, который принимает изображение и отправляет его в бесплатный сервис модерации,<br />
чтобы понять — есть ли на нём нежелательный контент

### Скачивание проекта
```bash
git clone \
  --single-branch \
  --depth=1 \
  https://github.com/ames0k0/TT--FastAPI--NSFW-Moderation
```

### Запуск проекта локально
<details>
  <summary>Зависимости</summary>
  <pre>
python -V  # Python 3.12.8</pre>
</details>

```bash
cd TT--FastAPI--NSFW-Moderation

# Создание виртуальной среды
python3 -m venv env
# Активация виртуальной среды
source env/bin/activate

# Скачивание зависимостей
pip install -r requirements.txt
# Запуск проекта
fastapi run src/main.py
```

| Сервис                        | Документация / SwaggerUI                  |
| ----------------------------- | ----------------------------------------- |
| http://127.0.0.1:8000/        | http://127.0.0.1:8000/docs                |

### REST API Эндпоинты

- <details>
  <summary><strong>POST /moderate</strong> - Проверка файла на нежелательный контент</summary>

  | Тело запроса    | Тип   | Описание          |
  | --------------- | ----- | ----------------- |
  | file            | Файл  | Файл для проверки |

  ```bash
  curl -X 'POST' \
    'http://127.0.0.1:8000/moderate' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'file=@./data/ok.jpg;type=image/jpeg'
  ```

  ```json
  {
    "status": "OK"
  }
  ```

  ```bash
  curl -X 'POST' \
    'http://127.0.0.1:8000/moderate' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'file=@./data/nsfw.jpg;type=image/jpeg'
  ```

  ```json
  {
    "status": "REJECTED",
    "reason": "NSFW Content"
  }
  ```
</details>
