# pywallet
Offline Bitcoin Wallet Generation in Python

Implements: https://www.ledgerwallet.com/support/bip39-standalone.html (wallet generation)
 
Enables secure, offline key generation, according to BIP 32, BIP 44, and BIP 39.

It outputs the seed as a 24-word (264-bit) mnemonic which can be written on paper or in 
a fire proof cryptosteel.com device.  The mnemonic phrase may be imported into Wallet  
software such as Electrum, Mycelium, and Coinomi.


Usage:

Execute internal tests:

  $ python btc.py test

    This runs a suite of tests to ensure correct operation using published test vectors. This 
    should be run at least once on the machine on which you intend to generate keys. The  test 
    script ("test-btc.sh") performs additional tests. It checks that the outputs of this tool 
    can be used to recover the same key.

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
