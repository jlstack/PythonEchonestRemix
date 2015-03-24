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
```

The search returns a dictionary with one key u'artists'. Artists contains many different things, but we want to look at u'items' which contains the different Artists found from our search. For this program, I just took the first item in the list (the top search result). Once the item was selected, I got the u'uri'. The u'uri' contains the spotify information for the artist. An example of a u'uri' would be "spotify:artist:7guDJrEfX3qb6FEbdPA5qi." You could simply go to [www.spotify.com/artist/7guDJrEfX3qb6FEbdPA5qi] to look at the searched artist's page. 

[www.spotify.com/artist/7guDJrEfX3qb6FEbdPA5qi] : www.spotify.com/artist/7guDJrEfX3qb6FEbdPA5qi
