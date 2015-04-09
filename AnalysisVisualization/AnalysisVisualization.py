__author__ = 'lukestack'

import echonest.remix.audio as audio
import matplotlib.pyplot as plt
import numpy as np
import aqplayer
from matplotlib.pyplot import pause, ion, ioff
import matplotlib.patches as mpatches



audio_file = audio.LocalAudioFile("/Users/lukestack/PycharmProjects/InfiniteJukeboxReplica/MP3Songs/15 Sir Duke.m4a")
audio_data = audio_file.render().data
audio_data = (audio_data[:, 0] + audio_data[:, 1]) / 2
condensed_data = []

for i in range(0, len(audio_data)/44100):
    data = audio_data[(i*44100):(i+1)*44100]
    condensed_data.append((np.amin(data), np.amax(data)))

tatums = audio_file.analysis.tatums
beats = audio_file.analysis.beats
bars = audio_file.analysis.bars
sections = audio_file.analysis.sections

fig = plt.figure()
ax = fig.add_subplot(111)

for sect in sections:
    ax.plot([sect.start, sect.start], [20000, -20000], linewidth=4, color='black')

for bar in bars:
    ax.plot([bar.start, bar.start], [15000, -15000], linewidth=3.5, color='purple')

for beat in beats:
    ax.plot([beat.start, beat.start], [10000, -10000], linewidth=3, color='green')

for tat in tatums:
    ax.plot([tat.start, tat.start], [5000, -5000], linewidth=2.5, color='red')

for sec in range(0, len(condensed_data)):
    if sec % 2 == 0:
        ax.plot([sec, sec + 1], [condensed_data[sec][0], condensed_data[sec][1]], linewidth=2, color='blue')
    else:
        ax.plot([sec, sec + 1], [condensed_data[sec][1], condensed_data[sec][0]], linewidth=2, color='blue')

ax.set_xlim([0, 10])
plt.show()
"""
ion()
cursor, = ax.plot(0, 0, color='green', markersize=10, marker='s')
player = aqplayer.Player()
for beat in beats:
    cursor.set_xdata(beat.start)
    fig.canvas.draw()
    pause(beat.duration)

ioff()
player.close_stream()
"""
