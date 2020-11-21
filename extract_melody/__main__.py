import sys
import os
import pretty_midi
from extractor import Extractor
from multiprocessing import Pool, Value, Lock

cmd_valid = "valid"
cmd_melody = "melody"

def main():
    midi_list_file = None
    keyword_file = None
    out_dir = None
    thread_num = os.cpu_count()
    cmd = None

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-mf":
            midi_list_file = sys.argv[i+1]
        if sys.argv[i] == "-kw":
            keyword_file = sys.argv[i+1]
        if sys.argv[i] == "-od":
            out_dir = sys.argv[i+1]
        if sys.argv[i] == "-cmd":
            cmd = sys.argv[i+1]

    extractor = Extractor(keyword_file)
    midi_list = []
    with open(midi_list_file) as fp:
        for line in fp:
            file = line.strip()
            midi_list.append(file)

    if cmd == cmd_valid:
        with Pool(thread_num) as pool:
            for file in midi_list:
                pool.apply_async(
                    extractor.extractValid,
                    args = (file, out_dir),
                    error_callback = lambda e: thread_error(e)
                )
            pool.close()
            pool.join()
    elif cmd == cmd_melody:
        with Pool(thread_num) as pool:
            for file in midi_list:
                pool.apply_async(
                    extractor.extractMelody,
                    args = (file, out_dir),
                    error_callback = lambda e: thread_error(e)
                )
            pool.close()
            pool.join()
    else:
        print("ERROR: invalid command")
        exit(1)

def thread_error(e):
    print(e)
    exit(1)

if __name__ == "__main__":
    main()
