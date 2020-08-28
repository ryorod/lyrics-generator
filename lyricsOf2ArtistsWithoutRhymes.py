import sys
import os
import hashlib
from pymarkovchain import MarkovChain
from lyricsmaster import LyricWiki

if __name__ == '__main__':

    if len(sys.argv) != 4:
        raise "Usage: python3 /Users/ryorod/lyrics_generator/lyricsOf2Artists.py \"[artist_name]\" \"[artist_name]\" [number_of_phrases_to_generate]"

    artist_name1 = sys.argv[1]
    artist_name2 = sys.argv[2]
    number_of_phrases = sys.argv[3]

    # Generating a Markov Chain Model
    db_name_hashed = "db/" + hashlib.md5((artist_name1+artist_name2).lower().encode('utf-8')).hexdigest()
    mc = MarkovChain(db_name_hashed)

    # Checking if the database already exists, if so uses the cache instead another API call
    if not os.path.isfile(db_name_hashed):
        print("No data cached. Please be patient while we search the lyrics of " + artist_name1 + " and " + artist_name2)		
		
        # Adding lyrics to a single gigant string
        lyrics = ''

        provider = LyricWiki()

        # Fetch all lyrics
        discography1 = provider.get_lyrics(artist_name1)
        discography2 = provider.get_lyrics(artist_name2)

        # Discography Objects and Album Objects can be iterated over.
        for album in discography1:    # album is an Album Object.
            for song in album:       # song is a Song Object.
                lyrics += song.lyrics
        for album in discography2:    # album is an Album Object.
            for song in album:       # song is a Song Object.
                lyrics += song.lyrics

        # Generating the database
        mc.generateDatabase(lyrics)
        mc.dumpdb()
    
    # Printing a string
    for i in range(0, int(number_of_phrases)):
         print(mc.generateString())