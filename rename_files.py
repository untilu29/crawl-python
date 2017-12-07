import os, fnmatch, re

def find_and_replace(directory, file_pattern):
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, file_pattern):
            file_path = os.path.join(path, filename)
            with open(file_path) as fi:
                lines = fi.readlines()
            with open(file_path, "w") as fo:
                for line in lines:
                    s = re.sub('[A-Z]+(\.[A-Z]+)+', lambda m: m.group(0).lower(), line)
                    s = s.replace("THRESHOLD_TO_APPLY_CLUSTERING_AROUND_BIGGEST_CITIES", "threshold.clustering.cities")
                    fo.write(s)

find_and_replace("D:\\PROJECT\\VibeConfig\\projects\\generic\\app\\euc1\\dev", "*.properties")