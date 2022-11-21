import requests
import xml.etree.ElementTree as ET
import json
from jinja2 import BaseLoader, Environment


class Api:
    def __init__(self):
        self.url = "https://nba-prod-us-east-1-mediaops-stats.s3.amazonaws.com/NBA/liveData/scoreboard/todaysScoreboard_00.json"
        self.page = requests.get(self.url)
        self.info = (self.page, type(self.page), self.url, 'Index the tuple to access page, type, and url')
        self.data = self.page.content
        self.tree_json = json.loads(self.data)
        self.games = self.tree_json['scoreboard']['games']
        self.date = [self.tree_json['scoreboard']['gameDate']]

    def today_teams(self):
        home_today = [game['homeTeam']['teamTricode'] for game in self.games]
        away_today = [game['awayTeam']['teamTricode'] for game in self.games]
        matchups = [home_today[i]+" vs "+away_today[i] for i in range(len(home_today))]
        return matchups, home_today, away_today

    def wins_losses(self):
        home_details = [game['homeTeam']['teamTricode']+": wins "
        +str(game['homeTeam']['wins'])+", losses "
        +str(game['homeTeam']['losses']) for game in self.games]
        away_details = [game['awayTeam']['teamTricode']
        +": wins "+str(game['awayTeam']['wins'])+", losses "
        +str(game['awayTeam']['losses']) for game in self.games]
        return home_details, away_details

    def game_leaders(self):
        home_details = [
            game['homeTeam']['teamTricode']
            +": Home Leader "+str(game['gameLeaders']['homeLeaders']['name'])+": "
            +str(game['gameLeaders']['homeLeaders']['points'])+" "
            +"pts "
            +", Away Leader (" + game['awayTeam']['teamTricode']+") "
            +str(game['gameLeaders']['awayLeaders']['name'])+": "
            +str(game['gameLeaders']['awayLeaders']['points'])
            +" pts" for game in self.games]
        return home_details

    def game_date(self):
        date = self.tree_json['scoreboard']['gameDate']
        return [date]

    def output(self):
        home_today = [game['homeTeam']['teamTricode'] for game in self.games]
        away_today = [game['awayTeam']['teamTricode'] for game in self.games]
        home_details = {'matchup_': [home_today[i]+
            " vs "+away_today[i] for i in range(len(home_today))],
            'home_':["\n"+
            game['homeTeam']['teamTricode']
            +": Home Leader "+str(game['gameLeaders']['homeLeaders']['name'])+": "
            +str(game['gameLeaders']['homeLeaders']['points'])+" "
            +"pts "
            +",\n \nAway Leader (" + game['awayTeam']['teamTricode']+") "
            +str(game['gameLeaders']['awayLeaders']['name'])+": "
            +str(game['gameLeaders']['awayLeaders']['points'])
            +" pts" for game in self.games]}
        html_template = """\
        <html>
        <head>
            <title>NBA GAMES PLAYED TODAY</title>
        </head>
        <body>
        <p>Game Date.{% for date in game_date %}
                <li>{{ date }}</li>
            {% endfor %}
        <p/>
        {% for detail, match in details.items() %}
            <tr>
            {% for matchup in match %}
                <th>{{ matchup }}</th>
            {% endfor %}
            <tr/>
        {% endfor %}
        </body>
        </html>
        """
        # jinja2 rendering
        template = Environment(loader=BaseLoader).from_string(html_template)
        template_vars = {"game_date": self.date ,"details": home_details}
        html_out = template.render(template_vars)

        return html_out



#nba= Api()
#print (nba.output())
        

