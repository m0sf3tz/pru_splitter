from subprocess import call
import os
import sys



fileName = sys.argv[1]
if len(sys.argv) == 1:
    print("File name required!")
    exit(0) 

mapfile = sys.argv[2]

if len(sys.argv) == 4: 
    stackOffset = int(sys.argv[3]) #offset into the file where the .data section starts (before this is the stack)   [it's the stack size, defualt is 0x100]
else:
    stackOffset = 0x100;

print("File name is  : " + fileName)
print("Map file is   : " + mapfile)
print("Stack size is : " + str(stackOffset))

sections = {1: ".text:_c_int00*", 2: ".text", 3: ".bss", 4:".data", 5:"rodata"}


os.system("rm bin1 2> /dev/null")
os.system("rm bin2 2> /dev/null")
os.system("rm bin3 2> /dev/null")
os.system("rm bin4 2> /dev/null")
os.system("rm bin5 2> /dev/null")

os.system("rm data.bin 2> /dev/null")
os.system("rm instructions.bin 2> /dev/null")

os.system("bash splitter.sh " + str(sections[1]) + " 1 " + str(fileName)) #cinit
os.system("bash splitter.sh " + str(sections[2]) + " 2 " + str(fileName)) #text
#os.system("bash splitter.sh " + str(sections[3]) + " 3 " + str(fileName)) #bss  //duh... will aways be empty
os.system("bash splitter.sh " + str(sections[4]) + " 4 " + str(fileName)) #data
os.system("bash splitter.sh " + str(sections[5]) + " 5 " + str(fileName)) #rodata

file('instructions.bin','wb').write(file('bin1','rb').read()+file('bin2','rb').read())
filler = (2**11) - os.stat('instructions.bin').st_size
os.system("dd if=/dev/zero bs=1 count=" + str(filler) + " >> instructions.bin" + " 2> /dev/null" + " status=none") #append zeros


os.system("touch data.bin")

              #offset #len 
bssInfo    = []     
dataInfo   = []      
rodataInfo = []
     
print("")
with open(mapfile) as fp:  
   line = fp.readline()
   cnt = 1
   while line:
       arr = line.split() 
       if arr:
          if arr[0] == '.bss':
              print("BSS info... section, page, offset, len")
              print(arr)
              print("")
              bssInfo.append(int(arr[2],16))
              bssInfo.append(int(arr[3],16))  
          if arr[0] == '.data':
              print("DATA info... section, page, offset, len")
              print(arr)
              print("")
              dataInfo.append(int(arr[2],16))
              dataInfo.append(int(arr[3],16))   
          if arr[0] == '.rodata':
              print("RODATA info... section, page, offset, len")
              print(arr)
              print("")
              rodataInfo.append(int(arr[2],16))
              rodataInfo.append(int(arr[3],16))
       line = fp.readline()

if not bssInfo:
    bssInfo = [0,0,0,0]
    print("No bss Section")
else:
    #we need to create a fake BSS section and fill it with zeros since it won't be in an object dump since BSS is 0
    os.system("touch bin3")
    os.system("dd if=/dev/zero bs=1 count=" + str(bssInfo[1]) + " >> bin3" + " 2> /dev/null"+ " status=none")
if not dataInfo:
    bssInfo = [0,0,0,0]
    print("No data Section")
if not rodataInfo:
    rodataInfo = [0,0,0,0]
    print("No rodata Section")
    
#fill the stack offset in the data section with zeros (not really required since we memset it all to zero before loading, but w/e)
os.system("dd if=/dev/zero bs=1 count=" + str(stackOffset) + " >> data.bin" + " 2> /dev/null"+ " status=none") #append zeros

file('data.bin','ab').write(file('bin3','rb').read())    #bss
file('data.bin','ab').write(file('bin4','rb').read())    #data
file('data.bin','ab').write(file('bin5','rb').read())    #rodata



filler = (2**11) - os.stat('bin3').st_size - os.stat('bin4').st_size -os.stat('bin5').st_size - stackOffset

os.system("dd if=/dev/zero bs=1 count=" + str(filler) + " >> data.bin" + " 2> /dev/null" + " status=none") #append zeros

