with open("bq-results-20200430-015314-knfowecdwyip.csv") as fh:
    line = fh.readline().strip()
    while line:
        print(line)
        line = fh.readline().strip()