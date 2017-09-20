# pywallet
Offline Bitcoin Wallet Generation in Python

Implements: https://www.ledgerwallet.com/support/bip39-standalone.html (wallet generation)
 
Enables secure, offline key generation, according to BIP 32, BIP 44, and BIP 39.

It outputs the seed as a 24-word (264-bit) mnemonic which can be written on paper or in 
a fire proof cryptosteel.com device.  The mnemonic phrase may be imported into Wallet Apps 
such as Electrum, Mycelium, and Coinomi


Usage:

Generate new private key:

$ python btc.py generate [additional entropy] [passphrase]

This generates a new random key and outputs a 24-word mnemonic phrase which may be used to 
recover the key at any future time. Additional entropy may be supplied as an additional string, 
such as the outcome of 256 coin tosses, or 100 die rolls. This should be done if the entropy 
source on the offline computer is suspect. An optional passphrase may be supplied but this must 
be remembered and re-entered along with the mnemonic to complete the recovery.

Recover a private key:

$ python btc.py recover "mnemonic phrase" [passphrase]

This recovers a private key from the 24-word mnemonic and optionally a passphase (if one was 
supplied at the creation). It is very prudent to perform a recovery of a newly generated and 
backed up private key to ensure it is properly recorded before sending any coins to it.  
Additionally, verifying proper receipt and spendability with a small number of coins is good to 
ensure a correct correspondance between the public address and the private key.

License:

Copyright (c) 2017 Jason Resch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
