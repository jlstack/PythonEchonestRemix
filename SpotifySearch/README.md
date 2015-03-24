##SpotifySearch

SpotifySearch searches for a specified artist on Spotify via spotipy. If the artist is found, the 30 second sample for each top-ten track is fetched and played (not all artists have all 10 tracks). 

**Problem**

Dr.Parry wanted to be able to search an artist and create an InfinitePlaylist with the 30 second samples for a presentation at a nearby high school. I had already written a similar program a while back, so I modified it to his needs.

**Dependencies**

 - spotipy
 - pyechonest
 - echonest.remix
 - aqplayer

**Using SpotifySearch**

SpotifySearch is very simple to use. Just fire it up and type in an artist. If it has the artist, it will fetch the tracks and play through them all.

**How It Works**

The first thing SpotifySearch does is prompt the user for an artist. It then searches Spotify and takes the first result.

```python
artist = raw_input("Please enter artist: ")
spotify = spotipy.Spotify()
results = spotify.search(q='artist:' + artist, type='artist')
artist_uri = results[u'artists'][u'items'][0][u'uri']
```

The search returns a dictionary with one key u'artists'. Artists contains many different things, but we want to look at u'items' which contains the different Artists found from our search. For this program, I just took the first item in the list (the top search result). Once the item was selected, I got the u'uri'. The u'uri' contains the spotify information for the artist. An example of a u'uri' would be "spotify:artist:7guDJrEfX3qb6FEbdPA5qi." You could simply go to play.spotify.com/artist/7guDJrEfX3qb6FEbdPA5qi to look at the searched artist's page. 

```python
songs = []
results = spotify.artist_top_tracks(artist_uri)
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
    f.close()
```

Next, using the u'uri', the top-ten tracks are retrieved. The search returns a dictionary with one key, u'tracks'. Each track contains information about the track, the album its on, the album artwork, etc. We want the u'preview_url'. An example preview_url is https://p.scdn.co/mp3-preview/1aca5b79c165c3126b7bd7797fc810996f83a338. As you can see, once the preview_url is found, the audio data is retrieved using urllib2. The data is written to a tempfile created using python's tempfile module. After the mp3 is created locally, an Echonest LocalAudioFile is created for the mp3 and added to the list of songs. The list contains tuples. Each tuple contains the name of the track and it's LocalAudioFile. If you are wondering about the track_from_filename, it is just used to get information about the track such as it's key and tempo. This information is unnecessary, but nice to have.

```python
for song in songs:
    print song[0]
    player = aqplayer.Player(song[1])
    beats = song[1].analysis.beats
    for beat in beats:
        player.play(beat)
    player.closeStream()
```

The last step is to play all of the files. Since the LocalAudioFile contains a wav file, this is easy using my aqplayer. See more at [aqplayer].

[aqplayer]: https://github.com/jlstack/PythonEchonestRemix/tree/master/aqplayer 
