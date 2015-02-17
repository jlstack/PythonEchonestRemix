##BeatDistance

Beat Distance is static and used to compare two 'echonest.remix.audio.AudioQuantum' of kind 'beat'.
The only method that should ever be called by the user is get_beat_distance().

**Example**

```python
import echonest.remix.audio as audio
import BeatDistance

audio_file = audio.LocalAudioFile("15 Sir Duke.m4a")
beats = audio_file.analysis.beats

beat1 = beats[0]
beat2 = beats[1]

print BeatDistance.get_beat_distance(beat1, beat2) #returns a numeric value for the "distance" between the two
```

**Code Explanation**

First, there are predefined weights for different fields. These are the same weights Paul Lamere decided on when implementing the InfiniteJukebox. Weights can be thought of as level of importance. Keep in mind that different fields have different ranges. A field may contribute more to the distance measurement even though it's weight is less than another. Timbre is the best example of this. It's weight is only 1, yet it has the greatest range of all the fields. Therefore, it plays the greatest importance when calculating distance.

```python
timbreWeight = 1
pitchWeight = 10
loudStartWeight = 1
loudMaxWeight = 1
durationWeight = 100
confidenceWeight = 1
```

In my method, I look to see which beat has the fewest number of segments. I then only compare this many number of segments. 

```python
if len(beat1.segments) > len(beat2.segments):
        segs = len(beat2.segments)
    else:
        segs = len(beat1.segments)
    total = 0
    for seg in range(0, segs):
        total += __get_seg_distance__(beat1.segments[seg], beat2.segments[seg]) #adds each distance between individual segments to the total
    average = total / segs #takes the average distance between segments
    return average
```

Paul Lamere's InfiniteJukebox implementation. Paul Lamere compares the number of segments located in beat1. If beat2 does not have at least as many segments as beat1, 100's are added in place of the actual distance between segments. 

```javascript
for (var j = 0; j < q1.overlappingSegments.length; j++) {
            var seg1 = q1.overlappingSegments[j];
            var distance = 100;
            if (j < q2.overlappingSegments.length) {
                var seg2 = q2.overlappingSegments[j];
                // some segments can overlap many quantums,
                // we don't want this self segue, so give them a
                // high distance
                if (seg1.which === seg2.which) {
                    distance = 100
                } else {
                    distance = get_seg_distances(seg1, seg2);
                }
            } 
            sum += distance;
        }
```

You may have noticed __seg_distance__(seg1, seg2, field) being called. __seg_distance__() just calls the __euclidean_distance__() with the right list of values based on the field given. The field will either be 'timbre' or 'pitch'. __euclidean_distance__() uses the same distance formula everyone uses in high school geometry. sqrt((q1-p1)**2 + (q2-p2)**2 + ...)

```python
sum = 0
    for i in range(0, len(v1)):
        delta = v2[i] - v1[i]
        sum += delta * delta
    return math.sqrt(sum)
```
