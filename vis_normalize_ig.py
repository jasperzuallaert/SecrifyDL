import sys
ifile = sys.argv[1]

lines = open(ifile).readlines()
total = 0
numseq = 0
for lineN in range(len(lines)//3):
    l3 = [abs(float(x)) for x in lines[3*lineN+2].rstrip().split(',')]
    if len(l3) >= 50:
        total += sum(l3)
        numseq += 1

avg_total_per_seq = total / numseq

for lineN in range(len(lines)//3):
    l1 = lines[3*lineN+0].rstrip()
    l2 = lines[3*lineN+1].rstrip()
    l3 = [float(x) for x in lines[3*lineN+2].rstrip().split(',')]
    normalized = [100*x/(avg_total_per_seq) for x in l3]
    print(l1)
    print(l2)
    print(','.join(f'{x:.3f}' for x in normalized))
