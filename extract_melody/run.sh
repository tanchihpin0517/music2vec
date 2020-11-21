if [ $HOSTNAME == "screampiano" ]; then
    MIDI="/cache/tanch/lakh_midi_file.txt"
    KEYWORD="./keyword.txt"
    OUT_DIR="/cache/tanch/valid"; mkdir -p $OUT_DIR
    python . -mf $MIDI -kw $KEYWORD -od $OUT_DIR -cmd valid
    find $OUT_DIR -type f > /cache/tanch/valid_midi_file.txt
    
    MIDI="/cache/tanch/valid_midi_file.txt"
    KEYWORD="./keyword.txt"
    OUT_DIR="/cache/tanch/melody"; mkdir -p $OUT_DIR
    python . -mf $MIDI -kw $KEYWORD -od $OUT_DIR -cmd melody
    find $OUT_DIR -type f > /cache/tanch/melody_midi_file.txt
fi
