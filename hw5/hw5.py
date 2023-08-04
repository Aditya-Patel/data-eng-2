"""
Aditya Patel
DE II
Homework 5
"""

import pandas as pd
import sqlite3 as sql
import sklearn.cluster as sklc

# Connect to database using sqlite3
con = sql.connect("chinook.db")

# a) Write an SQL query to gather information about the artists, their albums, tracks, genres, and playlists. Import this information into a pandas data frame.

query = '''
    SELECT r.ArtistId, r.Name as Artist, l.AlbumId, l.Title as Album, t.TrackId, t.Name, g.GenreId, g.Name as Genre, p.PlaylistId, p.Name as Playlist
    FROM Track t
    JOIN Album l USING(AlbumId)
    JOIN Artist r USING(ArtistId)
    JOIN Genre g USING(GenreId)
    JOIN PlaylistTrack USING(TrackId)
    JOIN Playlist p USING(PlaylistId);
    '''

chinook_df = pd.read_sql_query(query, con)

# b) Select all the artists that have more than one album for the analysis below
artist_df = chinook_df.groupby(['ArtistId']).filter(lambda x: x['AlbumId'].nunique() > 1)

# c) Construct a set of ten features for each artist
# * Genres: The first seven features represent the seven most popular genres. Create a numerical feature for each of the top 7 genres that records how many songs an artist has in each genre. (Determine the top 7 genres based on the number of tracks in each genre.)
# * Number of albums: Count of how many albums the artist has in the data (note this should be > 1 based on filter above).
# * Number of tracks: Count of how many tracks each artist has.
# * Number of playlists: Number of playlists that include tracks of an artist

# Get counts from artist information
artistCounts_df = artist_df.groupby(['ArtistId', 'Artist']).agg({'AlbumId': 'nunique', 'TrackId': 'nunique', 'PlaylistId': 'nunique'}).reset_index()

# Create Genre Information
