# Установка PostgreSQL — Windows и Ubuntu

Это руководство нужно выполнить **до** подключения PostgreSQL к Django-проекту (см. `DJANGO_GUIDE.md`, раздел «Подключение PostgreSQL»).

---

## Содержание

1. [Что такое PostgreSQL и зачем он нужен](#что-такое-postgresql-и-зачем-он-нужен)
2. [Установка на Ubuntu / Linux](#установка-на-ubuntu--linux)
3. [Установка на Windows](#установка-на-windows)
4. [Создание базы данных для проекта «Блог»](#создание-базы-данных-для-проекта-блог)
5. [Проверка подключения](#проверка-подключения)
6. [Частые проблемы](#частые-проблемы)

---

## Что такое PostgreSQL и зачем он нужен

**PostgreSQL** — реляционная СУБД (система управления базами данных). Django «из коробки» умеет работать с SQLite (файл `db.sqlite3`), но в реальных проектах почти всегда используют PostgreSQL или MySQL.

| | SQLite | PostgreSQL |
|---|---|---|
| Установка | Не нужна | Нужна отдельно |
| Для обучения | Отлично | Хорошо |
| Для продакшена | Редко | Стандарт |

На занятии мы сразу подключаем PostgreSQL к Django-проекту — до создания моделей и приложений.

---

## Установка на Ubuntu / Linux

### Шаг 1. Обновить список пакетов

```bash
sudo apt update
```

### Шаг 2. Установить PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib -y
```

- `postgresql` — сервер базы данных
- `postgresql-contrib` — дополнительные модули

### Шаг 3. Проверить, что сервис запущен

```bash
sudo systemctl status postgresql
```

Должно быть `active (running)`. Если нет:

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql   # автозапуск при загрузке
```

### Шаг 4. Узнать версию

```bash
psql --version
```

Пример вывода: `psql (PostgreSQL) 16.x`

### Шаг 5. Войти в PostgreSQL от имени системного пользователя postgres

```bash
sudo -u postgres psql
```

Вы увидите приглашение:

```
postgres=#
```

### Шаг 6. Задать пароль пользователю postgres (рекомендуется)

Внутри `psql`:

```sql
ALTER USER postgres WITH PASSWORD 'your_secure_password';
```

Замените `your_secure_password` на свой пароль. **Запишите его** — он понадобится в `.env` файле Django.

Выйти:

```sql
\q
```

### Шаг 7. (Опционально) Создать своего пользователя Linux с доступом к PostgreSQL

Если вы хотите подключаться без `sudo -u postgres`:

```bash
sudo -u postgres createuser --interactive
```

Ответьте на вопросы:
- Имя роли: ваше имя пользователя Linux (например, `artem`)
- Superuser? `y`

Задать пароль:

```bash
sudo -u postgres psql -c "ALTER USER artem WITH PASSWORD 'your_password';"
```

### Шаг 8. Установить клиент psql (если ещё не установлен)

Обычно ставится вместе с `postgresql`. Проверка:

```bash
which psql
```

---

## Установка на Windows

### Шаг 1. Скачать установщик

1. Откройте официальный сайт: https://www.postgresql.org/download/windows/
2. Нажмите **Download the installer** (через EDB)
3. Скачайте установщик для вашей версии Windows (64-bit)

Прямая ссылка на загрузку (может меняться): https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

### Шаг 2. Запустить установщик

1. Запустите `.exe` файл **от имени администратора**
2. Нажмите **Next** на экране приветствия

### Шаг 3. Выбрать компоненты

Оставьте по умолчанию:
- [x] PostgreSQL Server
- [x] pgAdmin 4 (графический интерфейс — удобно для новичков)
- [x] Stack Builder (можно снять галочку)
- [x] Command Line Tools (**обязательно** — там `psql`)

### Шаг 4. Каталог установки

По умолчанию: `C:\Program Files\PostgreSQL\16\` — можно оставить.

### Шаг 5. Задать пароль суперпользователя

- **Superuser (postgres) password** — придумайте и **запишите** пароль
- Это главный пароль для пользователя `postgres`

### Шаг 6. Порт

Оставьте **5432** (стандартный порт PostgreSQL).

### Шаг 7. Locale

Выберите **Default locale** или `Russian, Russia` — не критично для обучения.

### Шаг 8. Завершить установку

Дождитесь окончания. Снимите галочку «Launch Stack Builder», если не нужен.

### Шаг 9. Проверить установку

Откройте **PowerShell** или **cmd**:

```powershell
psql --version
```

Если команда не найдена, добавьте PostgreSQL в PATH:

1. Путь обычно: `C:\Program Files\PostgreSQL\16\bin`
2. **Параметры Windows → Система → О системе → Дополнительные параметры системы → Переменные среды**
3. В «Path» пользователя или системы добавьте путь к `bin`

### Шаг 10. Проверить, что сервис запущен

1. Нажмите `Win + R`, введите `services.msc`
2. Найдите **postgresql-x64-16** (номер версии может отличаться)
3. Статус должен быть **Running**

Или в PowerShell:

```powershell
Get-Service postgresql*
```

### Шаг 11. Войти через psql (Windows)

```powershell
psql -U postgres
```

Введите пароль, заданный при установке.

---

## Создание базы данных для проекта «Блог»

Эти команды одинаковы для Ubuntu и Windows (внутри `psql`).

### Вариант A — через командную строку (Ubuntu)

```bash
sudo -u postgres psql
```

### Вариант B — через командную строку (Windows)

```powershell
psql -U postgres
```

### Внутри psql выполните:

```sql
-- Создать базу данных для блога
CREATE DATABASE blog_db;

-- Создать отдельного пользователя для Django (хорошая практика)
CREATE USER blog_user WITH PASSWORD 'blog_password_123';

-- Выдать права на базу
GRANT ALL PRIVILEGES ON DATABASE blog_db TO blog_user;

-- В PostgreSQL 15+ нужно также выдать права на схему public
\c blog_db
GRANT ALL ON SCHEMA public TO blog_user;
GRANT CREATE ON SCHEMA public TO blog_user;

-- Проверить список баз
\l

-- Выйти
\q
```

> **Для занятия** можно использовать простые значения:
> - База: `blog_db`
> - Пользователь: `blog_user`
> - Пароль: `blog_password_123`
>
> В реальном проекте пароли должны быть сложными и храниться только в `.env`.

### Альтернатива — через pgAdmin (Windows / графический интерфейс)

1. Запустите **pgAdmin 4**
2. Подключитесь к серверу **PostgreSQL** (пароль postgres)
3. ПКМ на **Databases → Create → Database**
   - Name: `blog_db`
4. ПКМ на **Login/Group Roles → Create → Login/Group Role**
   - Name: `blog_user`
   - Вкладка **Definition**: Password: `blog_password_123`
   - Вкладка **Privileges**: Can login? Yes
5. ПКМ на `blog_db` → **Properties → Security** — добавьте `blog_user` с правами ALL

---

## Проверка подключения

### Через psql с новым пользователем

**Ubuntu:**

```bash
psql -U blog_user -d blog_db -h localhost
```

**Windows:**

```powershell
psql -U blog_user -d blog_db -h localhost
```

Пароль: `blog_password_123`

Если подключились — увидите:

```
blog_db=>
```

Проверочный запрос:

```sql
SELECT version();
\q
```

### Параметры для Django (.env)

После успешной проверки сохраните эти значения — они понадобятся в `DJANGO_GUIDE.md`:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=blog_db
DB_USER=blog_user
DB_PASSWORD=blog_password_123
DB_HOST=localhost
DB_PORT=5432
```

---

## Частые проблемы

### «connection refused» / «could not connect to server»

**Причина:** PostgreSQL не запущен.

**Ubuntu:**

```bash
sudo systemctl start postgresql
```

**Windows:** Запустите сервис `postgresql-x64-XX` в `services.msc`.

---

### «password authentication failed for user»

**Причина:** Неверный пароль или пользователь не создан.

**Решение:** Пересоздайте пароль:

```bash
sudo -u postgres psql -c "ALTER USER blog_user WITH PASSWORD 'blog_password_123';"
```

---

### «permission denied for schema public» (PostgreSQL 15+)

**Причина:** У пользователя нет прав на схему `public`.

**Решение:**

```sql
\c blog_db
GRANT ALL ON SCHEMA public TO blog_user;
GRANT CREATE ON SCHEMA public TO blog_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO blog_user;
```

---

### «psql: command not found» (Ubuntu)

```bash
sudo apt install postgresql-client -y
```

---

### «psql не является внутренней командой» (Windows)

Добавьте в PATH: `C:\Program Files\PostgreSQL\16\bin` (версия может отличаться).

---

### Порт 5432 занят

Проверьте, не запущен ли другой экземпляр PostgreSQL или Docker-контейнер:

```bash
sudo lsof -i :5432        # Linux
netstat -ano | findstr 5432   # Windows
```

---

## Чеклист перед занятием

- [ ] PostgreSQL установлен
- [ ] Сервис запущен
- [ ] База `blog_db` создана
- [ ] Пользователь `blog_user` создан с паролем
- [ ] Подключение через `psql -U blog_user -d blog_db -h localhost` работает
- [ ] Параметры записаны для `.env`

После этого переходите к **`DJANGO_GUIDE.md`**.
