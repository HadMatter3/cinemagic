"""
Natalia Woodbine
Programming Paradimgs Project

imdb_soup.py uses BeautifulSoup to visit every movie page on the IMDB Top 250 list.
It outputs a comma-seperated list of Title,[Genres],Director,[Stars],Rating,description.

"""

import re
import urllib
import urlparse

from mechanize import Browser
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

class opener(urllib.FancyURLopener):
        version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'

class imdb_data:
        title = None
        year = None
        rating = None
        description = None
        director = None
        stars = {None, None, None}
        found = False

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
                                        for row in tables.findAll('tr'):
                                                if row_count >= 1:
                                                        try:
                                                            # for every movie in the top 250 list
                                                            link = row.find(lambda tag: tag.name == 'a' and tag.has_key('href'))
                                                            follow_url = self.movieURL + str(link['href'])

                                                            # set title
                                                            self.title = link.contents[0]

                                                            # follow link to movie page
                                                            br.open(follow_url) 
                                                            movie_soup = BeautifulSoup( opener().open(follow_url).read() )

                                                            # get description
                                                            table = movie_soup.find(lambda tag: tag.name == 'table' and tag.has_key('id') and tag['id'] == 'title-overview-widget-layout')
                                                            table_desc = table.find(lambda tag: tag.name == 'p' and tag.has_key('itemprop') and tag['itemprop'] == 'description')
                                                            self.description = table_desc.contents[0]

                                                            # get director
                                                            table_dir1 = table.find(lambda tag: tag.name == 'a' and tag.has_key('itemprop') and tag['itemprop'] == 'url')
                                                            table_dir = table_dir1.find(lambda tag: tag.name == 'span' and tag.has_key('itemprop') and tag['itemprop'] == 'name')
                                                            self.director = table_dir.contents[0]

                                                            # get rating
                                                            table_rating = table.find(lambda tag: tag.name == 'span' and tag.has_key('itemprop') and tag['itemprop'] == 'ratingValue')
                                                            self.rating = table_rating.contents[0]

                                                            # get stars
                                                            stars = []
                                                            table_actors = table.find('div', {'itemprop': 'actors'})
                                                            for actor in table_actors.findAll('span'):
                                                                if actor.has_key('itemprop') and actor['itemprop'] == 'name':
                                                                    stars.append(actor.contents[0])
							    for n in range(len(stars)):
							    	stars[n] = stars[n].decode('latin-1').encode('utf-8')

                                                            # get genres
                                                            table_infobar = table.find('div', {'class': 'infobar'})
                                                            genre = []
                                                            for g in table_infobar.findAll('span'):
                                                                if g.has_key('itemprop') and g['itemprop'] == 'genre':
                                                                    genre.append(g.contents[0])
							    for n in range(len(genre)):
							    	genre[n] = genre[n].decode('latin-1').encode('utf-8')

                                                            print "{},{},{},{},{},{}".format(self.title, genre, self.director, stars, self.rating, self.description)
                                                            #print
                                                            #print
                                                        except Exception as e:
                                                            print e 
                                                row_count += 1
                                table_count += 1

                        self.found = True
                except Exception as e:
                        print e
              
if __name__ == "__main__":
        imdb = imdb_data()
