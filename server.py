import cherrypy
import json
import sys
import re
import math

movies = {}             # map movie_id:[title, rating]
directors = {}          # map director_id:name
actors = {}             # map actor_id:name
genres = []             # list of existing genres
directed_by = {}        # map movie_id:director_id
starring = {}           # map movie_id:[actor_ids]
movie_genre = {}        # movie_if:[genres]

class MovieController(object):
        def GET(self, index = None):
                output = {'result':'error'}
                if index == None: output['movies'] = get_movies()
                else: output['movie'] = get_movie(index)

                output['result'] = 'success'
                return json.dumps(output)

        def DELETE(self, index = None):
                pass
        def POST(self, index = None):
                pass
        def PUT(self, index = None):
                pass


def load_movies(filename):
        movie_file = open(filename)
        director_id, movie_id, actor_id = 0
        for line in movie_file.readlines():
                comma_split = line.rstrip('\r\n').split(',')
                left_bracket_split = line.rstrip('\r\n').split('[')



def get_movies():
        return movies

def get_movie(index):
        for item in movies:
                if str(item['id']) == str(index): return item

def start_service():
        dispatcher = cherrypy.dispatch.RoutesDispatcher()

        dispatcher.connect('movies_get', '/movies/', controller = MovieController(), action = 'GET', conditions = dict(method = ['GET']))
        dispatcher.connect('movie_get', '/movies/:index', controller = MovieController(), action = 'GET', conditions = dict(method = ['GET']))
        dispatcher.connect('movies_delete', '/movies/', controller = MovieController(), action = 'DELETE', conditions = dict(method = ['DELETE']))
        dispatcher.connect('movie_delete', '/movies/:index', controller = MovieController(), action = 'DELETE', conditions = dict(method = ['DELETE']))
        dispatcher.connect('movie_add', '/movies/:index', controller = MovieController(), action = 'PUT', conditions = dict(method = ['PUT']))
        dispatcher.connect('movies_post', '/movies/', controller = MovieController(), action = 'POST', conditions = dict(method = ['POST']))

        conf = {
                'global': {'server.socket_host': '0.0.0.0', 'server.socket_port': 8000,},
                '/': {'request.dispatch': dispatcher,}
        }
        cherrypy.config.update(conf)
        app = cherrypy.tree.mount(None, config=conf)
        cherrypy.quickstart(app)


if __name__ == '__main__':
    start_service()