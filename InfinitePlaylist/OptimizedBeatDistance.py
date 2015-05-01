import pickle
import os
import bisect

# Some methods from Dr.Parry's infinite_playlist
def get_edges(laf_i_, laf_j_, PLAYLIST_DIR):
    from numpy import isnan, where, vstack
    md5_i_ = laf_i_.analysis.pyechonest_track.md5
    md5_j_ = laf_j_.analysis.pyechonest_track.md5
    track_md5 = [md5_i_, md5_j_]
    track_md5.sort()
    edges_file_ = PLAYLIST_DIR + os.sep + track_md5[0] + "_" + track_md5[1] + ".edges.pkl"
    if os.path.isfile(edges_file_):
        print "loading", edges_file_
        with open(edges_file_, 'rb') as in_file_:
            edges_ = pickle.load(in_file_)
    else:
        num_edges = 0
        edges_ = {md5_i_: {}, md5_j_: {}}
        beat_distances = get_beat_distances(laf_i_, laf_j_)
        beat_distances[isnan(beat_distances)] = float('Inf')
        (ii, jj) = where(beat_distances < 80)
        for (i1, j1) in vstack((ii, jj)).T:
            d1 = beat_distances[i1, j1]
            update_edges(edges_, md5_i_, i1, md5_j_, j1, d1)
            if md5_i_ != md5_j_:
                update_edges(edges_, md5_j_, j1, md5_i_, i1, d1)
            num_edges += 1
        edges_['num_edges'] = num_edges
        print num_edges, "edges found"
        with open(edges_file_, 'wb') as output_:
            pickle.dump(edges_, output_)
    return edges_

def get_beat_distances(audio_i_, audio_j_):
    from numpy import minimum, array, ones, isnan, copy
    segments_i = get_segments(audio_i_)
    aq_beats_i = audio_i_.analysis.beats

    first_segment_index_i = array([audio_i_.analysis.segments.index(beat.segments[0]) for beat in aq_beats_i])\
        .reshape((len(aq_beats_i), 1))
    beat_length_i = array([len(beat.segments) for beat in aq_beats_i]).reshape((len(aq_beats_i), 1))

    segments_j = get_segments(audio_j_)
    aq_beats_j = audio_j_.analysis.beats

    first_segment_index_j = array([audio_j_.analysis.segments.index(beat.segments[0]) for beat in aq_beats_j])\
        .reshape((len(aq_beats_j), 1))
    beat_length_j = array([len(beat.segments) for beat in aq_beats_j]).reshape((len(aq_beats_j), 1))
    if audio_i_.filename == audio_j_.filename:
        segment_dist = seg_distances(segments_i)
    else:
        segment_dist = seg_distances(segments_i, segments_j)

    (m, n) = segment_dist.shape
    beat_dist_ = float('NaN') * ones((len(aq_beats_i), len(aq_beats_j)))
    # noinspection PyCallingNonCallable
    segment_dist2 = copy(segment_dist)
    for beat_length in range(1, 6):
        i_beat_index = [x for x in range(len(aq_beats_i)) if beat_length_i[x] == beat_length]
        j_beat_index = [x for x in range(len(aq_beats_j)) if beat_length_j[x] == beat_length]

        if len(i_beat_index) > 0 and len(j_beat_index) > 0:
            i_segment_index = first_segment_index_i[i_beat_index]
            j_segment_index = first_segment_index_j[j_beat_index]

            old_rows = beat_dist_[i_beat_index, :]
            new_rows = segment_dist2[i_segment_index, first_segment_index_j.T]
            is_nan = isnan(old_rows)
            old_rows[is_nan] = new_rows[is_nan]
            beat_dist_[i_beat_index, :] = old_rows

            old_cols = beat_dist_[:, j_beat_index]
            new_cols = segment_dist2[first_segment_index_i, j_segment_index.T]
            is_nan = isnan(old_cols)
            old_cols[is_nan] = new_cols[is_nan]
            beat_dist_[:, j_beat_index] = old_cols

        segment_dist2[:m-beat_length, :n-beat_length] += segment_dist[beat_length:, beat_length:]

    # divide by minimum number of segments per beat comparison
    num_segments = minimum(beat_length_i, beat_length_j.T)
    beat_dist_ /= num_segments

    # adjust for local_context of beat within bar
    beat_within_bar_i_ = array([beat.local_context()[0] for beat in aq_beats_i]).reshape((-1, 1))
    beat_within_bar_j_ = array([beat.local_context()[0] for beat in aq_beats_j]).reshape((1, -1))
    index = beat_within_bar_i_ * ones((1, beat_within_bar_j_.size)) != \
        ones((beat_within_bar_i_.size, 1)) * beat_within_bar_j_
    beat_dist_[index] = float('Inf')
    return beat_dist_

def get_segments(audio_file_):
    from numpy import hstack, array
    segments_ = audio_file_.analysis.segments
    n_ = len(segments_)
    pitches_ = array(segments_.pitches)
    timbre_ = array(segments_.timbre)
    duration_ = array(segments_.durations).reshape((n_, 1))
    loudness_max_ = array(segments_.loudness_max).reshape((n_, 1))
    loudness_start_ = array(segments_.loudness_begin).reshape((n_, 1))
    return hstack((10 * pitches_, timbre_, 100 * duration_, loudness_max_, loudness_start_))

def seg_distances(u_, v_=None):
    from scipy.spatial.distance import pdist, cdist, squareform
    from numpy import diag, ones
    if v_ is None:
        d_ = pdist(u_[:, 0:12], 'euclidean')
        d_ += pdist(u_[:, 12:24], 'euclidean')
        d_ += pdist(u_[:, 24:], 'cityblock')
        d_ = squareform(d_) + diag(float('NaN') * ones((u_.shape[0],)))
    else:
        d_ = cdist(u_[:, 0:12], v_[:, 0:12], 'euclidean')
        d_ += cdist(u_[:, 12:24], v_[:, 12:24], 'euclidean')
        d_ += cdist(u_[:, 24:], v_[:, 24:], 'cityblock')
    return d_

def update_edges(e_, m1_, i1_, m2_, i2_, d_):
    a = e_[m1_].get(i1_, [])
    bisect.insort(a, (d_, m2_, i2_))
    e_[m1_][i1_] = a