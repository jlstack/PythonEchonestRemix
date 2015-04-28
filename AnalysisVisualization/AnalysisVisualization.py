__author__ = 'lukestack'

import echonest.remix.audio as audio
import matplotlib.pyplot as plt
import numpy as np
import SegColor
import aqplayer
import threading
import time
from matplotlib.pyplot import pause, ion, ioff
import matplotlib.patches as mpatches



audio_file = audio.LocalAudioFile("MP3Songs/15 Sir Duke.m4a")
print audio_file.analysis.tempo['value']
audio_data = audio_file.render().data
audio_data = (audio_data[:, 0] + audio_data[:, 1]) / 2
bounds = SegColor.normalizeColor(audio_file)

tatums = audio_file.analysis.tatums
segments = audio_file.analysis.segments
beats = audio_file.analysis.beats
bars = audio_file.analysis.bars
sections = audio_file.analysis.sections

condensed_data = []

for tat in tatums:
    beginning = int(tat.start * 44100)
    end = int((tat.start + tat.duration) * 44100)
    data = audio_data[beginning:end]
    condensed_data.append((np.amin(data), np.amax(data)))

fig = plt.figure()
ax = fig.add_subplot(111)

for sect in sections:
    ax.plot([sect.start, sect.start], [0, 60], linewidth=4, color='black')

for bar in bars:
    ax.plot([bar.start, bar.start], [7.5, 52.5], linewidth=3.5, color='purple')

for beat in beats:
    ax.plot([beat.start, beat.start], [15, 45], linewidth=3, color='green')

for tat in tatums:
    ax.plot([tat.start, tat.start], [22.5, 37.5], linewidth=2.5, color='red')

for i in range(0, len(segments)):
    start = segments[i].start
    loudest_point = start + segments[i].time_loudness_max
    end = start + segments[i].duration
    color = SegColor.getSegmentColor(bounds, segments[i])
    if i != len(segments) - 1:
        ax.plot([start, loudest_point], [segments[i].loudness_begin, segments[i].loudness_max], linewidth=2, color=color)
        ax.plot([loudest_point, end], [segments[i].loudness_max, segments[i + 1].loudness_begin], linewidth=2, color=color)
    else:
        ax.plot([start, loudest_point], [segments[i].loudness_begin, segments[i].loudness_max], linewidth=2, color=color)
        ax.plot([loudest_point, end], [segments[i].loudness_max, 0], linewidth=2, color=color)

ax.plot([sections[0].start, sections[0].start], [0, 60], linewidth=4, color='black', label="Section")
ax.plot([bars[0].start, bars[0].start], [7.5, 52.5], linewidth=3.5, color='purple', label="Bar")
ax.plot([beats[0].start, beats[0].start], [15, 45], linewidth=3, color='green', label="Beat")
ax.plot([tatums[0].start, tatums[0].start], [22.5, 37.5], linewidth=2.5, color='red', label="Tatum")

def play_beat(beat, player):
    player.play(beat)

ax.set_xlim([0, 30])
ax.legend()
plt.show()

#still need to make it scroll
"""
dt = 0.001
timer = fig.canvas.new_timer(interval=dt*1000.0)
cursor, = ax.plot(0, 0, color='green', markersize=10, marker='s')
player = aqplayer.Player()
plt.show()
beat = beats[0]

thread_list = []
for beat in beats:
    thread = threading.Thread(target=play_beat, args=(beat, player))
    thread_list.append(thread)

for i in range(len(beats)):
    thread_list[i].start()
    cursor.set_xdata(beats[i].start)
    fig.canvas.draw()

player.close_stream()
"""
