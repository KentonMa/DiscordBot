import requests
from .opggcrawler import OPGGCrawler

queueType = 'RANKED_SOLO_5x5'

class LoLException(Exception):
  def __init__(self, error, response):
    self.error = error
    self.headers = response.headers

error_400 = "Bad request"
error_401 = "Unauthorized"
error_403 = "Blacklisted key"
error_404 = "Game data not found"
error_429 = "Too many requests"
error_500 = "Internal server error"
error_503 = "Service unavailable"
error_504 = 'Gateway timeout'

def raise_status(response):
  if response.status_code == 400:
    raise LoLException(error_400, response)
  elif response.status_code == 401:
    raise LoLException(error_401, response)
  elif response.status_code == 403:
    raise LoLException(error_403, response)
  elif response.status_code == 404:
    raise LoLException(error_404, response)
  elif response.status_code == 429:
    raise LoLException(error_429, response)
  elif response.status_code == 500:
    raise LoLException(error_500, response)
  elif response.status_code == 503:
    raise LoLException(error_503, response)
  elif response.status_code == 504:
    raise LoLException(error_504, response)
  else:
    response.raise_for_status()

class RiotApi:

  def __init__(self, key):
    self.key = key

  def base_request(self, url):
    headers = {'X-Riot-Token': self.key}
    r = requests.get(
      'https://na1.api.riotgames.com/{}'.format(url),
      headers=headers)
    raise_status(r)
    return r.json()

  def summoner_request(self, end_url):
    return self.base_request('lol/summoner/v3/summoners/{}'.format(end_url))

  def league_request(self, end_url):
    return self.base_request('lol/league/v3/{}'.format(end_url))

  def get_summoner(self, name):
    return self.summoner_request('by-name/{}'.format(name))

  def get_ranked_stats(self, name):
    try:
      summoner = self.get_summoner(name)
      stats = self.league_request(
        'positions/by-summoner/{}'.format(summoner['id']))

      for stat in stats:
        if (stat['queueType'] == queueType):
          win_percentage = (stat['wins'] / (stat['wins'] + stat['losses'])) * 100
          opgg_crawler = OPGGCrawler()
          mmr = opgg_crawler.get_mmr(stat['playerOrTeamName'])
          return '```\n{}\nRank: {} {}\nLP: {}\nWins: {} / Losses: {} (Win Rate: {:.2f}%)\n{}```More info here: https://na.op.gg/summoner/userName={}'.format(
            stat['playerOrTeamName'],
            stat['tier'],
            stat['rank'],
            stat['leaguePoints'],
            stat['wins'],
            stat['losses'],
            win_percentage,
            mmr,
            stat['playerOrTeamName'].replace(" ", "%20"))

      return '{} is not ranked.'.format(summoner['name'])
    except LoLException as err:
      return 'Error: {}.'.format(err.error)
