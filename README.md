Drawpile abuse report relay
---------------------------

This is a simple Python script that receives abuse reports from a Drawpile
server and relays them forward.

Currently, only a Discord webhook relay target is implemented.


## Installation

Python 3.7 is required. Check the `requirements.txt` file for a list of
libraries that must be installed.

To deploy as a Docker container, you can build the image by running:

	docker build -t drawpile_report_relay .

To run:

	docker run -p 8080:8080 --env-file config drawpile_report_relay 

Or check `start.sh` for an example.

The application is configured using environment variables.
Check `abusereport/settings.py` for the full list of settings, but at least
the following should be set:

 * `AUTH_TOKEN`: the token shared with drawpile-srv
 * `SERVER_HOST`: domain name of the server. This is used when generating a link to the session
 * `DISCORD_WEBHOOK`: the Discord webhook URL to use.

