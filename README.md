# Проект по бронированию для игрового клуба

## 1. Настройка виртуальной среды

### 1.1 Обновить индекс пакетов и сами пакеты
```text
sudo apt update && sudo apt upgrade -y
```

### 1.2 Установить pip
```text
sudo apt install python3-pip -y
```

### 1.3 Установить пакет виртуальной среды
```text
sudo apt install python3-venv -y
```

### 1.4 Создать виртуальную среду
```text
python3 -m venv venv
```

### 1.5 Активировать среду
```text
source test/test_env/bin/activate
```

## 2. Настройка базы данных

### 2.1 Установить PostgreSQL
```text
sudo apt install postgresql
```

### 2.2 Войти в редактор postgres
```text
sudo -u postgres psql postgres
```

### 2.3 Изменить пароль пользователя postgres
```text
ALTER USER postgres with encrypted password 'your_password';
```

### 2.5 Создать базу данных
```text
CREATE DATABASE gameclubdb;
```

### Создать пользователя базы данных для подключения 
```text
CREATE USER gameclubadmin with password 'your_password' SUPERUSER;
```

### 2.6 Выйти из редактора с помощью Ctrl+Z и перезапустить сервис 
```text
sudo systemctl restart postgresql.service
```

### 2.7 Создать файл .env с данными для доступа к БД
Пример файла .env
```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=gameclubdb
DB_USER=gameclubadmin
DB_PASS=your_password
```

## 3. Настройка backend-приложения

### 3.1 Установка uvicorn
```text
sudo apt install uvicorn
```