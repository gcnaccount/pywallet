# pywallet
Offline Multicoin Wallet Generation in Python

Implements offline wallet generation to support secure, manual, offline, and cold wallet generation.
It supports multple coin types, including Bitcoin (BTC), Bitcoin cash (BCH), and Litecoin (LTC).
It conforms to the BIP 32, BIP 44, and BIP 39 standards for Hierarchical Deterministic (HD) wallets.

The software (btc.py / bch.py / ltc.py) outputs the wallet seed as a 24-word (264-bit) mnemonic 
which can be written on paper, stamped on to metal, or encoded in a fireproof device (e.g. a 
cryptosteel.com device or similar). The mnemonic phrases output by this tool may be imported 
into wallet software such as Electrum, Mycelium, and Coinomi or any wallet that conforms to 
BIP 44 address paths and supports importing BIP 39 menmonic phrases.

Note that the phrase output by any of the generation scripts (btc.py / bch.py / ltc.py) can be 
used to recover the same HD wallet seed using any of those three scripts.

The code is designed for maximum code readability and simplicity rather than for 
optimized performance. This makes it easier to audit the code to ensure the absence 
of backdoors. There are no external library dependencies and important classes (in 
base.py) are less than 500 lines of code. The most critical sections to review 
in any wallet generation software relate to the random seed generation and the 
derivation of public addresses; as the corruption of either process could result 
in the loss or theft of coins sent to that address.

Note that this software is not intended for production use. It should only 
be used as a secondary or tertiary generation means to compare against 
outputs made by other offline wallet generation tools, e.g., together 
with a downloaded copie of generation tools such as:

* https://iancoleman.github.io/bip39/ together with
* https://www.ledgerwallet.com/support/bip39-standalone.html together with
* https://coinomi.com/recovery-phrase-tool.html

Using this tool, with its easily audited code, helps establish confidence in the 
proper calculation of wallets and addresses, which helps to build confidence that
generation is performed both correctly and randomly.

Usage:

Execute internal tests:

  $ python <btc.py/bch.py/ltc.py> test

    This runs a suite of tests to ensure correct operation using published test vectors. This 
    should be run at least once on the machine on which you intend to generate keys. The test 
    script ("test-btc.sh") performs additional tests. It checks that the outputs of this tool 
    can be used to recover the same key.

Generate new private key:

  $ python <btc.py/bch.py/ltc.py> generate [additional entropy] [passphrase]

    This generates a new random key and outputs a 24-word mnemonic phrase which may be used to 
    recover the key at any future time. Additional entropy may be supplied as an additional string, 
    such as the outcome of 256 coin tosses, or 100 die rolls. This should be done if the entropy 
    source on the offline computer is suspect. An optional passphrase may be supplied but this must 
    be remembered and re-entered along with the mnemonic to complete the recovery.

Recover a private key:

  $ python <btc.py/bch.py/ltc.py> recover "mnemonic phrase" [passphrase]

    This recovers a private key from the 24-word mnemonic and optionally a passphase (if one was 
    supplied during generation). It is prudent to perform a recovery of any newly generated and 
    backed up private key to ensure it is properly recorded *before* sending any coins to it.  
    Additionally, verifying proper receipt and spendability with a low value of coins is good to 
    ensure a correct correspondance between the displayed public address and the private key.
