#!/bin/bash

for j in {1..3}
do
  for i in {1..48}
  do
    melia_condor ./dcs @geo -dlogOptions "lexMode=$i" -execDir "state/execs/lex-$j-$i.exec" r$i
  done
done
