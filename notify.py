import requests
import xml.etree.ElementTree as ET
import json
from jinja2 import BaseLoader, Environment

url = "https://www.nba.com/sitemap_players.xml"
url = "https://nba-prod-us-east-1-mediaops-stats.s3.amazonaws.com/NBA/liveData/scoreboard/todaysScoreboard_00.json"




class Api:
    def __init__(self):
        self.url = url
    def loadRequest(self, url):
        page = requests.get(url)
        self.info = (page, type(page), url, 'Index the tuple to access page, type, and url')

    def parse_json(self):
        data = self.info[0].content
        self.tree_json = json.loads(data)

    def today_teams(self):
        
        games = self.tree_json['scoreboard']['games']
        home_today = [game['homeTeam']['teamTricode'] for game in games]
        away_today = [game['awayTeam']['teamTricode'] for game in games]
        matchups = [home_today[i]+" vs "+away_today[i] for i in range(len(home_today))]
        return matchups, home_today, away_today

    def wins_losses(self):
        games = self.tree_json['scoreboard']['games']
        home_details = [game['homeTeam']['teamTricode']+": wins "+str(game['homeTeam']['wins'])+", losses "+str(game['homeTeam']['losses']) for game in games]
        away_details = [game['awayTeam']['teamTricode']+": wins "+str(game['awayTeam']['wins'])+", losses "+str(game['awayTeam']['losses']) for game in games]

        return home_details, away_details

    def game_leaders(self):
        games = self.tree_json['scoreboard']['games']
        home_details = [
            game['homeTeam']['teamTricode']
            +": Home Leader "+str(game['gameLeaders']['homeLeaders']['name'])+": "
            +str(game['gameLeaders']['homeLeaders']['points'])+" "
            +"pts "
            +", Away Leader (" + game['awayTeam']['teamTricode']+") "
            +str(game['gameLeaders']['awayLeaders']['name'])+": "
            +str(game['gameLeaders']['awayLeaders']['points'])
            +" pts" for game in games]
        return(home_details)
    
    def game_date(self):
        date = self.tree_json['scoreboard']['gameDate']
        return [date]

    def output(self):
        date = [self.tree_json['scoreboard']['gameDate']]
        games = self.tree_json['scoreboard']['games']
        home_today = [game['homeTeam']['teamTricode'] for game in games]
        away_today = [game['awayTeam']['teamTricode'] for game in games]
        home_details = {'matchup_': [home_today[i]+
            " vs "+away_today[i] for i in range(len(home_today))],
            'home_':["\n"+
            game['homeTeam']['teamTricode']
            +": Home Leader "+str(game['gameLeaders']['homeLeaders']['name'])+": "
            +str(game['gameLeaders']['homeLeaders']['points'])+" "
            +"pts "
            +",\nAway Leader (" + game['awayTeam']['teamTricode']+") "
            +str(game['gameLeaders']['awayLeaders']['name'])+": "
            +str(game['gameLeaders']['awayLeaders']['points'])
            +" pts" for game in games]}
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
        template_vars = {"game_date": date ,"details": home_details}
        html_out = template.render(template_vars)

        return html_out
        
        

nba = Api()
nba.loadRequest(url)
nba.parse_json()
nba.today_teams()
nba.wins_losses()
nba.game_leaders()
print(nba.output())
#print(nba.parse_xml())