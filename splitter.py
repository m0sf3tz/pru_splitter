from subprocess import call
import os
import sys



fileName = sys.argv[1]
if len(sys.argv) == 1:
    print("File name required!")
    exit(0) 

if len(sys.argv) == 3: 
    stackOffset = sys.argv[2] #offset into the file where the .data section starts (before this is the stack)   [it's the stack size, defualt is 0x100]
else:
    stackOffset = 100;

print("File name is " + fileName)
print("Stack size is " + str(stackOffset))

sections = {1: ".text:_c_int00*", 2: ".text", 3: ".data"}

print(sections[3])

os.system("rm bin1 2> /dev/null")
os.system("rm bin2 2> /dev/null")
os.system("rm bin3 2> /dev/null")
os.system("rm data.bin 2> /dev/null")
os.system("rm instructions.bin 2> /dev/null")

os.system("bash splitter.sh " + str(sections[1]) + " 1 " + str(fileName)) #cinit
os.system("bash splitter.sh " + str(sections[2]) + " 2 " + str(fileName)) #text
os.system("bash splitter.sh " + str(sections[3]) + " 3 " + str(fileName)) #data


file('instructions.bin','wb').write(file('bin1','rb').read()+file('bin2','rb').read())
filler = (2**11) - os.stat('instructions.bin').st_size
os.system("dd if=/dev/zero bs=1 count=" + str(filler) + " >> instructions.bin") #append zeros


os.system("touch data.bin")

#fill the stack offset in the data section with zeros (not really required...)
os.system("dd if=/dev/zero bs=1 count=" + str(stackOffset) + " >> data.bin") #append zeros
file('data.bin','ab').write(file('bin3','rb').read())
filler = (2**11) - os.stat('bin3').st_size - stackOffset
os.system("dd if=/dev/zero bs=1 count=" + str(filler) + " >> data.bin") #append zeros

