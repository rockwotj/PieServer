from movie_quotes.framework.server.server import PieServer
from movie_quotes.main import app
from movie_quotes.framework import database
import os

if os.path.isfile("movie_quotes.db"):
    PieServer(app).run()
else:
    conn , c = database.connect("movie_quotes.db")
    database.create_table("moviequotes", ["movie","quote"], c)
    database.create_entry("moviequotes", ["movie","quote"], ["tyler", "i dont care"], c)
    database.close(conn)
    PieServer(app).run()
