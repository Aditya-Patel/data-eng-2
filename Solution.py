"""
Aditya Patel
DE II
Homework 1
"""

import pandas as pd
import math
import sqlite3 as sql
import csv

# ====================== PART 1 ======================

# Read in original CSVs
cast_df = pd.read_csv('cast.csv')
titles_df = pd.read_csv('titles.csv')
people_df = pd.read_csv('people.csv')

# Replace \N with math.nan
cast_cleaned_df = cast_df.replace('\\N', value=math.nan)
titles_cleaned_df = titles_df.replace('\\N', value=math.nan)
people_cleaned_df = people_df.replace('\\N', value=math.nan)

# Create updated CSVs
cast_cleaned_df.to_csv('cast_cleaned.csv', index=False)
titles_cleaned_df.to_csv('titles_cleaned.csv', index=False)
people_cleaned_df.to_csv('people_cleaned.csv', index=False)

# Create Category dataframe
category = cast_cleaned_df[['category']].squeeze().sort_values().unique()
category_df = pd.DataFrame(category)

# Create index for dataframe
category_id = []
for x in range(1, category.shape[0]+1):
    category_id.append(x)

# Add index and clean up dataset
category_df['category_id'] = category_id
category_df = category_df.rename(columns={0:"category"})
category_df = category_df[['category_id', 'category']]

# Export to csv
category_df.to_csv('category.csv', index=False)

# Convert category to ID number
cast_cleaned_df['category'].replace(category_df['category'].squeeze().tolist(),
                                    category_df['category_id'].squeeze().tolist(),
                                    inplace=True)

cast_cleaned_df.to_csv('cast_updated.csv', index=False)

# ====================== PART 2 ======================
con = sql.connect("imdb.db")
cur = con.cursor()

with open('titles.csv', 'r') as titles_table:
    dr = csv.DictReader(titles_table, delimiter = ',')
    title_to_db = [(i['tconst'], i['ordering'], i['title'], i['region'], i['language'], i['isOriginalTitle']) for i in dr]

with open('productions.csv', 'r') as productions_table:
    dr = csv.DictReader(productions_table, delimiter = ',')
    prod_to_db = [(i['tconst'], i['titleType'], i['primaryTitle'],i['originalTitle'],i['startYear'], i['endYear'], i['runtimeMinutes'],i['genres']) for i in dr]

with open('ratings.csv', 'r') as ratings_table:
    dr = csv.DictReader(ratings_table, delimiter = ',')
    ratings_to_db = [(i['tconst'], i['averageRating'], i['numVotes']) for i in dr]

with open('people.csv', 'r') as people_table:
    dr = csv.DictReader(people_table, delimiter = ',')
    people_to_db = [(i['nconst'], i['primaryName'], i['birthYear'], i['deathYear'], i['primaryProfession'], i['knownForTitles']) for i in dr]

with open('cast.csv', 'r') as cast_table:
    dr = csv.DictReader(cast_table, delimiter = ',')
    cast_to_db = [(i['tconst'],i['ordering'],i['nconst'],i['category'],i['job'],i['characters']) for i in dr]

# Convert \N to math.nan
for dataset in [title_to_db, prod_to_db, ratings_to_db, people_to_db, cast_to_db]:
    for record in range(len(dataset)):
        temp = list(dataset[record])
        temp = pd.Series(temp).replace('\\N', math.nan).to_list()
        dataset[record] = tuple(temp)

# Create tables in db
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS titles (
        TITLEID text,
        ORDERING integer, 
        TITLE text, 
        REGION text, 
        LANGUAGE text, 
        ISORIGINALTITLE integer
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS productions (
        TITLEID text, 
        TITLETYPE text, 
        PRIMARYTITLE text, 
        ORIGINALTITLE text, 
        STARTYEAR integer, 
        ENDYEAR integer, 
        RUNTIMEMINUTES integer, 
        GENRES text
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS ratings (
        TITLEID text, 
        AVERAGERATING real, 
        NUMVOTES integer
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS people (
        PEOPLEID text,
        PRIMARYNAME text, 
        BIRTHYEAR integer, 
        DEATHYEAR integer, 
        PRIMARYPROFESSION text, 
        KNOWNFORTITLES text
    )
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS cast (
        TITLEID text,
        ORDERING integer,
        PEOPLEID text,
        CATEGORY text,
        JOB text,
        CHARACTERS text
    )
    """
)

# Populate tables with datasets
cur.executemany(
    """
    INSERT INTO titles
        VALUES(?, ?, ?, ?, ?, ?);
    """,
    title_to_db
)

cur.executemany(
    """
    INSERT INTO productions 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """,
    prod_to_db
)

cur.executemany(
    """
    INSERT INTO ratings
        VALUES (?, ?, ?);
    """,
    ratings_to_db
)

cur.executemany(
    """
    INSERT INTO people
        VALUES (?, ?, ?, ?, ?, ?);
    """,
    people_to_db
)

cur.executemany(
    """
    INSERT INTO cast
        VALUES (?, ?, ?, ?, ?, ?);
    """,
    cast_to_db
)

con.commit()