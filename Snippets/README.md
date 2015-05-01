##Snippets

**Problem**

To improve the InfiniteJukebox, we wanted to be able to compare transitions individually. In order to do this, we decided to create small snippets of the song that contain only one transition. These small wave files could then be compared to see which transitions are superior.

**Process**

Snippets has one function that creates the transition files. Make_song_snippet takes 4 arguments. You must give it the two beat indices, and the two LocalAudioFiles. It then locates the bar of the first index and goes back two additional bars if possible. Once it hits the transition, it switches LocalAudioFiles and plays two additional bars or until the end of the song is reached. The wave file is saved using the md5's of the songs as well as the indices and distance between the two beats. This way, all the relevant information is present for later use.

**Example**

The code below produces 10 random transitions for the given song. Transitions are found using [BeatDistance].

```python
audio_file1 = audio.LocalAudioFile("15 Sir Duke.m4a")
branches = fb.getBranches(audio_file1)
for i in range(10):
    beat1 = random.choice(branches.keys())
    beat2 = random.choice(branches[beat1])[0]
    make_song_snippet(beat1, beat2, audio_file1, audio_file1)
```
[BeatDistance]:https://github.com/jlstack/PythonEchonestRemix/tree/master/BeatDistance
