import requests
from bs4 import BeautifulSoup

roles = ['TOP', 'MID', 'SUPPORT', 'ADC', 'JUNGLE']
champions = ['test']
max_champs = 5

class MatchUpGGCrawler:

  def get_counter_champs(self, champ, role):
    #TODO add champ check
    result = 'Champions strong against {}: ['.format(champ.upper())
    if role.upper() not in roles:
      return 'Please check the spelling of the champion/role'
    url = 'http://matchup.gg/champion/{}/{}/'.format(champ, role)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    champs = soup.select('#champion-lookup-strong .champion-lookup-item-name')
    counter = 0
    for champ in champs:
      if (counter == max_champs):
        result += ']'
        break
      counter = counter + 1
      result += champ.string
      if (counter < max_champs):
        result += ' | '
    return result
'''
t = MatchUpGGCrawler()
print(t.get_counter_champs('swain', 'mid'))
#t.get_counter_champs('swain', 'mid')
'''