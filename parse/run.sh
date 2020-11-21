if [ $HOSTNAME == "screampiano" ]; then
    MIDI="/cache/tanch/melody_midi_file.txt"
    KEYWORD="/screamlab/tanch/music2vec/melody_keyword.txt"
    python . -mf $MIDI -kw $KEYWORD -cmd parse
fi
