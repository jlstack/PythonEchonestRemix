__author__ = 'lukestack'

"""
SegColor allows you to visualize an 'echonest.remix.audio.AudioSegment' by assigning it a color
value based on the timbre of the segment. To do this, it looks at the 2-4 timbre values. According
to echonest the "second emphasizes brightness; third is more closely correlated to the flatness of a sound;
fourth to sounds with a stronger attack" This is the same technique Paul Lamere uses in InfiniteJukebox.
"""

def normalizeColor(audio_file):
    """
    :param audio_file: 'echonest.remix.audio.LocalAudioFile' being used
    :return: bounds for the colors(mins and maxs)
    """
    segments = audio_file.analysis.segments
    cmin = [100,100,100]
    cmax = [-100,-100,-100]
    for seg in segments:
        for j in range(3):
            t = seg.timbre[j + 1]
            if t < cmin[j]:
                cmin[j] = t
            if t > cmax[j]:
                cmax[j] = t
    return (cmin, cmax)

def getSegmentColor(bounds, seg):
    """
    :param bounds: established with normalizeColor()
    :param seg: 'echonest.remix.audio.AudioSegment' for which the color is being requested
    :return: hex value for the appropriate color
    """
    cmin = bounds[0]
    cmax = bounds[1]
    results = [0,0,0]
    for i in range(3):
        t = seg.timbre[i + 1]
        norm = (t - cmin[i]) / (cmax[i] - cmin[i])
        results[i] = norm * 255
    return '#%02x%02x%02x' % (results[1], results[2], results[0])