"""
Aditya Patel
DE II
Homework 5
"""

import sqlite3 as sql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from sklearn.cluster import KMeans
from sklearn.discriminant_analysis import StandardScaler


# Connect to database using sqlite3
con = sql.connect("chinook.db")

# a) Write an SQL query to gather information about the artists, their albums, tracks, genres, and playlists. Import this information into a pandas data frame.

query = '''
    SELECT r.ArtistId,
        r.Name as Artist, 
        l.AlbumId, 
        l.Title as Album, 
        t.TrackId, 
        t.Name as Track, 
        g.GenreId, 
        g.Name as Genre, 
        p.PlaylistId, 
        p.Name as Playlist
    FROM Track t
    JOIN Album l USING(AlbumId)
    JOIN Artist r USING(ArtistId)
    JOIN Genre g USING(GenreId)
    JOIN PlaylistTrack USING(TrackId)
    JOIN Playlist p USING(PlaylistId);
    '''

music_df = pd.read_sql_query(query, con)

# b) Select all the artists that have more than one album for the analysis below
grouped_df = music_df.groupby(['ArtistId']).filter(lambda x: x['AlbumId'].nunique() > 1)

# c) Construct a set of ten features for each artist
# * Genres: The first seven features represent the seven most popular genres. Create a numerical feature for each of the top 7 genres that records how many songs an artist has in each genre. (Determine the top 7 genres based on the number of tracks in each genre.)
# * Number of albums: Count of how many albums the artist has in the data (note this should be > 1 based on filter above).
# * Number of tracks: Count of how many tracks each artist has.
# * Number of playlists: Number of playlists that include tracks of an artist

# c.1) Extract the top 7 genres based on the dataframe
top_genres = grouped_df.groupby('Genre').agg({'Track':'count'}).sort_values(['Track'], ascending=False).head(7).index

# c.2) Create subset columns to aggregate
genre_df = grouped_df.groupby(['Genre', 'ArtistId']).agg({'Track':'count'})
artist_df = grouped_df.groupby(['ArtistId', 'Artist']).agg({'Album':'nunique', 'Track':'nunique', 'Playlist':'nunique'})

# c.3 Populate coluns with values
for genre in top_genres:
    artist_df[genre] = 0
    artists = genre_df.loc[genre].index
    for artist in artists:
        track_count = int(genre_df.loc[genre, artist])
        artist_df.loc[artist, genre] = track_count

artist_df.reset_index(inplace=True)

# d) Apply k-means clustering to cluster the artists based on the features above.
# d.1) Select subset of columns to cluster by
cols = artist_df.columns.to_list()[2:] # Selects all columns except 'Artist'
kmeans_data = artist_df[cols]

# d.2) Standardize data
std_data = StandardScaler().fit_transform(kmeans_data)

# d.3) Find optimal value of K
inertia = []
k_vals = list(range(2, 12, 2))

for k in k_vals:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(std_data)
    inertia.append(kmeans.inertia_)

# Plotting
plt.plot(k_vals, inertia)
plt.xticks(k_vals)
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.show()

# e) For your chosen value of k, for each cluster, find and report the three artists that are closest to the cluster centroid. Include their names and feature values from part c.
# e.1) Fit data using optimal value of k
k_optimal = 8

kmeans = KMeans(n_clusters=k_optimal)
kmeans.fit(std_data)

cluster_labels = kmeans.labels_
closest_artists = []

for k in range(k_optimal):
    k_indices = np.where(cluster_labels == k)[0]
    k_members = std_data[k_indices]
    centroid = kmeans.cluster_centers_[k]
    distances = distance.cdist([centroid], k_members, 'euclidean')[0]
    closest = distances.argsort()[:3]
    for idx in closest:
        df_original_idx = k_indices[idx]
        closest_distance = distances[idx]
        closest_artists.append({"Artist": artist_df.iloc[df_original_idx]["Artist"], "group_num": k, "centroid_dist": closest_distance})

analysis_df = pd.DataFrame(closest_artists).merge(artist_df, on='Artist', how='left')
print(analysis_df)