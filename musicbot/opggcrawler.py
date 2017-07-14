import requests
from bs4 import BeautifulSoup

tier_league = [
  'Bronze',
  'Silver',
  'Gold',
  'Platinum',
  'Diamond'
]

non_tier_league = [
  'Master',
  'Challenger'
]

class OPGGCrawler:

  def get_mmr(self, name):
    url = 'https://na.op.gg/summoner/ajax/mmr/summonerName={}'.format(name)
    r = requests.get(url)
    #TODO: status_code handling
    result = ''
    soup = BeautifulSoup(r.text, "html.parser")
    obj_mmr = self.get_mmr_from_html(soup)
    obj_avg_mmr = self.get_avg_mmr_from_html(soup)

    if (obj_mmr is None):
      return 'MMR Not available.'
    else:
      mmr = self.remove_space_tab(obj_mmr.string)
      result += 'Current MMR: {}'.format(mmr)

    if (obj_avg_mmr is not None):
      avg_mmr = self.remove_space_tab(obj_avg_mmr.string)
      avg_mmr = avg_mmr.split(' ')
      for league in non_tier_league:
        if (league in avg_mmr):
          result += ' | ' + ' '.join(avg_mmr)
          return result

      for league in tier_league:
        if (league in avg_mmr):
          rank_index = avg_mmr.index(league) + 1
          roman_rank = self.get_roman_rank(avg_mmr[rank_index])
          avg_mmr[rank_index] = roman_rank
          result += ' | ' + ' '.join(avg_mmr)

    return result

  def remove_space_tab(self, string):
    result = string.replace('\n', '')
    result = result.replace('\t', '')
    return result

  def get_mmr_from_html(self, soup):
    return soup.find('td', class_='MMR')

  def get_avg_mmr_from_html(self, soup):
    return soup.find('span', class_='InlineMiddle')

  def get_roman_rank(self, rank):
    result = {
      '1': 'I',
      '2': 'II',
      '3': 'III',
      '4': 'IV',
      '5': 'V'
    }
    return result[rank]
'''
c = OPGGCrawler()
print(c.get_mmr('voyboy'))
'''
