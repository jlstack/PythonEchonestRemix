__author__ = 'lukestack'
import math

"""
This class allows you to compare two 'echonest.remix.audio.AudioQuantum'. 
This method of comparing beats is almost identical to the way Paul Lamere compares
beats in the InfiniteJukebox. Only minor changes have been made.
"""

timbreWeight = 1
pitchWeight = 10
loudStartWeight = 1
loudMaxWeight = 1
durationWeight = 100
confidenceWeight = 1

def get_beat_distance(beat1, beat2):
    if type(beat1) != echonest.remix.audio.AudioQuantum or type(beat1) != echonest.remix.audio.AudioQuantum or \
                    beat1.kind != "beat" or beat2.kind != "beat":
        raise Exception("make sure both parameters are type <'echonest.remix.audio.AudioQuantum'>' and of kind 'beat'")
    if len(beat1.segments) > len(beat2.segments):
        segs = len(beat2.segments)
    else:
        segs = len(beat1.segments)
    average = 0
    for seg in range(0,segs):
        average += get_seg_distance(beat1.segments[seg], beat2.segments[seg])
    average = average / segs
    return average

def get_seg_distance(seg1, seg2):
    timbre = seg_distance(seg1, seg2, 'timbre')
    pitch = seg_distance(seg1, seg2, 'pitches')
    sloudStart = math.fabs(seg1.loudness_begin - seg2.loudness_begin)
    sloudMax = math.fabs(seg1.loudness_max - seg2.loudness_max)
    duration = math.fabs(seg1.duration - seg2.duration)
    if seg1.confidence != None and seg2.confidence != None:
        confidence = math.fabs(seg1.confidence - seg2.confidence)
    else:
        confidence = 0
    distance = (timbre * timbreWeight) + (pitch * pitchWeight) + (sloudStart * loudStartWeight) + \
               (sloudMax * loudMaxWeight) + (duration * durationWeight) + (confidence * confidenceWeight)
    return distance

def seg_distance(seg1, seg2, field):
    if field == 'timbre':
        return euclidean_distance(seg1.timbre, seg2.timbre)
    return euclidean_distance(seg1.pitches, seg2.pitches)

def euclidean_distance(v1, v2):
    sum = 0
    for i in range(0,len(v1)):
        delta = v2[i] - v1[i]
        sum += delta * delta
    return math.sqrt(sum)
