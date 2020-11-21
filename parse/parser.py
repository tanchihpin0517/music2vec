import pretty_midi
import numpy as np

class Parser:
    def __init__(self, keyword_file):
        self.keyword = []
        self.keyProfile = self.getKeyProfile()

        with open(keyword_file) as fp:
            for line in fp:
                kw = line.strip().lower()
                self.keyword.append(kw)

    def getKeyProfile(self):
        """
        ignore relative major and minor
        """
        base = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1] # C major (or A minor)
        #base = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # test
        profile = []
        for i in range(12):
            key = []
            for j in range(len(base)):
                index = (i-j) % 12
                key.append(base[index])
            profile.append(key)
        return profile

    def get_pitch_class_histogram(self, midi, use_duration=True, use_velocity=True, normalize=True):
        notes = []
        for instrument in midi.instruments:
            notes.extend(instrument.notes)

        weights = np.ones(len(notes))
        # Assumes that duration and velocity have equal weight
        if use_duration:
            weights *= [note.end - note.start for note in notes]
        if use_velocity:
            weights *= [note.velocity for note in notes]

        histogram, _ = np.histogram([n.pitch % 12 for n in notes],
                                    bins=np.arange(13),
                                    weights=weights,
                                    density=normalize)
        if normalize:
            histogram /= (histogram.sum() + (histogram.sum() == 0))
        return histogram


    def parse(self, midi_file):
        """
        * translate midi to notes
        * normalize to C major or a minor

        """
        midi = pretty_midi.PrettyMIDI(midi_file)
        print(midi.key_signature_changes)
        print(midi.get_pitch_class_histogram(use_duration=True))

        histogram = self.get_pitch_class_histogram(midi, use_duration=True)
        print(histogram)
        key_candidate = np.dot(self.keyProfile, histogram)
        print(key_candidate)
        key = 0
        m = 0
        for i in range(len(key_candidate)):
            if m < key_candidate[i]:
                m = key_candidate[i]
                key = i
        print(key)
