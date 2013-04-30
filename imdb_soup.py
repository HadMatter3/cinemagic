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
from noun_extract import extract_nouns
import pickle

pickle_movies = {} 
pickle_directed_by = {}
pickle_starring = {}
pickle_movie_genres = {}
pickle_description = {}       
pickled_movie_words = {}     
pickle_directors = set()
pickle_actors = set()
pickle_genres = set()
pickle_big_set = set()

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
                                        dir_count = 0
                                        movie_count = 0
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
                                                            
                                                            pickle_movies[movie_count] = str(self.title)
                                                            pickle_directed_by[movie_count] = str(self.director)
                                                            pickle_starring[movie_count] = stars
                                                            pickle_movie_genres[movie_count] = genre
                                                            pickle_description[movie_count] = str(self.description)
                                                            words = set()
                                                            words.update(extract_nouns(str(self.description)))
                                                            words.update(genre)
                                                            words.update(stars)
                                                            words.add(str(self.director))
                                                            pickled_movie_words[movie_count] = words

                                                            pickle_directors.add(self.director)
                                                            pickle_actors.update(set(stars))
                                                            pickle_genres.update(set(genre))
                                                           # big set contains the nouns of descriptions, genres, stars
                                                            pickle_big_set.update(extract_nouns(str(self.description)))
                                                            pickle_big_set.update(genre)
                                                            pickle_big_set.update(stars)
                                                            pickle_big_set.add(str(self.director))
                                                            print movie_count
                                                            print "<{},{},{},{},{},{}>".format(self.title, genre, self.director, stars, self.rating, self.description)
                                                            #print
                                                           #print
                                                            movie_count += 1
                                                        except Exception as e:
                                                            print e
                                                row_count += 1
                                table_count += 1

                        self.found = True
                        pickle_big_list = list(pickle_big_set)
                        pickle.dump(pickle_big_list, open("pickled/big_list.p", "wb"))
                        pickle.dump(pickle_movies, open("pickled/pickled_movies.p", "wb"))
                        pickle.dump(pickle_starring, open("pickled/pickled_starring.p", "wb"))
                        pickle.dump(pickle_directed_by, open("pickled/pickled_directed_by.p", "wb"))
                        pickle.dump(pickle_movie_genres, open("pickled/pickled_movie_genres.p", "wb"))
                        pickle.dump(pickle_description, open("pickled/pickled_descriptions.p", "wb"))
                        pickle.dump(pickled_movie_words, open("pickled/pickled_movie_words.p", "wb"))
                except Exception as e:
                        print e

if __name__ == "__main__":
        imdb = imdb_data()
