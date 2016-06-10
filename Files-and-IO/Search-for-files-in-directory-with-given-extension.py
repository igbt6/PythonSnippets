import os

def searchForFilesInDirectoryWithGivenExtension(folderPath,extensions:list):
    fileListDir=os.listdir(folderPath)
    files ={}
    for file in fileListDir:
        for extension in extensions:
            if file.endswith(extension):
                if extension not in files:
                    files[extension]=[file]
                else:
                    files[extension].append(file)
    return files
    

    
    
#test
print(searchForFilesInDirectoryWithGivenExtension(r'C:\Users\igbt6\Desktop\uC',['rar', 'pdf']))
#result:
# {
# 'pdf': ['Atollic_Develop_Debug_BootloaderApps_ARMCortex.pdf', 'AVR i ARM7. Programowanie mikrokontrolerów dla każdego.pdf', 'Definitive_Guide_To_The_ARM_Cortex_M3.pdf', 'EmbeddedLinuxPrimer.pdf', 'FFT_routines.pdf', 'FIFO_Tutorial.pdf', 'Magistrale_uC_teoria.pdf', 'marcel_kolodziejczyk_freertos.pdf', 'Mikrokontrolery STM32 w Praktyce-Krzysztof-Paprocki.pdf', 'opisRS232.pdf', 'Procesory DSP dla praktykĂłw -  Henryk A. Kowalski.pdf', 'Projektowanie_systemow_mikroprocesorowych_Pawel_Hadam.pdf', 'stm32100x.pdf', 'systemy_wbudowane_czasu_rzeczywistego.pdf'], 
# 'rar': ['Programming Embedded Systems.rar']
# }