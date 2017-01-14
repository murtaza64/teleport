#!/usr/local/bin/python3
import argparse, os, sys

HOME = os.environ['HOME']
TPCONFIG = HOME+'/.tp'
TPCMD = HOME+'/.tp_cmd'

def eprint(*args, **kwargs):
    with open(TPCMD, 'w') as f:
        print(*args, file=f, **kwargs)

def g(s):
    return '\033[32m'+s+'\033[0m'
    
def save_config():
    with open(TPCONFIG, 'w') as f:
        for k, v in d.items():
            f.write(k+':'+v+'\n')

d = {}

if len(sys.argv) == 1 or sys.argv[1] != '--runfrombash':
    print('tp: error: make sure tp bash function is defined')
    exit(1)
else:
    sys.argv.pop(1)

with open(TPCONFIG, 'r') as f:
    for l in f:
        warp, loc = l.split(':')
        d[warp] = loc.strip()

parser = argparse.ArgumentParser(prog='tp', 
    description='Teleport around your filesystem', usage='tp [-a|-r] portal')
parser.add_argument('portal', nargs='?', help='name of portal to go through')
parser.add_argument('-a', action='store_true', help='add new portal')
parser.add_argument('-r', action='store_true', help='remove portal')
parser.add_argument('path', nargs='?', help='path for new portal')
args = parser.parse_args()

if args.a and args.r:
    parser.print_usage()
    print('tp: error: choose one of -a or -r' )
    exit(1)
if args.a:
    a_parser = argparse.ArgumentParser(prog='tp -a', 
        description='Add a new tp portal', usage='tp -a portal [path]')
    a_parser.add_argument('portal', help='nickname for target path')
    a_parser.add_argument('path', nargs='?',help='target path (defaults to current directory)')
    args = a_parser.parse_args(sys.argv[2:])

    if args.portal in d:
        print('warning: {} is already a portal to {}'.format((args.portal), d[args.portal]))
        c = input('replace it (Y/n)?')
        if c.lower() == 'n':
            exit(0)
    if not args.path:
        path = os.path.abspath('.')
    else:
        try:
            os.chdir(args.path)
            path = os.path.abspath('.')
        except FileNotFoundError:
            print('warning: directory {} does not exist yet'.format(args.path))
            path = os.path.abspath(args.path)

    
    d[args.portal] = path
    save_config()
    print('created portal {} to {}'.format(g(args.portal), path))

elif args.r:
    r_parser = argparse.ArgumentParser(prog='tp -r', 
        description='Remove a tp portal', usage='tp -r portal')
    r_parser.add_argument('portal', help='name of portal to remove')
    args = r_parser.parse_args(sys.argv[2:])

    if args.portal in d:
        print('removed portal {} to {}'.format(g(args.portal), d[args.portal]))
        del d[args.portal]
        save_config()
    else:
        print('tp -r: error: portal {} does not exist'.format(g(args.portal)))
    
elif args.portal:
    if args.portal in d:
        eprint('cd', d[args.portal])
    else:
        print('tp: error: portal {} does not exist'.format(g(args.portal)))
else:
    d_sorted = sorted([(k, v) for k, v in d.items()], key=lambda p: p[0])
    l = len(max(d, key=len)) + 1
    for k, v in d_sorted:
        if(os.path.commonprefix((HOME, v)) == HOME):
            print(g(k) + ':'+' '*(l-len(k)) + '~'+v[len(HOME):])
        else:   
            print(g(k) + ':'+' '*(l-len(k)) + os.path.realpath(v))


# print(d)
# print(sys.argv)
