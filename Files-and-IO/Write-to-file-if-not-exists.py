import os
if not os.path.exists('testfile.txt'):
    with open('testfile.txt', 'wt') as f:
        f.write('TEST STRING\n')
else:
    print('File already exists!')