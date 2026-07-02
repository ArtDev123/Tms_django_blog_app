# Django — часть 1. Практическое руководство: проект «Блог»

Пошаговое руководство для занятия. Все команды выполняются в папке **`TMS_django`**.

> **Предварительно:** установите PostgreSQL и создайте базу `blog_db` по инструкции [`POSTGRESQL_INSTALL.md`](POSTGRESQL_INSTALL.md).

---

## Содержание

1. [Что такое Django](#1-что-такое-django)
2. [Подготовка окружения](#2-подготовка-окружения)
3. [Проект vs Приложение](#3-проект-vs-приложение)
4. [Создание проекта blog](#4-создание-проекта-blog)
5. [Структура проекта](#5-структура-проекта)
6. [Первый запуск — dev-сервер](#6-первый-запуск--dev-сервер)
7. [Переменные окружения и .env](#7-переменные-окружения-и-env)
8. [Подключение PostgreSQL](#8-подключение-postgresql)
9. [Приложение posts — сущность «Пост»](#9-приложение-posts--сущность-пост)
10. [Приложение comments — сущность «Комментарий»](#10-приложение-comments--сущность-комментарий)
11. [Миграции и manage-команды](#11-миграции-и-manage-команды)
12. [Админ-панель Django](#12-админ-панель-django)
13. [Views и URL — показать посты](#13-views-и-url--показать-посты)
14. [Шаблоны (Templates)](#14-шаблоны-templates)
15. [Справочник manage-команд](#15-справочник-manage-команд)
16. [Итоговая структура проекта](#16-итоговая-структура-проекта)
17. [Что изучили на занятии](#17-что-изучили-на-занятии)
18. [Полезные ссылки (документация Django)](#полезные-ссылки)

### Порядок на занятии

```
venv → проект blog → .env → PostgreSQL → migrate (системные таблицы)
     → приложения posts/comments → модели → migrate → админка → views → шаблоны
```

---

## 1. Что такое Django

**Django** — бесплатный веб-фреймворк на Python для быстрой разработки сайтов. Он следует паттерну **MVT**:

| Буква | Значение | Аналог в MVC |
|-------|----------|--------------|
| **M** | Model (модель) | Данные, таблицы БД |
| **V** | View (представление) | Логика — что показать |
| **T** | Template (шаблон) | HTML-разметка |

Django «из коробки» даёт:
- ORM (работа с БД через Python-классы)
- Админ-панель
- Систему маршрутизации URL
- Формы, аутентификацию, безопасность

**django-admin** — утилита командной строки для создания проектов.  
**manage.py** — «пульт управления» конкретным проектом (миграции, сервер, создание приложений).

### Как это работает вместе (MVT на примере)

Когда пользователь открывает http://127.0.0.1:8000/1/:

```
1. URL-маршрутизатор смотрит urls.py → находит view post_detail
2. View (views.py) обращается к Model (models.py) → Post.objects.get(pk=1)
3. View передаёт данные в Template (post_detail.html) → получается HTML
4. Браузер показывает страницу
```

Модель знает про базу данных. View знает, *что* показать. Шаблон знает, *как* это нарисовать.

📖 **Документация Django:**
- [Обзор Django](https://docs.djangoproject.com/en/stable/)
- [FAQ: MVT vs MVC](https://docs.djangoproject.com/en/stable/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-names-mvc)
- [Официальный Tutorial (часть 1)](https://docs.djangoproject.com/en/stable/intro/tutorial01/)

---

## 2. Подготовка окружения

### Шаг 2.1. Перейти в рабочую папку

```bash
cd /home/artem/Code/TMS_django
```

На Windows (пример):

```powershell
cd C:\Users\YourName\Code\TMS_django
```

### Шаг 2.2. Создать виртуальное окружение

**Зачем нужен venv?** У разных проектов могут быть разные версии Django и библиотек. Виртуальное окружение создаёт изолированную «песочницу» — пакеты ставятся только для этого проекта и не ломают другие.

```bash
python3 -m venv venv
```

Папка `venv/` появится в проекте. Её **не коммитят** в git (добавим в `.gitignore` позже).

### Шаг 2.3. Активировать окружение

**Linux / macOS:**

```bash
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (cmd):**

```cmd
venv\Scripts\activate.bat
```

После активации в начале строки терминала появится `(venv)`.

### Шаг 2.4. Обновить pip и установить зависимости

```bash
pip install --upgrade pip
pip install django python-dotenv psycopg2-binary
```

| Пакет | Зачем |
|-------|-------|
| `django` | Сам фреймворк |
| `python-dotenv` | Загрузка переменных из `.env` |
| `psycopg2-binary` | Драйвер PostgreSQL для Django |

> Все три пакета нужны **сразу** — PostgreSQL подключаем до создания моделей.

### Шаг 2.5. Зафиксировать зависимости

```bash
pip freeze > requirements.txt
```

Файл `requirements.txt` позволяет другим (и вам на другом компьютере) установить те же версии:

```bash
pip install -r requirements.txt
```

📖 **Документация Django:**
- [Установка Django](https://docs.djangoproject.com/en/stable/topics/install/)
- [Как управлять зависимостями (pip)](https://docs.djangoproject.com/en/stable/topics/install/#installing-an-official-release-with-pip)

---

Это **ключевые понятия** занятия.

### Проект (Project) — верхний уровень

**Проект** — конфигурация всего сайта: настройки, URL-маршруты верхнего уровня, подключение к БД, список приложений.

В нашем случае проект называется **`blog`** — это «оболочка» всего блога.

```
TMS_django/
├── blog/              ← ПРОЕКТ (конфигурация сайта)
│   ├── settings.py
│   └── urls.py
├── manage.py
├── posts/             ← ПРИЛОЖЕНИЕ (сущность: пост)
├── comments/          ← ПРИЛОЖЕНИЕ (сущность: комментарий)
└── ...
```

### Приложение (App) — одна сущность / один домен

**Приложение** — изолированный модуль, отвечающий за **одну бизнес-сущность**.

| Приложение | Сущность | Что внутри |
|------------|----------|------------|
| `posts` | Пост | модель Post, views, шаблоны списка/детали |
| `comments` | Комментарий | модель Comment, связь с Post |
| `categories` | Категория | *(на будущее)* |
| `tags` | Тег | *(на будущее)* |

**Правило:** одно приложение = одна сущность. Не складываем Post, Comment и Category в одно приложение.

**Аналогия:**
- **Проект `blog`** — здание (общие настройки, электричество, водопровод)
- **Приложения `posts`, `comments`** — отдельные квартиры с разным назначением

| | Проект | Приложение |
|---|---|---|
| Создаётся | Один раз | По одному на каждую сущность |
| Команда | `django-admin startproject blog` | `manage.py startapp posts` |
| Содержит | settings.py, urls.py | models.py, views.py, admin.py |
| Пример | `blog/` | `posts/`, `comments/` |

📖 **Документация Django:**
- [Projects and applications](https://docs.djangoproject.com/en/stable/intro/reusable-apps/)
- [Структура проекта](https://docs.djangoproject.com/en/stable/intro/overview/)

---

### Шаг 4.1. Создать проект

```bash
django-admin startproject blog .
```

**Обратите внимание на точку `.` в конце** — проект создаётся в текущей папке `TMS_django`, а не во вложенной.

Без точки Django создал бы лишнюю вложенность:

```
TMS_django/
└── blog/
    └── blog/      ← лишний уровень
```

### Шаг 4.2. Что появилось

```
TMS_django/
├── blog/                  # пакет конфигурации ПРОЕКТА
│   ├── __init__.py
│   ├── asgi.py            # для async-серверов
│   ├── settings.py        # ⚙️ главные настройки
│   ├── urls.py            # 🌐 URL маршруты проекта
│   └── wsgi.py            # для production-серверов
├── manage.py              # 🎮 manage-команды
├── venv/
└── requirements.txt
```

> Папка `blog/` здесь — это **проект** (конфигурация), а не приложение с моделями. Приложения создадим позже — после подключения PostgreSQL.

📖 **Документация Django:**
- [`django-admin startproject`](https://docs.djangoproject.com/en/stable/ref/django-admin/#django-admin-startproject)
- [Командная строка Django](https://docs.djangoproject.com/en/stable/ref/django-admin/)

---

Разберём ключевые файлы.

### `manage.py`

Точка входа для всех manage-команд. Не редактируют вручную.

```bash
python manage.py --help
```

### `blog/settings.py`

Главный конфиг:

- `INSTALLED_APPS` — список приложений (`posts`, `comments`, ...)
- `DATABASES` — настройки БД (PostgreSQL)
- `TEMPLATES` — шаблоны
- `SECRET_KEY` — секретный ключ (никогда в git!)
- `DEBUG` — режим отладки
- `ALLOWED_HOSTS` — разрешённые домены

### `blog/urls.py`

«Таблица маршрутов» верхнего уровня. Сюда подключают URL каждого приложения.

### `blog/wsgi.py` / `asgi.py`

Точки входа для веб-серверов (Gunicorn, uWSGI, Daphne). На занятии не трогаем.

📖 **Документация Django:**
- [Настройки (settings.py)](https://docs.djangoproject.com/en/stable/ref/settings/)
- [`INSTALLED_APPS`](https://docs.djangoproject.com/en/stable/ref/settings/#installed-apps)
- [URL dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)

---

Убедимся, что проект создан корректно.

### Шаг 6.1. Запустить сервер разработки

```bash
python manage.py runserver
```

Вывод:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Шаг 6.2. Открыть в браузере

Перейдите на http://127.0.0.1:8000/

Вы увидите стартовую страницу Django с ракетой — **проект работает**.

### Шаг 6.3. Остановить сервер

`Ctrl + C` в терминале.

> На этом этапе Django ещё использует SQLite по умолчанию. Следующие шаги — настроим PostgreSQL.

📖 **Документация Django:**
- [`runserver`](https://docs.djangoproject.com/en/stable/ref/django-admin/#runserver)
- [Development server](https://docs.djangoproject.com/en/stable/ref/django-admin/#runserver)

---

**Переменные окружения** — пары «ключ=значение», которые программа читает при запуске. Они живут **вне кода** — в операционной системе или в файле `.env`.

### Зачем это нужно

Представьте, вы пушите проект на GitHub. Если пароль от базы написан прямо в `settings.py`:

```python
PASSWORD = 'blog_password_123'  # ← плохо! попадёт в git, увидят все
```

Любой, кто видит репозиторий, получит доступ к вашей базе.

**Правильный подход:** пароль лежит в `.env` (файл **не коммитится**), а `settings.py` **читает** его:

```python
PASSWORD = os.getenv('DB_PASSWORD')  # ← код не содержит секрет
```

| | В коде | В .env |
|---|---|---|
| Безопасность | Плохо — видно в git | Хорошо — только у вас локально |
| Dev / Production | Один пароль на всех | Разные `.env` на разных серверах |
| Пример | `PASSWORD = '123'` | `DB_PASSWORD=123` |

Почему это важно:
- пароли не попадают в git
- разные настройки для dev и production
- один код — разные окружения

Настраиваем `.env` **до** создания моделей — так все данные сразу попадут в PostgreSQL.

### Шаг 7.1. Создать файл `.env`

В корне `TMS_django` создайте файл `.env`:

```env
# Django
SECRET_KEY=django-insecure-change-me-in-production-abc123xyz
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=blog_db
DB_USER=blog_user
DB_PASSWORD=blog_password_123
DB_HOST=localhost
DB_PORT=5432
```

> Значения БД должны совпадать с тем, что вы создали в [`POSTGRESQL_INSTALL.md`](POSTGRESQL_INSTALL.md).

### Шаг 7.2. Создать `.gitignore`

```
# .gitignore
venv/
__pycache__/
*.pyc
.env
*.log
.DS_Store
```

**`.env` никогда не коммитим в git!**

### Шаг 7.3. Создать `.env.example` (шаблон для команды)

```env
# .env.example — скопируйте в .env и заполните
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.postgresql
DB_NAME=blog_db
DB_USER=blog_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

`.env.example` **можно** коммитить — там нет реальных секретов.

### Шаг 7.4. Обновить `settings.py`

Откройте `blog/settings.py`. **В самом начале файла** замените импорты и `BASE_DIR` на:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # ← прочитать .env и загрузить переменные

BASE_DIR = Path(__file__).resolve().parent.parent
```

**Что делает каждая строка:**

| Строка | Объяснение |
|--------|------------|
| `import os` | Модуль для работы с переменными окружения (`os.getenv(...)`) |
| `from dotenv import load_dotenv` | Функция из пакета `python-dotenv` |
| `load_dotenv()` | Ищет файл `.env` в корне проекта и загружает все `KEY=VALUE` в память |
| `BASE_DIR` | Абсолютный путь к корню проекта (`TMS_django/`). Нужен для путей к файлам |

Замените `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`:

```python
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-key-only-for-dev')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')
```

**Разбор `os.getenv`:**

```python
os.getenv('SECRET_KEY', 'fallback-key-only-for-dev')
#         ↑ имя из .env    ↑ значение по умолчанию, если в .env нет
```

- `DEBUG = os.getenv('DEBUG', 'False') == 'True'` — из `.env` приходит строка `'True'`, а Django ждёт boolean. Сравниваем со строкой `'True'` → получаем `True` или `False`.
- `ALLOWED_HOSTS = ... .split(',')` — из `.env` строка `'127.0.0.1,localhost'`, Django ждёт **список**. `.split(',')` → `['127.0.0.1', 'localhost']`.

📖 **Документация Django:**
- [`SECRET_KEY`](https://docs.djangoproject.com/en/stable/ref/settings/#secret-key)
- [`DEBUG`](https://docs.djangoproject.com/en/stable/ref/settings/#debug)
- [`ALLOWED_HOSTS`](https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts)
- [Deployment checklist (про секреты)](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

---

> **Перед этим шагом** убедитесь, что PostgreSQL установлен, сервис запущен и база `blog_db` создана ([`POSTGRESQL_INSTALL.md`](POSTGRESQL_INSTALL.md)).

### Шаг 8.1. Настроить DATABASES в settings.py

Замените блок `DATABASES` в `blog/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'blog_db'),
        'USER': os.getenv('DB_USER', 'blog_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

Django читает параметры из `.env`. Пароль и логин не попадают в код.

**Разбор словаря `DATABASES`:**

```python
DATABASES = {
    'default': {   # ← имя подключения (можно несколько: 'default', 'analytics'...)
        'ENGINE': ...   # какой драйвер БД использовать
        'NAME': ...     # имя базы данных
        'USER': ...     # логин PostgreSQL
        'PASSWORD': ... # пароль
        'HOST': ...     # где сервер ('localhost' = на этом же компьютере)
        'PORT': ...     # порт (5432 — стандартный для PostgreSQL)
    }
}
```

| Ключ | Откуда берётся | Пример |
|------|----------------|--------|
| `ENGINE` | `.env` → `DB_ENGINE` | `django.db.backends.postgresql` |
| `NAME` | `.env` → `DB_NAME` | `blog_db` |
| `USER` | `.env` → `DB_USER` | `blog_user` |
| `PASSWORD` | `.env` → `DB_PASSWORD` | `blog_password_123` |
| `HOST` | `.env` → `DB_HOST` | `localhost` |
| `PORT` | `.env` → `DB_PORT` | `5432` |

`'default'` — имя подключения. Django использует его, если не указано другое. Для нашего проекта одного подключения достаточно.

### Шаг 8.2. Проверить подключение

```bash
python manage.py check --database default
```

Должно быть: `System check identified no issues`.

Если ошибка подключения — проверьте:
- запущен ли PostgreSQL (`sudo systemctl status postgresql`)
- совпадают ли логин/пароль/имя базы в `.env` и в PostgreSQL
- раздел «Частые проблемы» в [`POSTGRESQL_INSTALL.md`](POSTGRESQL_INSTALL.md)

### Шаг 8.3. Применить системные миграции

```bash
python manage.py migrate
```

Django создаст в PostgreSQL **системные таблицы**:
- `auth_user` — пользователи
- `django_session` — сессии
- `django_admin_log` — лог админки
- и другие служебные таблицы

> Своих таблиц (`posts_post`, `comments_comment`) пока нет — мы ещё не создавали приложения и модели.

### Шаг 8.4. Проверить таблицы в PostgreSQL (опционально)

```bash
psql -U blog_user -d blog_db -h localhost -c "\dt"
```

Вы увидите список таблиц `auth_*`, `django_*` — это нормально.

### Шаг 8.5. Проверить статус миграций

```bash
python manage.py showmigrations
```

Все встроенные приложения должны быть отмечены `[X]`.

📖 **Документация Django:**
- [PostgreSQL notes](https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes)
- [Настройка `DATABASES`](https://docs.djangoproject.com/en/stable/ref/settings/#databases)
- [`migrate`](https://docs.djangoproject.com/en/stable/ref/django-admin/#migrate)
- [`check --database`](https://docs.djangoproject.com/en/stable/ref/django-admin/#check)

---

PostgreSQL подключён — создаём первое приложение и модель.

### Шаг 9.1. Создать приложение

```bash
python manage.py startapp posts
```

### Шаг 9.2. Структура приложения

```
posts/
├── __init__.py
├── admin.py       # регистрация Post в админке
├── apps.py        # конфигурация приложения
├── migrations/    # файлы миграций БД
│   └── __init__.py
├── models.py      # 📦 модель Post
├── tests.py       # тесты
└── views.py       # 👁 логика отображения постов
```

### Шаг 9.3. Подключить приложение к проекту

Откройте `blog/settings.py`, найдите `INSTALLED_APPS` и добавьте `'posts'`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts',  # ← приложение «Пост»
]
```

> **Важно:** без записи в `INSTALLED_APPS` Django не видит приложение — миграции и админка не работают.

**Что такое `INSTALLED_APPS`?** Это список всех «модулей», которые Django должен знать. Встроенные (`django.contrib.admin`, `django.contrib.auth`...) дают админку, авторизацию, сессии. Наши (`posts`, `comments`) — бизнес-логику.

Django **не сканирует** папки автоматически. Создали папку `posts/` — этого мало, нужно явно прописать `'posts'` в settings.

---

### Шаг 9.4. Описать модель Post

**Что такое модель?** Это Python-класс, который описывает таблицу в базе данных. Каждый атрибут класса (`title`, `content`...) — это **столбец** таблицы. Каждый объект класса (`post = Post(...)`) — это **строка** в таблице.

`models.Model` — базовый класс Django. Наследуясь от него, мы говорим: «этот класс — модель, создай для него таблицу в БД».

Откройте `posts/models.py` и замените содержимое:

```python
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """Модель поста блога."""

    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
    )
    content = models.TextField(
        verbose_name='Содержание',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликован',
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
```

---

### Подробный разбор модели Post

Разберём код **построчно** — от общей идеи до каждого параметра.

#### Класс и таблица в БД

```python
class Post(models.Model):
```

Django автоматически создаст таблицу с именем **`posts_post`**:
- `posts` — имя приложения
- `post` — имя модели в нижнем регистре

Это convention Django, менять не нужно.

#### Поля модели — столбцы таблицы

Каждое поле = один столбец в PostgreSQL.

##### `title = models.CharField(max_length=200, verbose_name='Заголовок')`

| Параметр | Значение | Объяснение |
|----------|----------|------------|
| `CharField` | тип поля | Короткая строка (как `VARCHAR` в SQL) |
| `max_length=200` | 200 символов | Максимальная длина. Django проверяет это при сохранении |
| `verbose_name='Заголовок'` | подпись | Человекочитаемое имя поля — показывается в **админке** и формах |

##### `content = models.TextField(verbose_name='Содержание')`

`TextField` — длинный текст **без ограничения длины** (в отличие от CharField). Подходит для текста статьи, комментария, описания.

##### `author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')`

**ForeignKey** — «внешний ключ». Связь **многие-к-одному**:

```
User (один)  ←────  Post (много)
 admin              пост 1
                    пост 2
                    пост 3
```

Один пользователь может написать много постов. У каждого поста — один автор.

| Параметр | Объяснение |
|----------|------------|
| `User` | Модель, на которую ссылаемся. `User` — встроенная модель Django (таблица `auth_user`) |
| `on_delete=models.CASCADE` | Что делать, если пользователь **удалён**. `CASCADE` = удалить все его посты тоже. Другие варианты: `SET_NULL`, `PROTECT` — см. [on_delete argument](https://docs.djangoproject.com/en/stable/ref/models/fields/#django.db.models.ForeignKey.on_delete) |
| `related_name='posts'` | Имя **обратной связи**. Из пользователя можно получить его посты: `user.posts.all()`. Без `related_name` Django создал бы имя `post_set` — менее понятно |

В PostgreSQL Django создаст столбец `author_id` (число — id пользователя).

##### `created_at = models.DateTimeField(auto_now_add=True, ...)`

| Параметр | Объяснение |
|----------|------------|
| `DateTimeField` | Дата и время (2026-07-02 15:30:00) |
| `auto_now_add=True` | Заполняется **один раз** — в момент **создания** записи. При редактировании не меняется |

##### `updated_at = models.DateTimeField(auto_now=True, ...)`

| Параметр | Объяснение |
|----------|------------|
| `auto_now=True` | Обновляется **каждый раз** при сохранении записи (и при создании, и при редактировании) |

**Разница `auto_now_add` vs `auto_now`:**

| | auto_now_add | auto_now |
|---|---|---|
| Когда ставится | Только при создании | При каждом save() |
| Можно задать вручную | Да (только при создании) | Нет |
| Пример | Дата регистрации | Дата последнего изменения |

##### `is_published = models.BooleanField(default=True, ...)`

| Параметр | Объяснение |
|----------|------------|
| `BooleanField` | True / False (да / нет) |
| `default=True` | Если не указано — по умолчанию `True` (пост опубликован) |

---

#### `class Meta` — настройки модели (не поля!)

```python
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']
```

**`Meta`** — это **внутренний класс** внутри модели. Он **не создаёт столбец** в базе данных. Это «настройки поведения» модели — метаданные. Полный список опций: [Model `Meta` options](https://docs.djangoproject.com/en/stable/ref/models/options/).

Представьте: поля (`title`, `content`...) — это **данные** таблицы, а `Meta` — **инструкция для Django**, как с этой таблицей работать.

##### `verbose_name = 'Пост'`

Человекочитаемое имя модели в **единственном числе**.

Где используется:
- админка: «Добавить **Пост**», «Изменить **Пост**»
- сообщения об ошибках

Без `verbose_name` Django взял бы имя класса как есть — `Post` (на английском).

##### `verbose_name_plural = 'Посты'`

Имя модели во **множественном числе**.

Где используется:
- боковое меню админки: раздел **«Посты»**
- заголовок списка объектов

Без этого Django автоматически добавил бы `s` → `Posts`. Для русского языка это неудобно, поэтому задаём вручную.

**Пример в админке:**

```
Без Meta:                    С Meta:
├── Posts                    ├── Посты        ← verbose_name_plural
│   ├── Add Post             │   ├── Добавить Пост   ← verbose_name
│   └── Change Post          │   └── Изменить Пост
```

##### `ordering = ['-created_at']`

**Сортировка по умолчанию** — в каком порядке Django отдаёт записи, если вы не указали другой.

| Запись | Значение |
|--------|----------|
| `'created_at'` | По дате создания, **от старых к новым** (возрастание) |
| `'-created_at'` | По дате создания, **от новых к старым** (убывание). Минус `-` = reverse |

Это значит:
```python
Post.objects.all()
# вернёт посты: сначала самый новый, потом более старые
```

Можно указать несколько полей: `ordering = ['-is_published', '-created_at']` — сначала опубликованные, внутри группы по дате.

**`ordering` в Meta vs `.order_by()` в коде:**

| | Meta.ordering | QuerySet.order_by() |
|---|---|---|
| Когда | Всегда по умолчанию | Когда явно вызвали в view |
| Пример | `Post.objects.all()` | `Post.objects.order_by('title')` |
| Приоритет | Низкий | Высокий (перебивает Meta) |

---

#### `def __str__(self)` — текстовое представление объекта

```python
    def __str__(self):
        return self.title
```

Это **не поле базы данных**. Это Python-метод, который говорит: «когда нужно показать объект как текст — верни заголовок».

Где это видно:
- **админка** — в выпадающих списках вместо «Post object (1)» будет «Мой первый пост»
- **Django shell** — `print(post)` выведет заголовок
- **ForeignKey** — при выборе поста в комментарии покажется заголовок, а не `Post object (3)`

Без `__str__` Django показывал бы бесполезное `Post object (1)`.

---

### Сводная таблица полей

| Поле | Тип | В БД | Описание |
|------|-----|------|----------|
| `id` | AutoField | `id` (PK) | Создаётся **автоматически** Django — первичный ключ |
| `title` | CharField | `title VARCHAR(200)` | Заголовок |
| `content` | TextField | `content TEXT` | Текст поста |
| `author` | ForeignKey | `author_id INTEGER` | Ссылка на `auth_user.id` |
| `created_at` | DateTimeField | `created_at TIMESTAMP` | Когда создан |
| `updated_at` | DateTimeField | `updated_at TIMESTAMP` | Когда изменён |
| `is_published` | BooleanField | `is_published BOOLEAN` | Опубликован ли |

> Столбец `id` вы **не писали** — Django добавляет его сам к каждой модели. Это уникальный номер записи (1, 2, 3...).

📖 **Документация Django:**
- [Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Model field reference (все типы полей)](https://docs.djangoproject.com/en/stable/ref/models/fields/)
- [`ForeignKey`](https://docs.djangoproject.com/en/stable/ref/models/fields/#foreignkey)
- [`Meta` options (`verbose_name`, `ordering`...)](https://docs.djangoproject.com/en/stable/ref/models/options/)
- [Модель `User` (auth)](https://docs.djangoproject.com/en/stable/ref/contrib/auth/#user-model)
- [`django-admin startapp`](https://docs.djangoproject.com/en/stable/ref/django-admin/#startapp)

---

Создаём второе приложение — только для комментариев. Принцип **одна сущность = одно приложение**.

### Шаг 10.1. Создать приложение

```bash
python manage.py startapp comments
```

### Шаг 10.2. Подключить к проекту

В `blog/settings.py` добавьте `'comments'`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts',
    'comments',  # ← приложение «Комментарий»
]
```

### Шаг 10.3. Описать модель Comment

Откройте `comments/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Comment(models.Model):
    """Комментарий к посту."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий от {self.author} к «{self.post.title}»'
```

---

### Подробный разбор модели Comment

Модель Comment повторяет те же идеи, что и Post, но добавляет **связь между двумя приложениями**.

#### ForeignKey на Post — связь между приложениями

```python
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
```

| Параметр | Объяснение |
|----------|------------|
| `Post` | Ссылаемся на модель из **другого приложения** (`posts`). Django создаст столбец `post_id` |
| `on_delete=CASCADE` | Удалили пост → все его комментарии удалятся автоматически |
| `related_name='comments'` | **Обратная связь.** Из поста: `post.comments.all()` — все комментарии к этому посту |

**Схема связи:**

```
posts_post (таблица)          comments_comment (таблица)
┌────┬──────────────┐         ┌────┬─────────┬───────────┐
│ id │ title        │         │ id │ post_id │ text      │
├────┼──────────────┤         ├────┼─────────┼───────────┤
│ 1  │ Первый пост  │◄────────│ 1  │ 1       │ Класс!    │
│ 2  │ Второй пост  │         │ 2  │ 1       │ Спасибо   │
└────┴──────────────┘         │ 3  │ 2       │ Интересно │
                              └────┴─────────┴───────────┘
```

- Комментарии 1 и 2 привязаны к посту с `id=1`
- Комментарий 3 — к посту с `id=2`

**Как пользоваться в коде:**

```python
# Прямая связь (Comment → Post)
comment = Comment.objects.first()
comment.post.title          # заголовок поста этого комментария

# Обратная связь (Post → Comment) через related_name
post = Post.objects.first()
post.comments.all()         # все комментарии к посту
post.comments.count()       # количество комментариев
post.comments.filter(is_active=True)  # только активные
```

> Без `related_name='comments'` пришлось бы писать `post.comment_set.all()` — работает, но менее читаемо.

#### Meta в Comment — те же правила

```python
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']
```

| Параметр | Отличие от Post |
|----------|-----------------|
| `ordering = ['created_at']` | **Без минуса** — комментарии от **старых к новым** (как в обычном чате). У Post было `'-created_at'` — новые посты сверху |

> **Важно:** `comments` импортирует `Post` из `posts.models`. Поэтому `posts` должен быть **выше** `comments` в `INSTALLED_APPS`.

📖 **Документация Django:**
- [Related objects (обратные связи, `related_name`)](https://docs.djangoproject.com/en/stable/topics/db/queries/#related-objects)
- [Lookups spanning relationships (`post__title`)](https://docs.djangoproject.com/en/stable/topics/db/queries/#lookups-that-span-relationships)
- [Models across apps (`related_name`)](https://docs.djangoproject.com/en/stable/topics/db/models/#be-careful-with-related-name-and-related-query-name)

### Итоговая схема приложений

```
blog/                  ← проект (конфигурация)
├── settings.py        ← PostgreSQL + posts + comments
└── urls.py

posts/                 ← сущность Post
├── models.py          ← class Post
├── views.py
├── admin.py
└── templates/posts/

comments/              ← сущность Comment
├── models.py          ← class Comment (ForeignKey → Post)
└── admin.py
```

---

## 11. Миграции и manage-команды

**Миграция** — Python-файл с инструкциями: «создай таблицу», «добавь столбец», «удали поле». Django отслеживает, какие миграции уже применены, и выполняет только новые.

### Две команды — две разные задачи

| Команда | Что делает | Аналогия |
|---------|------------|----------|
| `makemigrations` | Смотрит на `models.py`, **генерирует** файл миграции | Архитектор рисует чертёж |
| `migrate` | **Выполняет** миграции в базе данных | Строители строят по чертежу |

**Важно:** `makemigrations` **не трогает** базу данных. Только создаёт файл в папке `migrations/`.  
`migrate` — **реально создаёт/меняет** таблицы в PostgreSQL.

Модели описаны — превращаем их в таблицы **в PostgreSQL**.

### Шаг 11.1. Создать миграции

```bash
python manage.py makemigrations
```

Ожидаемый вывод:

```
Migrations for 'posts':
  posts/migrations/0001_initial.py
    + Create model Post
Migrations for 'comments':
  comments/migrations/0001_initial.py
    + Create model Comment
```

Django создал **отдельные миграции для каждого приложения**.

**Что внутри файла миграции?** Откройте `posts/migrations/0001_initial.py` — увидите Python-код с операциями `CreateModel`, `AddField` и т.д. Эти файлы **можно коммитить** в git — так вся команда получает одинаковую структуру БД.

**Почему `0001`?** Номер версии миграции. Если позже добавите поле `slug` к Post — появится `0002_post_slug.py`. Django применяет их по порядку.

### Шаг 11.2. Применить миграции

```bash
python manage.py migrate
```

Django создаст в PostgreSQL:
- `posts_post` — таблица постов
- `comments_comment` — таблица комментариев

**Почему такие имена таблиц?** `<приложение>_<модель>` в нижнем регистре. Можно переопределить через `class Meta: db_table = 'my_posts'`, но обычно не нужно.

### Шаг 11.3. Посмотреть SQL миграции (опционально)

```bash
python manage.py sqlmigrate posts 0001
python manage.py sqlmigrate comments 0001
```

Показывает SQL-команды, которые выполнит миграция в PostgreSQL.

### Шаг 11.4. Проверить статус миграций

```bash
python manage.py showmigrations
```

Все приложения должны быть `[X]`.

### Шаг 11.5. Проверить таблицы в PostgreSQL (опционально)

```bash
psql -U blog_user -d blog_db -h localhost -c "\dt"
```

Теперь в списке должны быть `posts_post` и `comments_comment`.

📖 **Документация Django:**
- [Migrations (обзор)](https://docs.djangoproject.com/en/stable/topics/migrations/)
- [`makemigrations`](https://docs.djangoproject.com/en/stable/ref/django-admin/#makemigrations)
- [`migrate`](https://docs.djangoproject.com/en/stable/ref/django-admin/#migrate)
- [`showmigrations`](https://docs.djangoproject.com/en/stable/ref/django-admin/#showmigrations)
- [`sqlmigrate`](https://docs.djangoproject.com/en/stable/ref/django-admin/#sqlmigrate)
- [Migration operations reference](https://docs.djangoproject.com/en/stable/ref/migration-operations/)

---

**Админ-панель** — готовый интерфейс для управления данными. Одно из главных преимуществ Django.

### Шаг 12.1. Создать суперпользователя

```bash
python manage.py createsuperuser
```

Введите:
- Username: `admin`
- Email: (можно оставить пустым)
- Password: придумайте пароль (минимум 8 символов, не слишком простой)

> Пользователь сохраняется в PostgreSQL (таблица `auth_user`), которую мы создали на шаге 8.3.

### Шаг 12.2. Зарегистрировать Post в админке

Django **не показывает** модели в админке автоматически. Нужно явно «зарегистрировать» — сказать: «эту модель можно редактировать через /admin/».

Откройте `posts/admin.py`:

```python
from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at', 'author')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    date_hierarchy = 'created_at'
```

**Разбор кода:**

| Строка | Объяснение |
|--------|------------|
| `from .models import Post` | Точка `.` = «из текущего приложения». Импортируем модель Post |
| `@admin.register(Post)` | **Декоратор** — регистрирует модель Post в админке. Альтернатива: `admin.site.register(Post, PostAdmin)` |
| `class PostAdmin(admin.ModelAdmin)` | Класс настроек отображения Post в админке |
| `list_display` | Какие **столбцы** показать в списке постов |
| `list_filter` | **Фильтры** справа (по статусу, дате, автору) |
| `search_fields` | По каким полям **искать** (строка поиска сверху) |
| `list_editable` | Какие поля можно **редактировать прямо в списке**, не заходя внутрь |
| `date_hierarchy` | **Навигация по датам** сверху (год → месяц → день) |

### Шаг 12.3. Зарегистрировать Comment в админке

Откройте `comments/admin.py`:

```python
from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'author')
    search_fields = ('text', 'post__title')
    list_editable = ('is_active',)
```

| Настройка | Что делает |
|-----------|------------|
| `list_display` | Колонки в списке |
| `list_filter` | Фильтры справа |
| `search_fields` | Поиск (`post__title` — по связанному полю) |
| `list_editable` | Редактирование прямо в списке |

**Что значит `post__title`?** Двойное подчёркивание `__` в Django — «перейди по связи ForeignKey». Comment → Post → title. То есть можно искать комментарии по **заголовку поста**, к которому они привязаны.

### Шаг 12.4. Запустить сервер и зайти в админку

```bash
python manage.py runserver
```

Откройте: http://127.0.0.1:8000/admin/

Войдите как `admin` с вашим паролем.

В админке **два раздела от двух приложений**:
- **Posts → Посты**
- **Comments → Комментарии**

### Шаг 12.5. Создать тестовые данные

1. **Posts → Посты → Добавить** — создайте 2–3 поста
2. **Comments → Комментарии → Добавить** — добавьте комментарии к постам

### Шаг 12.6. Проверить через Django shell

```bash
python manage.py shell
```

```python
from posts.models import Post
from comments.models import Comment

Post.objects.count()
Comment.objects.count()
post = Post.objects.first()
post.comments.all()
exit()
```

📖 **Документация Django:**
- [The Django admin site](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [`ModelAdmin` options (`list_display`, `list_filter`...)](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#modeladmin-options)
- [`createsuperuser`](https://docs.djangoproject.com/en/stable/ref/django-admin/#createsuperuser)
- [Django shell](https://docs.djangoproject.com/en/stable/ref/django-admin/#shell)

---

### Что такое View

**View** — функция (или класс), которая:
1. Получает **HTTP-запрос** от браузера (`request`)
2. Достаёт данные из базы (через модели)
3. Возвращает **HTTP-ответ** — обычно HTML-страницу

```
Браузер: GET /1/  →  urls.py  →  post_detail(request, pk=1)  →  HTML
```

Views для постов — в **`posts`**. Комментарии на странице поста подтягиваются из **`comments`** через обратную связь `post.comments`.

### Шаг 13.1. Написать views в posts

Откройте `posts/views.py`:

```python
from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    """Список опубликованных постов."""
    posts = Post.objects.filter(is_published=True)
    context = {
        'posts': posts,
        'page_title': 'Блог',
    }
    return render(request, 'posts/post_list.html', context)


def post_detail(request, pk):
    """Детальная страница одного поста с комментариями."""
    post = get_object_or_404(Post, pk=pk, is_published=True)
    comments = post.comments.filter(is_active=True)
    context = {
        'post': post,
        'comments': comments,
        'page_title': post.title,
    }
    return render(request, 'posts/post_detail.html', context)
```

**Разбор `post_list`:**

| Строка | Объяснение |
|--------|------------|
| `def post_list(request):` | View **всегда** принимает `request` — объект с данными запроса (метод GET/POST, cookies, пользователь...) |
| `Post.objects.filter(is_published=True)` | ORM-запрос: «дай все посты, где is_published=True». Аналог SQL: `SELECT * FROM posts_post WHERE is_published = true` |
| `context = {'posts': posts, ...}` | **Словарь данных** для шаблона. Ключ `posts` → переменная `{{ posts }}` в HTML |
| `return render(request, 'posts/post_list.html', context)` | Взять шаблон, подставить данные из context, вернуть готовый HTML |

**Разбор `post_detail`:**

| Строка | Объяснение |
|--------|------------|
| `def post_detail(request, pk):` | `pk` — primary key (id поста). Приходит из URL: `/1/` → `pk=1` |
| `get_object_or_404(Post, pk=pk, is_published=True)` | Найти пост по id. Если не найден или не опубликован → **404 страница** (не ошибка 500) |
| `post.comments.filter(is_active=True)` | Обратная связь через `related_name='comments'`. Все **активные** комментарии к этому посту |

`post.comments.filter(...)` — обратная связь через `related_name`. Приложение `posts` **не импортирует** модель Comment — Django знает о связи через ForeignKey.

### Шаг 13.2. URL приложения posts

Создайте файл `posts/urls.py`:

```python
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
]
```

| URL | View | name |
|-----|------|------|
| `/` | post_list | posts:post_list |
| `/1/` | post_detail | posts:post_detail |

**Разбор `urls.py`:**

| Строка | Объяснение |
|--------|------------|
| `app_name = 'posts'` | **Namespace** — пространство имён URL. Позволяет разным приложениям иметь одинаковые имена (`post_list` в posts и в news) |
| `path('', views.post_list, ...)` | URL `/` (корень сайта) → функция `post_list` |
| `path('<int:pk>/', ...)` | URL `/1/`, `/2/`... `<int:pk>` — захват числа из URL и передача в view как аргумент `pk` |
| `name='post_list'` | Имя маршрута. Используется в шаблонах: `{% url 'posts:post_list' %}` → `/` |

**Зачем `app_name`?** Если позже добавите приложение `news` с таким же `name='post_list'`, без namespace будет конфликт. С namespace: `posts:post_list` и `news:post_list` — разные маршруты.

### Шаг 13.3. Подключить URL к проекту

Откройте `blog/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
]
```

Проект `blog` делегирует маршрутизацию приложению `posts`.

📖 **Документация Django:**
- [Writing views](https://docs.djangoproject.com/en/stable/topics/http/views/)
- [URL dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)
- [`path()` / `include()`](https://docs.djangoproject.com/en/stable/ref/urls/)
- [`get_object_or_404`](https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#get-object-or-404)
- [Making queries (`filter`, `all`)](https://docs.djangoproject.com/en/stable/topics/db/queries/)
- [QuerySet API reference](https://docs.djangoproject.com/en/stable/ref/models/querysets/)

---

**Шаблон** — HTML-файл с «дырками», куда Django подставляет данные из view.

```html
<h1>{{ post.title }}</h1>          ← подставится заголовок
{% for comment in comments %}     ← цикл по комментариям
    <p>{{ comment.text }}</p>
{% endfor %}
```

Шаблоны лежат в приложении `posts`.

### Шаг 14.1. Создать папки

```bash
mkdir -p posts/templates/posts
```

> Convention Django: `posts/templates/posts/` — чтобы имена шаблонов не пересекались между приложениями.

**Почему две папки `posts`?** Django ищет шаблоны во всех папках `templates/` приложений из `INSTALLED_APPS`. Если в `posts` и `comments` оба положить `base.html` — конфликт. Поэтому добавляют подпапку с именем приложения: `posts/base.html`, `comments/base.html`.

### Шаг 14.2. Базовый шаблон

Создайте `posts/templates/posts/base.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ page_title|default:"Блог" }}{% endblock %}</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: system-ui, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            color: #333;
        }
        header { border-bottom: 2px solid #333; margin-bottom: 2rem; padding-bottom: 1rem; }
        header a { color: #333; text-decoration: none; font-size: 1.5rem; font-weight: bold; }
        .post-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        .post-card h2 { margin-bottom: 0.5rem; }
        .post-card a { color: #0066cc; }
        .meta { color: #666; font-size: 0.9rem; margin-top: 0.5rem; }
        .content { margin-top: 1.5rem; }
        .comments { margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #ddd; }
        .comment {
            background: #f9f9f9;
            border-radius: 6px;
            padding: 1rem;
            margin-bottom: 0.75rem;
        }
        footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #ddd; color: #666; }
    </style>
</head>
<body>
    <header>
        <a href="{% url 'posts:post_list' %}">📝 Мой Блог</a>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>Django Blog — учебный проект</p>
    </footer>
</body>
</html>
```

### Шаг 14.3. Список постов

Создайте `posts/templates/posts/post_list.html`:

```html
{% extends 'posts/base.html' %}

{% block title %}{{ page_title }}{% endblock %}

{% block content %}
<h1>Все посты</h1>

{% if posts %}
    {% for post in posts %}
    <article class="post-card">
        <h2>
            <a href="{% url 'posts:post_detail' post.pk %}">{{ post.title }}</a>
        </h2>
        <p>{{ post.content|truncatewords:30 }}</p>
        <p class="meta">
            Автор: {{ post.author.username }} |
            {{ post.created_at|date:"d.m.Y H:i" }} |
            Комментариев: {{ post.comments.count }}
        </p>
    </article>
    {% endfor %}
{% else %}
    <p>Пока нет опубликованных постов. Добавьте их в <a href="/admin/">админке</a>.</p>
{% endif %}
{% endblock %}
```

### Шаг 14.4. Страница поста с комментариями

Создайте `posts/templates/posts/post_detail.html`:

```html
{% extends 'posts/base.html' %}

{% block title %}{{ post.title }}{% endblock %}

{% block content %}
<article>
    <h1>{{ post.title }}</h1>
    <p class="meta">
        Автор: {{ post.author.username }} |
        Опубликовано: {{ post.created_at|date:"d.m.Y H:i" }}
        {% if post.updated_at != post.created_at %}
        | Обновлено: {{ post.updated_at|date:"d.m.Y H:i" }}
        {% endif %}
    </p>
    <div class="content">
        {{ post.content|linebreaks }}
    </div>
</article>

<section class="comments">
    <h2>Комментарии ({{ comments.count }})</h2>

    {% if comments %}
        {% for comment in comments %}
        <div class="comment">
            <p>{{ comment.text|linebreaks }}</p>
            <p class="meta">
                {{ comment.author.username }} |
                {{ comment.created_at|date:"d.m.Y H:i" }}
            </p>
        </div>
        {% endfor %}
    {% else %}
        <p>Комментариев пока нет.</p>
    {% endif %}
</section>

<p><a href="{% url 'posts:post_list' %}">← Назад к списку</a></p>
{% endblock %}
```

**Разбор синтаксиса шаблонов:**

| Конструкция | Что делает | Пример |
|-------------|------------|--------|
| `{% extends 'posts/base.html' %}` | Наследование — «взять base.html как каркас» | Общий header/footer не дублируем |
| `{% block content %}` | «Дырка», которую дочерний шаблон заполняет | В base — пустой block, в post_list — контент |
| `{{ post.title }}` | Вывести значение переменной | Заголовок поста |
| `{{ post.content\|truncatewords:30 }}` | **Фильтр** — обрезать до 30 слов | Для превью в списке |
| `{{ post.created_at\|date:"d.m.Y H:i" }}` | Фильтр форматирования даты | `02.07.2026 15:30` |
| `{% for post in posts %}` | Цикл по списку | Перебрать все посты |
| `{% if posts %}` | Условие | Показать блок, если посты есть |
| `{% url 'posts:post_detail' post.pk %}` | Сгенерировать URL по имени | `/1/` вместо hardcode |
| `{{ post.comments.count }}` | Вызов метода/связи | Количество комментариев |

**`|`** — это **фильтр** (pipe). `{{ value|filter }}` — «возьми value и пропусти через filter». Как `|` в Linux: `cat file | grep word`.

### Шаг 14.5. Запустить и проверить

```bash
python manage.py runserver
```

- http://127.0.0.1:8000/ — список постов
- http://127.0.0.1:8000/1/ — первый пост с комментариями
- http://127.0.0.1:8000/admin/ — админка (Posts + Comments)

📖 **Документация Django:**
- [Templates (обзор)](https://docs.djangoproject.com/en/stable/topics/templates/)
- [The Django template language](https://docs.djangoproject.com/en/stable/ref/templates/language/)
- [Built-in template tags and filters (`for`, `if`, `url`, `extends`...)](https://docs.djangoproject.com/en/stable/ref/templates/builtins/)
- [Template inheritance (`extends`, `block`)](https://docs.djangoproject.com/en/stable/ref/templates/language/#template-inheritance)

---

| Команда | Описание |
|---------|----------|
| `python manage.py runserver` | Запуск dev-сервера |
| `python manage.py startapp <name>` | Создать приложение |
| `python manage.py makemigrations` | Создать файлы миграций |
| `python manage.py migrate` | Применить миграции к БД |
| `python manage.py showmigrations` | Статус миграций |
| `python manage.py sqlmigrate posts 0001` | SQL конкретной миграции |
| `python manage.py check --database default` | Проверка подключения к БД |
| `python manage.py createsuperuser` | Создать admin-пользователя |
| `python manage.py shell` | Python-консоль с Django |
| `python manage.py check` | Проверка проекта на ошибки |
| `python manage.py dumpdata posts comments` | Экспорт данных в JSON |
| `python manage.py loaddata file.json` | Импорт данных |
| `python manage.py collectstatic` | Сбор статики (production) |
| `python manage.py test` | Запуск тестов |
| `python manage.py flush` | ⚠️ Очистить всю БД |
| `python manage.py --help` | Список всех команд |

### django-admin vs manage.py

| | django-admin | manage.py |
|---|---|---|
| Где | Глобально (venv) | Внутри проекта |
| Задача | Создать проект | Управлять проектом |
| Пример | `django-admin startproject blog` | `python manage.py migrate` |

### Два этапа migrate на занятии

| Когда | Команда | Что создаётся |
|-------|---------|---------------|
| После подключения PostgreSQL (§8) | `migrate` | Системные таблицы Django |
| После создания моделей (§11) | `makemigrations` + `migrate` | `posts_post`, `comments_comment` |

📖 **Документация Django:**
- [Полный справочник `django-admin` / `manage.py`](https://docs.djangoproject.com/en/stable/ref/django-admin/)

---

```
TMS_django/
├── .env                        # секреты (НЕ в git)
├── .env.example                # шаблон переменных
├── .gitignore
├── requirements.txt
├── manage.py
│
├── blog/                       # ПРОЕКТ — конфигурация сайта
│   ├── __init__.py
│   ├── settings.py             # .env + PostgreSQL + INSTALLED_APPS
│   ├── urls.py                 # include('posts.urls')
│   ├── wsgi.py
│   └── asgi.py
│
├── posts/                      # ПРИЛОЖЕНИЕ — сущность Post
│   ├── admin.py                # PostAdmin
│   ├── models.py               # class Post
│   ├── views.py                # post_list, post_detail
│   ├── urls.py
│   ├── migrations/
│   │   └── 0001_initial.py
│   └── templates/posts/
│       ├── base.html
│       ├── post_list.html
│       └── post_detail.html
│
├── comments/                   # ПРИЛОЖЕНИЕ — сущность Comment
│   ├── admin.py                # CommentAdmin
│   ├── models.py               # class Comment (FK → Post)
│   ├── migrations/
│   │   └── 0001_initial.py
│   └── views.py
│
└── venv/
```

Все данные хранятся в **PostgreSQL** (`blog_db`), файла `db.sqlite3` нет.

---

## 17. Что изучили на занятии

### Теоретические понятия

| Понятие | Что это |
|---------|---------|
| **Проект** | Конфигурация всего сайта (`blog/`: settings, urls) |
| **Приложение** | Модуль одной сущности (`posts/`, `comments/`) |
| **Manage-команды** | CLI-управление через `manage.py` |
| **django-admin** | Утилита создания проектов |
| **Панель администратора** | `/admin/` — CRUD без написания UI |
| **Переменные окружения** | Секреты в `.env`, не в коде |

### Практические навыки (в порядке выполнения)

- [x] Создали виртуальное окружение и установили Django
- [x] Создали **проект** `blog`
- [x] Настроили **`.env`** и переменные окружения
- [x] **Подключили PostgreSQL** до создания моделей
- [x] Применили системные миграции в PostgreSQL
- [x] Создали **приложение** `posts` (сущность Post)
- [x] Создали **приложение** `comments` (сущность Comment)
- [x] Выполнили миграции моделей в PostgreSQL
- [x] Настроили админ-панель
- [x] Сделали views, URLs и шаблоны
- [x] Запустили рабочий блог

---

## Домашнее задание (опционально)

1. Создать приложение `categories` с моделью Category и связать с Post
2. Добавить поле `slug` к модели Post (ЧПУ-ссылки)
3. Создать приложение `tags` с моделью Tag (ManyToMany с Post)
4. Перенести отображение комментариев в отдельный view внутри `comments`

---

## Быстрый старт с нуля (шпаргалка)

```bash
cd TMS_django
python3 -m venv venv
source venv/bin/activate          # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env              # заполнить значения PostgreSQL
python manage.py migrate          # системные таблицы
# ... создать apps, models ...
python manage.py makemigrations
python manage.py migrate          # таблицы posts, comments
python manage.py createsuperuser
python manage.py runserver
```

---

## Полезные ссылки

### Официальная документация Django (по темам занятия)

| Тема занятия | Ссылка |
|--------------|--------|
| Обзор, первые шаги | [Django documentation](https://docs.djangoproject.com/en/stable/) |
| Официальный Tutorial | [Writing your first Django app](https://docs.djangoproject.com/en/stable/intro/tutorial01/) |
| Проект vs приложение | [Reusable apps](https://docs.djangoproject.com/en/stable/intro/reusable-apps/) |
| `settings.py` | [Settings reference](https://docs.djangoproject.com/en/stable/ref/settings/) |
| PostgreSQL | [Databases: PostgreSQL](https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes) |
| Модели, поля, `Meta` | [Models](https://docs.djangoproject.com/en/stable/topics/db/models/) · [Fields](https://docs.djangoproject.com/en/stable/ref/models/fields/) · [Meta options](https://docs.djangoproject.com/en/stable/ref/models/options/) |
| Связи (`ForeignKey`) | [Related objects](https://docs.djangoproject.com/en/stable/topics/db/queries/#related-objects) |
| Миграции | [Migrations](https://docs.djangoproject.com/en/stable/topics/migrations/) |
| Админка | [Admin site](https://docs.djangoproject.com/en/stable/ref/contrib/admin/) |
| Views и URL | [Views](https://docs.djangoproject.com/en/stable/topics/http/views/) · [URLs](https://docs.djangoproject.com/en/stable/topics/http/urls/) |
| Шаблоны | [Templates](https://docs.djangoproject.com/en/stable/topics/templates/) · [Template language](https://docs.djangoproject.com/en/stable/ref/templates/language/) |
| Manage-команды | [`django-admin` reference](https://docs.djangoproject.com/en/stable/ref/django-admin/) |
| Безопасность / деплой | [Deployment checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/) |

### Другие ресурсы

- [Документация psycopg2](https://www.psycopg.org/docs/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
