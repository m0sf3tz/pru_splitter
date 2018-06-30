#!/bin/bash

IN_F=./$3
OUT_F=./bin
SECTION=$1

objdump -h $IN_F |
  grep -w $SECTION |
  awk '{print "dd if='$IN_F' of='$OUT_F$2' bs=1 count=$[0x" $3 "] skip=$[0x" $6 "]"}' |
  bash
