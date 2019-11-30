import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p,""--paths",dest='paths', nargs='+', help="paths to corpus data")
parser.add_argument("-t","--threshold",dest='threshold', help="threshold allowed between pairs")
parser.add_argument("-l","--lines", dest='lines', help="number of lines of the corpus")
args = parser.parse_args()


rem = 0

files = [open(f) for f in args.paths]
out_files_names = ['.'.join(f.split('.')[0:-1]) + '.filtered.' + f.split('.')[-1] for f in args.paths]
out_files = [open(f,'w+') for f in out_files_names]
r_max = 1.0+float(args.threshold)
r_min = 1.0-float(args.threshold)


for i in range(int(args.lines)):
    lines  = [f.readline().replace('\n','') for f in files]
    is_parallel = True
    for li in lines:
        li = li.split()
        if is_parallel:    
            for lj in lines:
                lj = lj.split()
                diff = float(len(li))/float(len(lj))
                if diff < r_min or diff > r_max:
                    is_parallel = False
                    rem += 1
                    print('* Removed sentences:', rem)
                    print('* s1:', li)
                    print('* s2:', lj)
                    print('* diff:',diff)
                    print('*************************')
                    break

    if is_parallel:
        for i,l in enumerate(lines):
            print(l, file=out_files[i])

for i in range(len(files)):
    files[i].close()

for i in range(len(out_files)):
    out_files[i].close()

