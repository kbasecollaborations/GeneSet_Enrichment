import gzip

with gzip.open('210_paper.gmt.gz','rt') as f:
    for line in f:
        print('got line', line)
