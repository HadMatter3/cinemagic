from mechanize import Browser
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re
import urllib
from urllib import urlretrieve
from urllib2 import urlopen
import urlparse
import os
import sys

movie_urls = []
class opener(urllib.FancyURLopener):
        version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'

class imdb_data:

        movieURL = "http://www.imdb.com"

        def __init__(self):
                self._scrape()

        def _scrape(self):
                br = Browser()
                TOP_URL = "http://www.imdb.com/chart/top"

                br.open(TOP_URL)
                only_table_tags = SoupStrainer("table")
                soup = BeautifulSoup(opener().open(TOP_URL).read(), parse_only = only_table_tags)
                #print soup
                try:
                        table_count = 0
                        for tables in soup.findAll('table'):
                                if table_count == 1:
                                        row_count = 0
                                        dir_count = 0
                                        movie_count = 0
                                        for row in tables.findAll('tr'):

                                                if row_count >= 1:
                                                        try:
                                                            # for every movie in the top 250 list
                                                            link = row.find(lambda tag: tag.name == 'a' and tag.has_key('href'))
                                                            follow_url = self.movieURL + str(link['href'])
                                                            br.open(follow_url)

                                                            movie_soup = BeautifulSoup( opener().open(follow_url).read() )
                                                            table = movie_soup.find(lambda tag: tag.name == 'div' and tag.has_key('id') and tag['id'] == 'title-overview-widget')
                                                            image = table.find(lambda tag: tag.name == 'td' and tag.has_key('id') and tag['id'] == 'img_primary')
                                                            image_url = image.find(lambda tag: tag.name == 'a')
                                                            # print image_url['href']
                                                            new_follow_url = self.movieURL + str(image_url['href'])
                                                            br.open(new_follow_url)
                                                            image_soup = BeautifulSoup( opener().open(new_follow_url).read() )
                                                            new_table = image_soup.find(lambda tag: tag.name == 'table' and tag.has_key('id') and tag['id'] == 'outerbody')
                                                            new_div = new_table.find(lambda tag: tag.name == 'div' and tag.has_key('id') and tag['id'] == 'canvas')
                                                            new_image = new_div.find(lambda tag: tag.name == 'img')
                                                            print new_image['src']
                                                            new_image_url = new_image["src"]
                                                            filename = "pics/" + link.contents[0] + ".jpg"
                                                            f = open(filename, 'wb')
                                                            f.write(urllib.urlopen(new_image_url).read())
                                                            f.close
                                                            # filename = new_image["src"].split("/")[-1]
                                                            # outfolder = '/pics/'
                                                            # outpath = os.path.join(outfolder, filename)
                                                            # urlretrieve(new_image_url, outfolder)
                                                            # movie_urls.append(new_image_url)
                                                        except Exception as e:
                                                            print e
                                                row_count += 1
                                table_count += 1


                except Exception as e:
                        print e

if __name__ == "__main__":
        imdb = imdb_data()
