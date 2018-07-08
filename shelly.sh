#!/bin/bash
# This line is a comment.



rm for_real.out 
rm for_real.map 
rm -rf pru-cbuf-fw 

git clone https://github.com/m0sf3tz/pru-cbuf-fw.git

cp pru-cbuf-fw/Debug/for_real.out .
cp pru-cbuf-fw/Debug/for_real.map .




