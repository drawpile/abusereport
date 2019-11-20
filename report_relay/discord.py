import aiohttp
import logging


logger = logging.getLogger(__name__)


async def send_abusereport(webhook_url, server_host, report):
    embed_fields = []

    # Find details about the user being reported on
    # (if any: the report may also be about the session in general)
    if report.get('perp'):
        troller = {
            "name": f":japanese_ogre: User #{report['perp']}",
            "value": "Unknown user",
        }
        for user in report['users']:
            if user['id'] == report['perp']:
                troller = {
                    "name": f":japanese_ogre: {user['name']}",
                    "value": user['ip'],
                }
                break

        embed_fields.append(troller)

    # The user doing the reporting
    embed_fields.append({
        "name": f":cold_sweat: {report['user']}",
        "value": report["ip"]
    })

    # Construct the message
    message = {
        "embeds": [
            {
                "title": f""":bangbang: Abuse report received from {server_host} session {report["sessionTitle"] or "(Untitled session)"}""",
                "description": report["message"] + f"\nSession: drawpile://{server_host}/{report['session']}",
                "color": 16711680,
                "author": {
                    "name": report["user"],
                },
                "fields": embed_fields,
            }
        ]
    }

    # Send it to the Discord channel webhook
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=message) as response:
            if response.status not in (200, 204):
                text = await response.text()
                logger.warn(f"{webhook_url} responded with {response.status}: {text}")


