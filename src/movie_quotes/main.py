
import os
import json
from framework.server.upload import Upload
from framework import pie_server
from framework import database

PATH = os.path.dirname(__file__)

class StaticFileHandler(pie_server.RequestHandler):
    def get(self):
        file = open(os.path.join(PATH, self.get_file()))
        self.response.write(file.read())

    def get_file(self):
        return 'public' + self.request.path

class IndexFileHandler(StaticFileHandler):
    def get_file(self):
        return 'public/index.html'

class ZZZZ_API(pie_server.RequestHandler):
    def get(self):
        conn, c = database.connect("movie_quotes.db")
        return_cont = database.read_all("moviequotes",c)
        database.close(conn)
        return_cont = [{'id':v[0], 'movie':v[1], 'quote':v[2]} for v in return_cont]
        self.response.write(json.dumps(return_cont))

    def post(self):
        movie = self.request.qs_lookup("movie")
        quote = self.request.qs_lookup("quote")
        conn, c = database.connect("movie_quotes.db")
        database.create_entry("moviequotes", ["movie","quote"], [movie, quote], c)
        _id = database.read_all("moviequotes",c)[-1][0]
        database.close(conn)
        self.response.write(json.dumps({'id':_id}))

    def delete(self):
        _id = self.request.qs_lookup("id")
        conn, c = database.connect("movie_quotes.db")
        database.delete_entry_by_key("moviequotes","ID", _id, c)
        database.close(conn)

    def put(self):
        movie = self.request.qs_lookup("movie")
        quote = self.request.qs_lookup("quote")
        _id = self.request.qs_lookup("id")
        conn, c = database.connect("movie_quotes.db")
        database.update_entry("moviequotes","movie",movie,"ID",_id,c)
        database.close(conn)
        conn, c = database.connect("movie_quotes.db")
        database.update_entry("moviequotes","quote",quote,"ID",_id,c)
        database.close(conn)

static_files = []
for file in os.walk(os.path.join(PATH, "public")):
    static_files += [file[0][7 + len(PATH):] + '/' + f for f in file[2]]

paths = {'/' : IndexFileHandler, '/api/moviequotes' : ZZZZ_API}

for file in static_files:
    paths[file] = StaticFileHandler

app = pie_server.App(paths)
