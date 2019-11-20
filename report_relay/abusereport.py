import asyncio
import logging

from jsonschema import validate, ValidationError
from aiohttp import web

from .settings import settings
from . import discord

logger = logging.getLogger(__name__)

REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "session": {
            "type": "string",
            "pattern": r"[0-9a-fA-F-]+"
        },
        "sessionTitle": {"type": "string"},
        "user": {"type": "string"},
        "auth": {"type": "boolean"},
        "ip": {"type": "string"},
        "message": {"type": "string"},
        "offset": {"type": "integer"},
        "perp": {"type": "integer"},
        "users": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "auth": {"type": "boolean"},
                    "mod": {"type": "boolean"},
                    "ip": {"type": "string"},
                },
                "required": ["id", "name", "ip"]
            }
        }
    },
    "required": ["session", "sessionTitle", "user", "ip", "message", "users"]
}


async def receive_report(request):
    try:
        auth_type, auth_token = request.headers\
            .get('authorization', '').split(' ', 1)
    except ValueError:
        return web.Response(text="Bad authorization", status=401)

    if auth_type.lower() != 'token':
        return web.Response(
            text="Authorization type must be Token",
            status=401)

    if auth_token != settings.AUTH_TOKEN:
        return web.Response(text="Incorrect token", status=401)

    try:
        body = await request.json()
    except ValueError:
        return web.Response(text="Unparseable JSON", status=400)

    try:
        validate(instance=body, schema=REPORT_SCHEMA)
    except ValidationError as e:
        return web.Response(text=e.message, status=400)

    targets = []

    if settings.DISCORD_WEBHOOK:
        targets.append(discord.send_abusereport(
            settings.DISCORD_WEBHOOK,
            settings.SERVER_HOST,
            body))

    # We could support other webhook and delivery methods here,
    # such as Slack, email or a Telegram bot.

    if not targets:
        logger.warn(
            "Report from %s not relayed, because no targets were configured!",
            body['user'])

    else:
        await asyncio.gather(*targets)

        logger.info("Abuse report from %s sent to %d target(s)".format(
            body['user'],
            len(targets)
        ))

    return web.Response(status=204)

