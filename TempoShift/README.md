##Tempo Shift

**Problem**

I wanted to be able to shift tempo in real time, beat by beat. This idea had been proposed by many, and was not an idea of my own. However, with a minor addition to aqplayer, it is now possible.

**Warnings**

In my experience, tempo shifting does not work if you try to modify anything larger than a beat. Even if you just try to modify a bar, glitches between bars occur. Also, tempo shifting sounds much better if you keep the ratio between .5 and 1.5. These are limitations in dirac. Getting close to these limits results in audio that can contain static sounds and blips.

**Dependencies**

-dirac
-pyaudio

**Example**

The example below makes every beat a little faster in tempo than the one before it. It starts out with a ratio of 1.25, which is slower than the original and moves up to a ratio of .75, which is faster than the original. In short, the song starts out slow but ends faster than the original.

```python
audiofile = audio.LocalAudioFile("Sir Duke.m4a")
    player = Player(audiofile)
    beats = audiofile.analysis.beats
    for beat in beats:
        ratio = 1.25 - ((float(beat.absolute_context()[0]) / float(len(beats))) * .5)
        print ratio
        beat_audio = beat.render()
        scaled_beat = dirac.timeScale(beat_audio.data, ratio)
        ts = audio.AudioData(ndarray=scaled_beat, shape=scaled_beat.shape,
                                     sampleRate=audiofile.sampleRate, numChannels=scaled_beat.shape[1])
        player.play_from_AudioData(ts)
    player.close_stream()
```

