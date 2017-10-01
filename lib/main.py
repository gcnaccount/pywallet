################################################################################################
# 
# Copyright (c) 2017 Jason Resch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################################

################################################################################################
# Imports
################################################################################################

from base import *

################################################################################################
# CLI Functions
################################################################################################

def run_tests(coin):
  if coin.symbol == "btc":
    from test import btc_test_vectors as test_vectors
  elif coin.symbol == "bch":
    from test import bch_test_vectors as test_vectors
  elif coin.symbol == "ltc":
    from test import ltc_test_vectors as test_vectors
  else:
    raise Exception("Unkown coin type")
  test_vectors.bip32_tests().execute_all_tests()
  test_vectors.bip39_tests().execute_all_tests()
  test_vectors.bip44_tests().execute_all_tests()
  print "All tests completed successfully"

command = argv[0]

def print_usage_and_exit():
  print "USAGE: python " + command + " test"
  print "USAGE: python " + command + " generate [additional entropy] [passphrase]"
  print "USAGE: python " + command + " recover \"mnemonic phrase\" [passphrase]"
  exit(1)

################################################################################################
# Generate random seed
################################################################################################

def main(coin):

  # Parse command line options
  if len(argv) < 2:
    print_usage_and_exit()
    exit(1)

  supplied_entropy = ""
  passphrase = ""

  if len(argv) >= 2:

    word_encoder = mnemonic()

    if (argv[1].lower() == "test"):
      run_tests(coin)
      exit(0)
	
    if (argv[1].lower() == "generate"):
      if len(argv) >= 3:
        supplied_entropy = argv[2]
      if len(argv) >= 4:
        passphrase = argv[3]
	  
      print "Generating new " + coin.name + " private key..."
      print
      print "Additional Entropy:   ", supplied_entropy
      print "Passphrase:           ", passphrase

      # Generate some randomness
      generated_entropy = SystemRandom().randint(1, pow(2, 384))
      print "System entropy:       ", generated_entropy
	
      # Combined entropy
      combined_entropy = str(generated_entropy) + supplied_entropy
      print "Combined Entropy:     ", combined_entropy
	
      # Hash to form conditioned entropy
      entropy = sha256(combined_entropy).digest()
      print "Conditioned Entropy:  ", binascii.hexlify(entropy)

      # Create word set
      word_set = word_encoder.encode(entropy)
      recovered = word_encoder.decode(word_set)
      assert entropy == recovered, "Problem decoding generated phrase"
      print "Entropy as words:     ", word_set

    elif (argv[1].lower() == "recover"):
      if len(argv) >= 3:
        word_set = argv[2].strip().lower()
        word_encoder.decode(word_set)
      else:
        print "USAGE: python " + command + " recover \"mnemonic phrase\" [passphrase]"
        exit(1)
      if len(argv) >= 4:
        passphrase = argv[3]
        
      print "Restoring existing " + coin.name + " private key..."
      print
      print "Mnemonic phrase:      ", word_set
      print "Passphrase:           ", passphrase
    else: 
      print_usage_and_exit()

  print

  # Generate seed from words
  seed = word_encoder.generate_seed(word_set, passphrase)
  print "Seed:                 ", binascii.hexlify(seed)

  print

  ################################################################################################
  # Generate private key and chain code from seed
  ################################################################################################

  # Hash random seed and parse it to secret key and chain code
  seed_hmac = hmac.new("Bitcoin seed", seed, sha512).hexdigest()
  secret_key = seed_hmac[:64]
  chain_code = binascii.unhexlify(seed_hmac[64:])

  private_key = int(secret_key, 16)
  if (private_key > secp256k1.r):
    raise Exception("Private key is too large!!!")

  w = wallet(coin=coin, private_key_int=private_key)

  print "Private Key as Int:   ", w.get_private_key_as_int()

  private_key_hex = w.get_private_key_as_hex()
  print "Private Key as Hex:   ", private_key_hex

  print

  ################################################################################################
  # Export and Import WIF
  ################################################################################################

  wif = w.get_wif()
  print "Private Key as WIF:   ", wif

  valid = validate_wallet_input_format(wif)
  print "WIF is valid:         ", valid 
  assert valid == True, "WIF is invalid"

  imported_wallet = wallet(coin=coin, private_key_wif=wif)
  assert w.get_private_key_as_int() == imported_wallet.get_private_key_as_int()
  assert w.get_address_as_b58() == imported_wallet.get_address_as_b58()
  assert validate_address(imported_wallet.get_address_as_b58())
  assert w.get_address_as_b58(True) == imported_wallet.get_address_as_b58(True)
  assert validate_address(imported_wallet.get_address_as_b58(True))

  # Create Wallet form WIF
  print

  ################################################################################################
  # Compute Public Key
  ################################################################################################

  # Derive Public Key from Private Key
  public_key = w.get_public_key_as_point()
  print "Public Key Point:     ", public_key
  print "Public Key as Hex:    ", public_key.as_hex()

  print

  ################################################################################################
  # Compute Address
  ################################################################################################

  # Form address
  hex_address = w.get_address_as_hex()
  print "Hex address:          ", hex_address

  # Convert to base 58
  address = w.get_address_as_b58()
  print "Address (B58):        ", address

  ################################################################################################
  # Verify Address
  ################################################################################################

  valid = validate_address(address)
  print "Address is valid:     ", valid 
  assert valid == True, "Address is invalid"

  print

  ################################################################################################
  # Create Child Keys
  ################################################################################################

  chain_code_hex = binascii.hexlify(chain_code)
  print "Chain Code as Hex:    ", chain_code_hex

  print

  # Create hierarchical deterministic wallet
  ckd = child_key_derivation(coin, chain_code_hex, public_key, private_key)
  print "BIP 32 Root Private:  ", ckd.serialize_private()
  print "BIP 32 Root Public:   ", ckd.serialize_public()

  print

  # Derive child key using private key
  child1 = ckd.derive_subkey(0)

  # Derive child key from public key only
  ckd2 = child_key_derivation(coin, chain_code_hex, public_key)
  child2 = ckd2.derive_subkey(0)
  assert child1.get_public_key() == child2.get_public_key()
  assert child1.get_chain_code() == child2.get_chain_code()

  path = "m/44'/" + coin.bip32_code + "'/0'"
  account_extended_key = parse_path(coin, seed, path)
  print "Acct Ext Private Key: ", account_extended_key.serialize_private()
  print "Acct Ext Public Key:  ", account_extended_key.serialize_public()
  print "Acct Ext 44 Path:     ", account_extended_key.get_path()

  print

  path = "m/44'/" + coin.bip32_code + "'/0'/0"
  bip_44_key = account_extended_key.derive_subkey(0)
  bip_44_key_2 = parse_path(coin, seed, path)
  print "BIP 44 Private Key:   ", bip_44_key.serialize_private()
  print "BIP 44 Public Key:    ", bip_44_key.serialize_public()
  print "BIP 44 Path:          ", bip_44_key.get_path()

  assert bip_44_key.serialize_private() == bip_44_key_2.serialize_private()
  assert bip_44_key.serialize_public() == bip_44_key_2.serialize_public()
  assert bip_44_key.get_path() == bip_44_key_2.get_path()

  print
  
  print "Path:                   Address:                                Public Key:                                                             Private Key:"
  for i in range(11):
    path_i = "m/44'/" + coin.bip32_code + "'/0'/0/" + str(i)
    address_i = bip_44_key.derive_subkey(i)
    address_i2 = parse_path(coin, seed, path_i)
    w = wallet(coin, address_i.get_private_key())
    
    child_private_key = w.get_wif(True)
    child_public_key = binascii.hexlify(ser_p(address_i.get_public_key()))
    child_address_i = w.get_address_as_b58(True)
    
    print path_i + "  \t" + child_address_i + "\t" + child_public_key + "\t" + child_private_key

    assert validate_address(w.get_address_as_b58(True))
    assert validate_address(w.get_address_as_b58(False))

    w2 = wallet(coin, address_i2.get_private_key())
    assert address_i.get_path() == address_i2.get_path(), str(address_i.get_path()) + " != " + str(address_i2.get_path())
    assert w.get_wif(True) == w2.get_wif(True)
    assert w.get_wif(False) == w2.get_wif(False)
    assert ser_p(address_i.get_public_key()) == ser_p(address_i2.get_public_key())
    assert w.get_address_as_b58(True) == w2.get_address_as_b58(True)
    assert w.get_address_as_b58(False) == w2.get_address_as_b58(False)

  print
