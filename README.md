# PlayDraft

Code challenge for PlayDraft. Display basketball/baseball/football player info in JSON format

## How to Use
1. Install Python 3.6
2. Create a new virtualenv (```virtualenv venv```)
3. Activate the virtualenv (```source venv/bin/activate```)
4. Run ```pip install -r requirements.txt``` to install dependencies
5. Run ```python app.py```
6. Connect to ```localhost:5000``` from web browser
7. Follow API Endpoint to desired resource. See below

API Endpoints to follow:

To get all players by type of sport: /api/players/all/[SPORT_TYPE]

To get specific player info by player name brief: /api/players/[NAME_BRIEF]
