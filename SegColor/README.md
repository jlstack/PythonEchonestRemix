##SegColor

SegColor is static and used to produce a visual representation of an 'echonest.remix.audio.AudioSegment'. It does this by assigning rgb values according to the 2-4 timbre values of the segment. The method I am using is identicle to Paul Lamere's in InfiniteJukebox. I just converted it into Python. 

**Example**

```python
audio_file = audio.LocalAudioFile("15 SirDuke.m4a")
segs = audio_file.analysis.segments
bounds = sc.normalizeColor(audio_file)
print sc.getSegmentColor(bounds, segs[0]) #should be a hex value
```

**Code Explanation**

There are only two methods in SegColor. The first normalizeColor() retrieves the mins and maxs of the timbre values for the entire song. These values are later used to turn the timbre values into a decimal ranging from 0 to 1. The decimal is then multiplied by 255 to give an appropriate color value for each rgb color (since the RGB color system uses values from 0 to 255).

The timbre values used for the colors:
    * Red - timbre value 3 which is the "flatness of a sound" 
    * Green - timbre value 4 which has to do with the "attack" of the segment
    * Blue - timbre value 2 which correlates to the "brightness" of the segment

For more about timbre visit [Analyzer Documentation]

Paul Lamere's original

```javascript
function normalizeColor() {
    cmin = [100,100,100];
    cmax = [-100,-100,-100];

    var qlist = track.analysis.segments;
    for (var i = 0; i < qlist.length; i++) {
        for (var j = 0; j < 3; j++) {
            var t = qlist[i].timbre[j + 1];

            if (t < cmin[j]) {
                cmin[j] = t;
            }
            if (t > cmax[j]) {
                cmax[j] = t;
            }
        }
    }
}
```

My implemenataion

```python
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
```

Paul Lamere's original

```javascript
function getSegmentColor(seg) {
    var results = []
    for (var i = 0; i < 3; i++) {
        var t = seg.timbre[i + 1];
        var norm = (t - cmin[i]) / (cmax[i] - cmin[i]);
        results[i] = norm * 255;
        results[i] = norm;
    }
    return to_rgb(results[1], results[2], results[0]);
    //return to_rgb(results[0], results[1], results[2]);
}
```

My implemenataion

```python
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
```

[Analyzer Documentation]: http://developer.echonest.com/docs/v4/_static/AnalyzeDocumentation.pdf
