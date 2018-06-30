from subprocess import call
import os

sections = {1: ".text:_c_int00*", 2: ".text"}

os.system("rm bin1")
os.system("rm bin2")
os.system("rm data.bin")

os.system("bash wtf.sh " + str(sections[1]) + " 1") #cinit
os.system("bash wtf.sh " + str(sections[2]) + " 2") #text

file('instructions.bin','wb').write(file('bin1','rb').read()+file('bin2','rb').read())

filler = (2**11) - os.stat('instructions.bin').st_size

os.system("dd if=/dev/zero bs=1 count=" + str(filler) + " >> instructions.bin") #append zeros



