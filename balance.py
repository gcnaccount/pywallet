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

from lib.base import *
from lib import coin_types
from urllib import urlopen

import json

def get_price(coin, currency="USD"):
  rate_uri = "https://min-api.cryptocompare.com/data/price?fsym=" + coin.symbol.upper() + "&tsyms=USD"
  response = urlopen(rate_uri)
  result = response.read()
  text = json.loads(result)
  return float(text[currency])

def get_balance(coin, address):
  satoshis_per_coin = 100 * 1000 * 1000 # 100 million
  balance_uri = "https://api.blockcypher.com/v1/" + coin.symbol + "/main/addrs/" + address + "/balance"

  response = urlopen(balance_uri)
  result = response.read()
  text = json.loads(result)
  num_transactions = int(text["n_tx"])
  return float(text["final_balance"]) / float(satoshis_per_coin), num_transactions

def decompress_point(compressed_public_key):
  parity = ord(compressed_public_key[:1]) - 2
  x = compressed_public_key[1:]
  hex_x = binascii.hexlify(x)
  xint = int(hex_x, 16)
  p = secp256k1.x_to_point(xint)
  y_parity = p.y % 2
  if y_parity == parity:
    return p
  else:
    return point(p.x, secp256k1.p - p.y)


def get_account_value(root_public_key, coin, price):

  # Decode base 58 public key
  root_public_key_hex = base58().decode(root_public_key)

  # Decode chain code
  chain_code_offset = 25
  chain_code_length = 64
  chain_code_hex = root_public_key_hex[chain_code_offset:chain_code_offset+chain_code_length]
  
  # Decode public key
  public_key_hex = root_public_key_hex[chain_code_offset+chain_code_length:-8]
  public_key = decompress_point(binascii.unhexlify(public_key_hex))

  # Derive child key from public key only
  account = child_key_derivation(coin, chain_code_hex, public_key)
  receive = account.derive_subkey(0) # Receive address
  change = account.derive_subkey(1) # Change address

  value = 0.0
  coins = 0.0
  print "Path:                   Address:                                Balance (coins):        Balance (USD):"

  # Receive addresses
  for i in range(1000):
    path_i = "m/44'/" + coin.bip32_code + "'/0'/0/" + str(i)
    address_i = receive.derive_subkey(i)
    a = public_address(coin, address_i.get_public_key())
    child_address_i = a.get_address_as_b58(True)
    balance_coin, transactions = get_balance(coin, child_address_i)
    if (transactions == 0):
      break
    balance_usd = float(balance_coin) * price
    value += balance_usd
    coins += balance_coin
    print path_i + "  \t" + child_address_i + "\t" + str(balance_coin).rjust(16) + "\t" + str(balance_usd)
    
  # Change addresses
  for i in range(1000):
    path_i = "m/44'/" + coin.bip32_code + "'/0'/1/" + str(i)
    address_i = change.derive_subkey(i)
    a = public_address(coin, address_i.get_public_key())
    child_address_i = a.get_address_as_b58(True)
    balance_coin, transactions = get_balance(coin, child_address_i)
    if (transactions == 0):
      break
    balance_usd = float(balance_coin) * price
    value += balance_usd
    coins += balance_coin
    print path_i + "  \t" + child_address_i + "\t" + str(balance_coin).rjust(16) + "\t" + str(balance_usd)
    
  return value, coins


def main():

  if len(argv) < 3:
    command = argv[0]
    print "USAGE: python " + command + " <BIP32 Account Extended Public Key> <coin type>"
    exit(1)

  root_public_key = argv[1]
  
  if argv[2] == "btc":
    coin = coin_types.btc
  elif argv[2] == "bch":
    coin = coin_types.bch
  elif argv[2] == "ltc":
    coin = coin_types.ltc
  else:
    print "Unknown coin type: " + argv[2] + ".  Supported coin types: 'btc', 'bch', 'ltc'."
    exit(1)
  
  # Get current market value of coin
  price = get_price(coin)
  print
  print "Coin type:                      " + coin.name
  print "Current price (USD):            $" + str(price)
  print

  # Lookup wallet balances
  value, coins = get_account_value(root_public_key, coin, price)

  print
  print "Total coins:                     " + str(coins) + " " + coin.symbol.upper()
  print "Total account value (USD):      $" + str(value)
  print

if __name__ == "__main__":
  main()
