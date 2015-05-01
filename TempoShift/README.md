##Tempo Shift

**Problem**

I wanted to be able to shift tempo in real time, beat by beat. This idea had been proposed by many, and was not an idea of my own. However, with a minor addition to aqplayer, it is now possible.

**Warnings**

In my experience, tempo shifting does not work if you try to modify anything larger than a beat. Even if you just try to modify a bar, glitches between bars occur. Also, tempo shifting sounds much better if you keep the ratio between .5 and 1.5. These are limitations in dirac. Getting close to these limits results in audio that can contain static sounds and blips.

**Dependencies**

    -aqplayer

**Example**

The example below makes every beat a little faster in tempo than the one before it. It starts out with a ratio of 1.25, which is slower than the original and moves up to a ratio of .75, which is faster than the original. In short, the song starts out slow but ends faster than the original.

```python
song = "15 Sir Duke.m4a"
audiofile = audio.LocalAudioFile(song)
player = Player()
beats = audiofile.analysis.beats
for beat in beats:
    ratio = 1.25 - ((float(beat.absolute_context()[0]) / float(len(beats))) * .5)
    player.shift_tempo_and_play(beat, ratio)
player.close_stream()
```

**Progress Made**

The real progress made is not merely this program. What I am trying to demonstrate is that now, [aqplayer] has the ability to tempo shift in real time! Just give your player the AudioQuantum and shift ratio and it will do it all for you using the power of dirac.

[aqplayer]: https://github.com/jlstack/PythonEchonestRemix/tree/master/aqplayer
