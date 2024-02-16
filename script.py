from dotenv import load_dotenv
import os
import spotipy
import pandas as pd
import numpy as np

env_path = os.path.join(
    os.path.dirname(__file__),
    '..',
    '.env')

load_dotenv(env_path)

id = os.environ.get('ID')
secret = os.environ.get('SECRET')

manager = spotipy.SpotifyClientCredentials(client_id = id, client_secret = secret)
sp = spotipy.Spotify(client_credentials_manager = manager)
sp.requests_timeout = 10

top50_countries = {
    'spain': '37i9dQZEVXbNFJfN1Vw8d9',
    'japan': '37i9dQZEVXbKXQ4mDTEBXq',
    'usa': '37i9dQZEVXbLRQDuF5jeBp',
    'morocco': '37i9dQZEVXbJU9eQpX8gPT',
    'brasil': '37i9dQZEVXbMXbN3EUUhlg',
    'italy': '37i9dQZEVXbIQnj7RRhdSX',
    'argentina': '37i9dQZEVXbMMy2roB9myp',
    'peru': '37i9dQZEVXbJfdy5b0KP7W',
    'india': '37i9dQZEVXbLZ52XmnySJg',
    'philippines': '37i9dQZEVXbNBz9cRCSFkY',
    'global': '37i9dQZEVXbMDoHDwVN2tF',
    'uk': '37i9dQZEVXbLnolsZ8PSNw',
    'germany': '37i9dQZEVXbJiZcmkrIHGU',
    'uruguay': '37i9dQZEVXbMJJi3wgRbAy',
    'france': '37i9dQZEVXbIPWwFssbupI',
    'netherlands': '37i9dQZEVXbKCF6dqVpDkS',
    'south-corea': '37i9dQZEVXbNxXF4SkHj9F',
    'chile': '37i9dQZEVXbL0GavIqMTeb',
    'mexico': '37i9dQZEVXbO3qyFxbkOE1',
    'romania': '37i9dQZEVXbNZbJ6TZelCq',
    'poland': '37i9dQZEVXbN6itCcaL3Tt',
    'australia': '37i9dQZEVXbJPcfkRz0wJ0',
    'turkey': '37i9dQZEVXbIVYVBNw9D5K',
    'ecuador': '37i9dQZEVXbJlM6nvL1nD1',
    'ireland': '37i9dQZEVXbKM896FDX8L1'}

final_df = pd.DataFrame()

for country, country_id in top50_countries.items():

    tracks = sp.playlist_items(playlist_id = country_id)

    artists_id = []

    for item in tracks['items']:
        artists_id.append(item['track']['artists'][0]['id'])
        
    df = []

    for item in tracks['items']:
        track = item['track']
        df.append({
            'name':track['name'],
            'main_artist':track['artists'][0]['name'],
            'release_date':track['album']['release_date'],
            'duration_ms':track['duration_ms'],
            'popularity':track['popularity'],
            'explicit':track['explicit'],
            'album_type':track['album']['album_type'],
            'track_id':track['id'],
            'main_artist_id':track['artists'][0]['id']
        })
        
    df = pd.DataFrame(df)
    len(df)

    artists_genre = []

    for id in artists_id:
        artist = sp.artist(artist_id = id)
        if len(artist['genres']) >= 1:
            artists_genre.append({'artist_id':id,'genre':artist['genres'][0]})
        else:
            artists_genre.append({'artist_id':id,'genre':np.nan})
            
    genre_df = pd.DataFrame(artists_genre)

    len(genre_df)

    df = df.merge(
        right = genre_df,
        left_on = 'main_artist_id',
        right_on = 'artist_id',
        how = 'left',
        ).drop('artist_id', axis = 1).drop_duplicates().reset_index(drop = True)
    
    df['list_country'] = country
    df['ranking'] = range(1, len(df) + 1)
    
    final_df = pd.concat([final_df, df], axis = 0, ignore_index = True)
    
final_df.to_csv(
    path_or_buf = os.path.join(os.path.dirname(__file__), 'spotify_data.csv'))