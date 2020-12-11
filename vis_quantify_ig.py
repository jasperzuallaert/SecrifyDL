proteins = 'ACDEFGHIKLMNPQRSTVWY'

def prot_averagePerPosition(lines,n):
    import numpy as np
    first15 = np.zeros((n,20))
    last15 = np.zeros((n,20))
    ctr_first =np.zeros((n,20))
    ctr_last = np.zeros((n,20))
    for i in range(len(lines) // 3):
        l2 = lines[3 * i + 1].strip().split(',')
        l3 = lines[3 * i + 2].strip().split(',')
        if len(l3) >= int(n):
            for j in range(n):
                if l2[j] in proteins:
                    first15[j][proteins.index(l2[j])] += float(l3[j])
                    ctr_first[j][proteins.index(l2[j])] += 1
                if l2[-(j+1)] in proteins:
                    last15[-(j+1)][proteins.index(l2[-(j+1)])] += float(l3[len(l2)-(j+1)])
                    ctr_last[-(j+1)][proteins.index(l2[-(j+1)])] += 1

    first15 /= ctr_first
    last15 /= ctr_last

    for j in range(20):
        print(proteins[j],end=',')
        for i in range(n):
            print(f'{first15[i][j]:.3f}',end=',')
        print(',',end='')
        for i in range(n):
            print(f'{last15[i][j]:.3f}',end=',')
        print()

def prot_getAveragePerAA(lines):
    import numpy as np
    avgNml = np.zeros(20)
    avgAbs = np.zeros(20)
    count = np.zeros(20)
    for i in range(len(lines) // 3):
        l2 = lines[3 * i + 1].strip().split(',')
        l3 = lines[3 * i + 2].strip().split(',')
        for aa,sct in zip(l2,l3):
            if aa in proteins:
                avgNml[proteins.index(aa)] += float(sct)
                avgAbs[proteins.index(aa)] += abs(float(sct))
                count[proteins.index(aa)] += 1

    avgNml = avgNml / count
    avgAbs = avgAbs / count

    print(','+','.join(proteins))
    print('avg,'+','.join([f'{x:.3f}' for x in avgNml]))
    print('avg (abs),'+','.join([f'{x:.3f}' for x in avgAbs]))

def prot_getIndividualPatternGraphsPerAA(lines,divide_in_groups = 10):
    import numpy as np
    counts = np.zeros((21,divide_in_groups),dtype=np.int32)
    scores = np.zeros((21,divide_in_groups),dtype=np.float32)

    for i in range(len(lines) // 3):
        # l1 = [float(x) for x in lines[3 * i].strip().split(',')]
        l2 = lines[3 * i + 1].strip().split(',')
        l3 = lines[3 * i + 2].strip().split(',')
        for pos,(aa,sct) in enumerate(zip(l2,l3)):
            if aa in proteins:
                bin = int(pos//(np.ceil(len(l2)/divide_in_groups)))
                counts[proteins.index(aa)][bin] += 1
                scores[proteins.index(aa)][bin] += float(sct)
                scores[20][bin] += abs(float(sct))
                counts[20][bin] += 1
    print(','+','.join([f'{x:.3f}' for x in range(divide_in_groups)]))
    scores = scores / counts
    for i in range(20):
        print(proteins[i]+','+','.join([f'{x:.3f}' for x in scores[i]]))
    print('all (abs val) per pos,'+','.join([f'{x:.3f}' for x in scores[20]]))



def doVis(allLines):
    lines_for_vis = []
    for line in allLines:
        lines_for_vis.append(line.strip())

    print('lines_for_vis',len(lines_for_vis))
    print()
    s = ','+','.join([str(x) for x in range(15)]) + ',,' + ','.join([str(x) for x in range(15)][::-1])
    print(s)
    prot_averagePerPosition(lines_for_vis,15)
    print()
    prot_getAveragePerAA(lines_for_vis)
    print()
    prot_getIndividualPatternGraphsPerAA(lines_for_vis,divide_in_groups = 20)

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    all_lines = open(filename).readlines()
    doVis(all_lines)


