#!/bin/sh

for i in `seq 1 10`;
do
  echo $i

  # Generate
  python btc.py generate additional passphrase > gen-output.txt
  cat gen-output.txt | grep "Entropy as words" | cut -c 24- > mnemonic.txt

  # Recover
  mnemonic=`cat mnemonic.txt`
  python btc.py recover "$mnemonic" passphrase > rec-output.txt

  # Compare
  cat gen-output.txt | tail -n 36 > gen-verify.txt
  cat rec-output.txt | tail -n 36 > rec-verify.txt

  diff gen-verify.txt rec-verify.txt


done
