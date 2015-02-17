##BeatDistance

Beat Distance is static and used to compare two 'echonest.remix.audio.AudioQuantum' of kind 'beat'.
The only method that should ever be called by the user is get_beat_distance().

**Example**

```python
import echonest.remix.audio as audio
import BeatDistance

audio_file = audio.LocalAudioFile("15 Sir Duke.m4a")
beats = audio_file.analysis.beats

beat1 = beats.__getitem__(0)
beat2 = beats.__getitem__(1)

print BeatDistance.get_beat_distance(beat1, beat2)
```
