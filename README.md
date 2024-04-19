# KALZAK BOT 🎒+💩 (👽👽👽👽👽)

---

## Содержание 🔍
1. [Installation](#installation)

---

## Installation 🔧 <a id="installation"></a>

1. `git clone https://github.com/kravasos5/KALZAK_BOT`
2. Создать виртуальную среду
    1. `python3 -m venv ./<venv_name>`
    2. Активиротать виртуальную среду командой
    `\venv\Scripts\activate.bat` для Windows
    `source /venv/bin/activate` для Linux и MacOS.
3. `pip install -r requirements.txt`
4. В корне создать *.env* файл со следующей информацией:
    ```
    DB_HOST=<database_host>
    DB_PORT=<database_port>
    DB_USER=<database_user>
    DB_PASS=<database_password>
    DB_NAME=<database_name>

    MODE=DEV
    ```
    `DEV` режим для разработки, `TEST` для тестирования, но для тестов будет создан отдельный *.test.env*