##InfiniteJukeboxReplica

InfiniteJukeboxReplica is a Python implementation of Paul Lamere's InfiniteJukebox. Some liberties were taken to simplify the code. Just run the InfiniteJukeBoxApp.py and a gui will pop up. Just put the path of your song into the textbox and choose your threshold. Threshold can be thought of as the quality of the branches. The lower the threshold, the better the branches will sound but a fewer number of branches will exist.

**Dependencies**

To use the InfiniteJukeboxReplica, you will need:

      - pyaudio
      - ffmpeg
      - Tkinter
      - pickle
      - echonest.remix 

You must have an Echonest API key set up on your machine to use the program.

**Process**

InfiniteJukeboxReplica uses branches found and stored with [FindBranches]. These branches are found using [BeatDistance] to calculate the distance between beats. To assign colors to each beat [SegColor] is used. These are the colors used when drawing the beat tiles and the branches between beats. To play the audio of the song, [aqplayer] is used. The main process the program uses is found in the play() method.

```python
def play(canvas, audio_file, branches, threshold):
    player = Player(audio_file)
    beats = audio_file.analysis.beats
    lastBranch = max(branches.keys())
    width = (1440 - (xpad * 2)) / float(len(beats))
    cur = drawCurrentBeat(canvas, width, 0)
    canvas.update()
    player.play(beats[0], True) #play the first beat with extra frames for intro
    bran = None
    i = 1
    while i < len(beats):
        randomInt = random.randint(0,1)
        if bran != None:
            canvas.delete(bran)
        if cur != None:
            canvas.delete(cur)
        if i == lastBranch or (branches.has_key(i) and randomInt == 1):
            branchTo = random.choice(branches[i])
            if i == lastBranch or (branchTo[0] < lastBranch and branchTo[1] <= threshold):
                bran = drawCurrentBranch(canvas, width, i, branchTo[0])
                i = branchTo[0]
        cur = drawCurrentBeat(canvas, width, i)
        canvas.update()
        player.play(beats[i])
        i+=1
```

In play(), a Player is created using the LocalAudioFile. The last branch is then found by finding the key with the greatest value. The first beat is played before the loop, because it has extra frames that must be played at the beginning of the song since the first beat of a song rarely falls on second 0.0. After that, an endless loop is used to play the song "forever." The loop checks every beat to see if it has any branchable beats associated with it. If it does, there is a 50% chance that a branch will be taken. If it chooses to branch, a random branch is chosen from the list of branchable beats. No matter what, the lastbranch is always taken. 

If you want to readjust your threshold, just close the canvas and reopen it with the new threshold value. Notice that the lastbranch will always appear, even if you set the threshold to 0. This is to ensure that it never stops playing.

[aqplayer]: https://github.com/jlstack/PythonEchonestRemix/tree/master/aqplayer
[BeatDistance]: https://github.com/jlstack/PythonEchonestRemix/tree/master/BeatDistance
[FindBranches]: https://github.com/jlstack/PythonEchonestRemix/tree/master/FindBranches
[SegColor]: https://github.com/jlstack/PythonEchonestRemix/tree/master/SegColor  
