<img src="https://github.com/jlstack/PythonEchonestRemix/blob/master/AnalysisVisualization/Images/BackInBlackAnalysisVisual.png" height="400" width="500" align="middle"/> <img src="https://github.com/jlstack/PythonEchonestRemix/blob/master/AnalysisVisualization/Images/SirDukeAnalysisVisual.png" height="400" width="500" align="middle"/>

##AnalysisVisualization

A simple visualization to see some of the data provided by Echonest.

**Problem**

It is often difficult for people to understand the data that Echonest provides for us. To help them understand, Dr.Parry and I discussed creating a visual representation. This respresentation would need some method of displaying the audio, as well as the markers(tatums, beats, bars and sections).

**Dependencies**

    - SegColor

**How it Works**

AnalysisVisualization first plots the audio. Echonest provides you with "loudness" information for each segment. For each segment, I plotted a line between the "loudness_begin" to the "loudness_max" (y values). For the x values, Echonest provides the "start" time of each segment and the "time_loudness_max" (which is a time offset relative to the "start" time). I then connected the "loudness_max" point to the start of the next segment and shaded the whole area below. For the colors, I used [SegColor]. Below is the code I used to accomplish this step.

```python
for i in range(0, len(segments)):
    start = segments[i].start
    loudest_point = start + segments[i].time_loudness_max
    end = start + segments[i].duration
    color = SegColor.getSegmentColor(bounds, segments[i])
    if i + 1 < len(segments):
        next_seg_loudness = segments[i + 1].loudness_begin
    else:
        next_seg_loudness = 0
    ax.plot([start, loudest_point], [segments[i].loudness_begin, segments[i].loudness_max], linewidth=2, color=color)
    ax.fill_between([start, loudest_point], [segments[i].loudness_begin, segments[i].loudness_max], -60, color=color)
    ax.plot([loudest_point, end], [segments[i].loudness_max, next_seg_loudness], linewidth=2, color=color)
    ax.fill_between([loudest_point, end], [segments[i].loudness_max, next_seg_loudness], -60, color=color)
```

The next step was to plot all of the time markers for tatums, beats, bars and sections. This was much easier. I just iterated through all lists and plotted a vertical line at the "start" of the AudioQuantum. The colors of the lines are arbitrary.

```python
for sect in sections:
    ax.plot([sect.start, sect.start], [-30, -60], linewidth=4, color='black')

for bar in bars:
    ax.plot([bar.start, bar.start], [-37.5, -60], linewidth=3.5, color='blue')

for beat in beats:
    ax.plot([beat.start, beat.start], [-45, -60], linewidth=3, color='green')

for tat in tatums:
    ax.plot([tat.start, tat.start], [-52.5, -60], linewidth=2.5, color='red')
```

**How to USE**

Just clone the code and enter your favorite song. It's that easy!

**Improvements**

I initially wanted the visual to scroll with the music, but had a lot of difficulties trying to make this happen. If anyone wants to take it upon themselves to make it happen, that would be awesome!

[SegColor]:https://github.com/jlstack/PythonEchonestRemix/tree/master/SegColor
