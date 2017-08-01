import requests
from bs4 import BeautifulSoup

class OPGGCrawler:

  def get_mmr(self, name):
    url = 'https://na.op.gg/summoner/ajax/mmr/summonerName={}'.format(name)
    try:
      r = requests.get(url)
    except requests.exceptions.RequestException as e:
      print(e)
      return 'An error occured. Could not get MMR.'

    result = ''
    soup = BeautifulSoup(r.text, "html.parser")
    obj_mmr = self.get_mmr_from_html(soup)

    if (obj_mmr is None):
      return 'MMR Not available.'
    else:
      mmr = self.remove_space_tab(obj_mmr.string)
      result += 'MMR: {}'.format(mmr)

    return result

  def remove_space_tab(self, string):
    result = string.replace('\n', '')
    result = result.replace('\t', '')
    return result

  def get_mmr_from_html(self, soup):
    return soup.find('td', class_='MMR')
