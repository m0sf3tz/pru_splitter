#!/bin/bash

IN_F=./a.elf
OUT_F=./bin
SECTION=$1

objdump -h $IN_F |
  grep $SECTION |
  awk '{print "dd if='$IN_F' of='$OUT_F$2' bs=1 count=$[0x" $3 "] skip=$[0x" $6 "]"}' |
  bash
