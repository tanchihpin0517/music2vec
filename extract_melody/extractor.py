import os
import pretty_midi
import pickle
import shutil

class Extractor():
    def __init__(self, keyword_file):
        self.keyword = []

        with open(keyword_file) as fp:
            for line in fp:
                kw = line.strip().lower()
                self.keyword.append(kw)

    def extractValid(self, file, out_dir):
        print(file)
        try:
            midi = pretty_midi.PrettyMIDI(file)
            name = os.path.basename(file)
            of = os.path.join(out_dir, name)
            shutil.copy2(file, str(of))
        except Exception as e:
            print(e)

    def extractMelody(self, file, out_dir):
        midi = pretty_midi.PrettyMIDI(file)

        contain, name = self.containMelody(midi)
        if contain:
            print(file)
            name = os.path.basename(file)
            of = os.path.join(out_dir, name)
            shutil.copy2(file, of)

    def containMelody(self, midi: pretty_midi.PrettyMIDI) -> (bool, str):
        for instrument in midi.instruments:
            name = instrument.name.lower()
            for kw in self.keyword:
                if kw in name:
                    return (True, name)

        return (False, None)
