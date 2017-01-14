function tp {
    touch ~/.tp_cmd
    python3 /usr/bin/tp.py --runfrombash $1 $2 $3
    $(<~/.tp_cmd)
    rm ~/.tp_cmd
}