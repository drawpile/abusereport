import sys
import os

from dotenv import load_dotenv


required = object()


class Settings:
    def __init__(self, *defaults):
        self._errors = []
        for key, default in defaults:
            value = os.getenv(key)

            if value is None:
                if default is required:
                    self._errors.append(f"Environment variable {key} not set!")
                    continue
                else:
                    value = default

            setattr(self, key, value)


load_dotenv()

settings = Settings(
    ('AUTH_TOKEN', ''),            # Token shared with the Drawpile server
    ('SERVER_HOST', 'localhost'),  # Hostname of the Drawpile server
    ('DISCORD_WEBHOOK', ''),       # URL of the Discord webhook relay target
)

if settings._errors:
    for e in settings._errors:
        print(e, file=sys.stderr)
    sys.exit(1)

