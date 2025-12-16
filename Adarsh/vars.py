# (c) adarsh-goel

import os
from os import getenv, environ
from dotenv import load_dotenv

load_dotenv()


class Var(object):

    # ===== BASIC =====
    MULTI_CLIENT = False

    API_ID = int(getenv("API_ID"))
    API_HASH = str(getenv("API_HASH"))
    BOT_TOKEN = str(getenv("BOT_TOKEN"))

    name = str(getenv("name", "AkkiFileStreamBot"))

    SLEEP_THRESHOLD = int(getenv("SLEEP_THRESHOLD", "60"))
    WORKERS = int(getenv("WORKERS", "4"))

    # ===== BIN CHANNEL (SAFE) =====
    _BIN = getenv("BIN_CHANNEL")
    BIN_CHANNEL = int(_BIN) if _BIN and _BIN.lstrip("-").isdigit() else None

    # ===== WEB =====
    PORT = int(getenv("PORT", "8080"))
    BIND_ADRESS = str(getenv("WEB_SERVER_BIND_ADDRESS", "0.0.0.0"))

    PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))

    # ===== OWNER =====
    OWNER_ID = set(
        int(x) for x in os.environ.get("OWNER_ID", "").split() if x.isdigit()
    )
    OWNER_USERNAME = str(getenv("OWNER_USERNAME", ""))

    # ===== HEROKU / VPS =====
    NO_PORT = bool(getenv("NO_PORT", False))
    APP_NAME = str(getenv("APP_NAME", ""))

    if "DYNO" in environ:
        ON_HEROKU = True
        APP_NAME = str(getenv("APP_NAME"))
    else:
        ON_HEROKU = False

    FQDN = (
        str(getenv("FQDN", BIND_ADRESS))
        if not ON_HEROKU or getenv("FQDN")
        else APP_NAME + ".herokuapp.com"
    )

    HAS_SSL = bool(getenv("HAS_SSL", False))

    if HAS_SSL:
        URL = f"https://{FQDN}/"
    else:
        URL = f"http://{FQDN}/"

    # ===== DATABASE =====
    DATABASE_URL = str(getenv("DATABASE_URL", ""))

    # ===== CHANNELS =====
    UPDATES_CHANNEL = str(getenv("UPDATES_CHANNEL", "-1002490871576"))

    BANNED_CHANNELS = list(
        set(
            int(x)
            for x in str(getenv("BANNED_CHANNELS", "-1002950549585")).split()
            if x.lstrip("-").isdigit()
        )
    )
