#!/bin/sh

a=0

while [ $a -lt 10 ]
do
   python classificador_vinhos.py $a
   a=`expr $a + 1`
done


