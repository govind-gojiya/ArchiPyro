# ArchiPyro 🔥

> **Forge scalable Python backend architectures in seconds.**

[![PyPI version](https://badge.fury.io/py/archipyro.svg)](https://badge.fury.io/py/archipyro)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/archipyro.svg)](https://pypi.org/project/archipyro/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**ArchiPyro** is a powerful CLI tool designed to help developers quickly scaffold backend projects with **Clean Architecture**, **MVC**, or **Minimal** patterns, enforcing best practices, consistency, and scalability from day one.

Whether you prefer **Flask** or **FastAPI**, ArchiPyro generates a production-ready foundation with optional integrations for databases, caching, background tasks, and more.

---

## 🚀 Features

- **Multi-Framework Support**: First-class support for both **Flask** and **FastAPI**.
- **Multiple Architectures**: Choose from **Clean Architecture**, **MVC**, or **Minimal** patterns.
- **Database Ready**: Built-in support for **PostgreSQL**, **MySQL**, **MongoDB**, and **SQLite**.
- **Interactive CLI**: Easy-to-use prompts for project initialization and component generation.
- **Incremental Generation**: Add services, models, and routes as your project grows.
- **Auto Route Registration**: New routes automatically register in your application.
- **Infrastructure Scaffolding**: Auto-generate **Docker**, **docker-compose**, **CI/CD workflows**, and **Logging** configurations.
- **Best Practices**: Includes type hinting, structured logging, PascalCase naming, and environment configuration management.

---

## 📦 Installation

Install ArchiPyro via pip:

```bash
pip install archipyro
```

---

## ⚡ Quick Start

### 1. Initialize a New Project

Run the `init` command to start the interactive wizard:

```bash
archipyro init
```

You will be prompted to select:
- **Framework**: Flask or FastAPI
- **Architecture**: Clean Architecture, MVC, or Minimal
- **Database**: PostgreSQL, MySQL, MongoDB, SQLite, or None
- **Optional Features**: Docker, CI/CD, Redis, Celery, JWT Auth, etc.

### 2. Explore the Structure

ArchiPyro generates a structured project layout. For example, a **FastAPI** project with **Clean Architecture**:

```text
my_project/
├── app/
│   ├── main.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   ├── services/
│   ├── repositories/
│   │   └── base_repository.py
│   ├── routes/
│   ├── utils/
│   │   └── email.py
│   └── dependencies/
│       └── db.py
├── .env
└── README.md
```

**Flask MVC** structure:
```text
my_project/
├── run.py
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── routes/
│   ├── models/
│   ├── templates/
│   └── static/
└── requirements.txt
```

**Minimal** structure (single file):
```text
my_project/
├── app.py          # Flask
# or
├── main.py         # FastAPI
└── requirements.txt
```

---

## 🛠 Usage Guide

### Adding Components

Once your project is initialized, use the `add` command to generate new components.

**Add a Service:**
```bash
archipyro add service user
# Creates app/services/user_service.py
```

**Add a Repository:**
```bash
archipyro add repository user
# Creates app/repositories/user_repository.py
```

**Add a Model:**
```bash
archipyro add model user
# Creates app/models/user.py
```

**Add a Route/Router:**
```bash
archipyro add route auth
# Creates app/routes/auth.py (Flask) or app/routes/auth.py (FastAPI)
# Automatically registers in your app!
```

**Add a Complete Resource (Recommended):**
```bash
archipyro add resource product
# Creates Model + Repository + Service + Route in one command
# Perfect for vertical slice architecture
```

### Generating Infrastructure

Use the `gen` command to add infrastructure files if you skipped them during init.

**Generate Docker Config:**
```bash
archipyro gen docker
```

**Generate CI/CD Workflow:**
```bash
archipyro gen ci
```

---

## ✨ Key Features

### 🔐 Authentication Ready
When JWT/Auth is selected, get ready-to-use authentication with:
- User model with password hashing
- Login/Register endpoints
- JWT token generation and validation
- Protected route decorators

### 📧 Email Service
Includes `app/utils/email.py` with `send_email()` function:
- Integrates with Flask-Mail or fastapi-mail
- Dummy implementation when Mail Service is not selected

### 🔄 Automatic Route Registration
New routes are automatically registered:
- **Flask**: Added to `app/__init__.py` as blueprints
- **FastAPI**: Included in `app/main.py` as routers

### 🎨 Smart Naming
Handles snake_case input correctly:
- Input: `order_item`
- Generated: `OrderItemService`, `OrderItemRepository`, `OrderItem`

### 🗃️ Database Drivers
Automatically includes required drivers:
- PostgreSQL: `psycopg2-binary`
- MySQL: `pymysql`
- MongoDB: `mongoengine`

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for Python developers who value clean code and best practices.**
