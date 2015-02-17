__author__ = 'lukestack'
import math
import echonest.remix

"""
This a way of comparing two 'echonest.remix.audio.AudioQuantum' beats.
This method of comparing beats is almost identical to the way Paul Lamere compares
beats in the InfiniteJukebox. Only minor changes have been made.
"""

timbreWeight = 1
pitchWeight = 10
loudStartWeight = 1
loudMaxWeight = 1
durationWeight = 100
confidenceWeight = 1

"""
These are the weights decided on by Paul Lamere.
Weights can be thought of as level of importance when calculating distance.
For more on the specifications of these fields, visit http://developer.echonest.com/docs/v4/_static/AnalyzeDocumentation.pdf
"""

def get_beat_distance(beat1, beat2):
    """
    The only method the user should ever call.
    The distance between beats is really just the average distance between the segments of the two beats.

    :param beat1: first beat to be compared
    :param beat2: second beat to be compared
    :return: a numeric value for the distance between beats
    """
    if type(beat1) != echonest.remix.audio.AudioQuantum or type(beat1) != echonest.remix.audio.AudioQuantum or \
                    beat1.kind != "beat" or beat2.kind != "beat":
        raise Exception("make sure both parameters are type <'echonest.remix.audio.AudioQuantum'>' and of kind 'beat'")
    if len(beat1.segments) > len(beat2.segments):
        segs = len(beat2.segments)
    else:
        segs = len(beat1.segments)
    total = 0
    for seg in range(0, segs):
        total += __get_seg_distances__(beat1.segments[seg], beat2.segments[seg]) #adds each distance between individual segments to the total
    average = total / segs #takes the average distance between segments
    return average


def __get_seg_distances__(seg1, seg2):
    """
    Takes the distance between individual segments.

    :param seg1: first segment to be compared
    :param seg2: second segment to be compared
    :return: a numeric value for the distance between segments
    """
    timbre = __seg_distance__(seg1, seg2, 'timbre')
    pitch = __seg_distance__(seg1, seg2, 'pitches')
    sloudStart = math.fabs(seg1.loudness_begin - seg2.loudness_begin)
    sloudMax = math.fabs(seg1.loudness_max - seg2.loudness_max)
    duration = math.fabs(seg1.duration - seg2.duration)
    if seg1.confidence != None and seg2.confidence != None:
        confidence = math.fabs(seg1.confidence - seg2.confidence)
    else:
        confidence = 0
    #takes the individual field differences and multiplies them by their corresponding weights to get the overall distance
    distance = (timbre * timbreWeight) + (pitch * pitchWeight) + (sloudStart * loudStartWeight) + \
               (sloudMax * loudMaxWeight) + (duration * durationWeight) + (confidence * confidenceWeight)
    return distance

def __seg_distance__(seg1, seg2, field):
    """
    Helper method to call the __euclidean_distance__() with the
    right list of values based on the field given

    :param seg1: first segment to be compared
    :param seg2: second segment to be compared
    :param field: either timbre or pitch
    :return: distance between list of values for pitch or timbre
    """
    if field == 'timbre':
        return __euclidean_distance__(seg1.timbre, seg2.timbre)
    return __euclidean_distance__(seg1.pitches, seg2.pitches)


def __euclidean_distance__(v1, v2):
    """
    Think of the distance formula in geometry. It's the same thing.
    sqrt((q1-p1)**2 + (q2-p2)**2 + ...)

    :param v1: list of values from seg1
    :param v2: list of values from seg2
    :return: the euclidean distance between the two lists
    """
    sum = 0
    for i in range(0, len(v1)):
        delta = v2[i] - v1[i]
        sum += delta * delta
    return math.sqrt(sum)

