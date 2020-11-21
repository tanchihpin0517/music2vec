import sys
import os
from parser import Parser
from multiprocessing import Pool, Value, Lock

cmd_parse = "parse"

def main():
    midi_list_file = None
    keyword_file = None
    thread_num = os.cpu_count()

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-mf":
            midi_list_file = sys.argv[i+1]
        if sys.argv[i] == "-kw":
            keyword_file = sys.argv[i+1]
        if sys.argv[i] == "-cmd":
            cmd = sys.argv[i+1]

    parser = Parser(keyword_file)
    midi_list = []
    with open(midi_list_file) as fp:
        for line in fp:
            file = line.strip()
            midi_list.append(file)

    midi_list = ["/screamlab/tanch/music2vec/test1.mid"]
    if cmd == cmd_parse:
        with Pool(thread_num) as pool:
            for file in midi_list:
                pool.apply_async(
                    parser.parse,
                    args = (file,),
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

if __name__ == '__main__':
    main()
