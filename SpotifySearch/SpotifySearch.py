author__ = 'lukestack'

import urllib2
import spotipy
from tempfile import NamedTemporaryFile
from pyechonest import track
import echonest.remix.audio as audio
import aqplayer

def getTopTen(lz_uri):
    songs = []
    spotify = spotipy.Spotify()
    results = spotify.artist_top_tracks(lz_uri)
    index = 0
    for t in results[u'tracks'][:10]:
        url = t[u'preview_url']
        req2 = urllib2.Request(url)
        response = urllib2.urlopen(req2)
        data = response.read()
        f = NamedTemporaryFile(suffix = ".mp3")
        f.write(data)
        songs.append((t['name'], audio.LocalAudioFile(f.name)))
        t1 = track.track_from_filename(f.name)
        print 'track:' + t['name'] + "   key:" + str(t1.key) + " tempo:" + str(t1.tempo) + " mode:" + str(t1.mode)
        index += 1
        f.close()
    return songs

def play(songs):
    for song in songs:
        print song[0]
        player = aqplayer.Player(song[1])
        beats = song[1].analysis.beats
        for beat in beats:
            player.play(beat)
        player.closeStream()
        
def main():
    results = None
    while results == None:
        try:
            artist = raw_input("Please enter artist: ")
            spotify = spotipy.Spotify()
            results = spotify.search(q='artist:' + artist, type='artist')
            print "Found:", results[u'artists'][u'items'][0][u'name'] #takes the top search result
            lz_uri = results[u'artists'][u'items'][0][u'uri']
            songs = getTopTen(lz_uri)
            play(songs)
        except IndexError: #artist not found
            print "\nPlease choose a different artist."
            results = None

if __name__ == '__main__':
    main()

