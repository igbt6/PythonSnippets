for codec in ['latin_1', 'utf_8', 'utf_16','ascii']:
    print(codec, 'Łószczykięwicz'.encode(codec,errors='ignore'), sep='\t')
    print('Łószcz')
    
    
    
import codecs
f = codecs.open('myutf8file.txt','r', encoding='utf-8',errors='ignore')
file=f.read()