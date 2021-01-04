from os import listdir
from os.path import join, isdir
import json
distPath = './dist'
yearFolders = [f for f in listdir(distPath) if isdir(join(distPath, f))]
result = {}
for year in yearFolders:
    result[year] = [f for f in listdir(join(
        distPath, year)) if isdir(join(distPath, year, f))]

with open(f'./dist/main.json', 'w') as outfile:
    json.dump(result, outfile)
