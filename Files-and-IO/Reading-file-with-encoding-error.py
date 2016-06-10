#Error here:
# Traceback (most recent call last):
  # File "Reading-file-with-encoding-error.py", line 2, in <module>
    # print(f.read())
  # File "C:\Python35\lib\encodings\cp852.py", line 19, in encode
    # return codecs.charmap_encode(input,self.errors,encoding_map)[0]
# UnicodeEncodeError: 'charmap' codec can't encode character '\ufffd' in position 4: character maps to <undefined>
#with open('Reading-file-with-encoding-error.txt', 'rt') as f:
#    print(f.read())

#always check    
import sys
print(sys.stdout.encoding) 


   
#1 replace bad characters with Unicode U+fffd replacement character
import codecs
f = codecs.open('Reading-file-with-encoding-error.txt', encoding='utf-8')
for line in f:
    # print(line.encode('utf-8'))

#2 ignore bad chars 
with open('Reading-file-with-encoding-error.txt', 'rt', encoding='ascii', errors='ignore') as f:
    print(f.read())

#3 linux and others
with open('Reading-file-with-encoding-error.txt', 'rb') as f:
    print(f.read().decode("utf-8"))    
   
#4 linux and others
with open('Reading-file-with-encoding-error.txt', 'rb') as f:
    print(f.read().decode("cp852"))
    
#5 will never raise UnicodeDecodeError when reading data 
with open('Reading-file-with-encoding-error.txt', 'rt', encoding='ascii', errors='surrogateescape') as f:
    print(f.read())