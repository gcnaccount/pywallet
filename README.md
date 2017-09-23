# pywallet
Offline Bitcoin Wallet Generation in Python

Implements offline wallet generation to enables secure, offline or cold key generation.
It is designed to conform to the BIP 32, BIP 44, and BIP 39 standards.

The program outputs the seed as a 24-word (264-bit) mnemonic which can be written on 
paper, stamped on metal, or encoded in a fireproof device (e.g. a cryptosteel.com device).
The mnemonic phrases output by this tool may be imported into Wallet  software such as 
Electrum, Mycelium, and Coinomi.

The code is designed for maximum code readability and simplicity rather than for 
optimized performance. This makes it easier to audit the code to ensure the absence 
of backdoors. There are no external library dependencies and the classes altogether 
are less than 400 of code lines. The most critical sections to review are the 
random seed generation and the calculation of public addresses; as the corruption of
either process could result in the loss or theft of coins sent to that address.

This version is not intended for production use. It is recommended to be used only 
as a secondary method to compare against outputs made by other offline wallet generation 
tools (e.g. together with a downloaded version of 
https://www.ledgerwallet.com/support/bip39-standalone.html or 
https://coinomi.com/recovery-phrase-tool.html). This helps to build confidence in the 
proper calculation of wallets and addresses; that it is done correctly and randomly.

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
