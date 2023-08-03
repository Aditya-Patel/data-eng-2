"""
Aditya Patel
DE II
Homework 5
"""

import pandas as pd
import math
import sqlite3 as sql
import csv

# Connect to database using sqlite3
con = sql.connect("chinook.db")

# a) Write an SQL query to gather information about the artists, their albums, tracks, genres, and playlists. Import this information into a pandas data frame.

query = '''
    SELECT r.ArtistId, r.Name, l.AlbumId, l.Title, t.TrackId, t.Name, g.GenreId, g.Name, p.PlaylistId, p.Name
    FROM Track t
    JOIN Album l USING(AlbumId)
    JOIN Artist r USING(ArtistId)
    JOIN Genre g USING(GenreId)
    JOIN PlaylistTrack USING(TrackId)
    JOIN Playlist p USING(PlaylistId);
    '''

join_df = pd.read_sql_query(query, con)

print(join_df.head)