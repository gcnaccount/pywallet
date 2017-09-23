#!/usr/bin/python
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
#
# Implements: https://www.ledgerwallet.com/support/bip39-standalone.html (wallet generation)
# 
# Enables secure, offline key generation, according to BIP 32, BIP 44, and BIP 39.
#
# It outputs the seed as a 24-word (264-bit) mnemonic which can be written on paper or in 
# a fire proof cryptosteel.com device.  The mnemonic phrase may be imported into Wallet Apps 
# such as Electrum, Mycelium, and Coinomi
#
# Usage:
#
# Execute internal tests:
#
# $ python btc.py test
#
# This runs a suite of tests to ensure correct operation using published test vectors. This 
# should be run at least once on the machine on which you intend to generate keys. The  test 
# script ("test-btc.sh") performs additional tests. It checks that the outputs of this tool 
# can be used to recover the same key.
#
# Generate new private key:
#
# $ python btc.py generate [additional entropy] [passphrase]
#
# This generates a new random key and outputs a 24-word mnenomic phrase which may be used to 
# recover the key at any future time. Additional entropy may be supplied as an additional string, 
# such as the outcome of 256 coin tosses, or 100 die rolls. This should be done if the entropy 
# source on the offline computer is suspect. An optional passphrase may be supplied but this must 
# be remembered and re-entered along with the mnemonic to complete the recovery.
#
# Recover a private key:
#
# $ python btc.py recover [passphrase]
#
# This recovers a private key from the 24-word mnemonic and optionally a passphase (if one was 
# supplied at the creation). It is very prudent to perform a recovery of a newly generated and 
# backed up private key to ensure it is properly recorded before sending any coins to it.  
# Additionally, verifying proper receipt and spendability with a small number of coins is good to 
# ensure a correct correspondance between the public address and the private key.
#
################################################################################################

################################################################################################
# Imports
################################################################################################

from random import SystemRandom
from hashlib import sha512, sha256
from sys import argv, exit

import binascii
import hashlib
import hmac
import struct

################################################################################################
# Utility Functions
################################################################################################

# Converts an integer to a hexadecimal string
def int_to_hex(num, bit_length=None):
  hex_str = hex(num)
  hex_str = hex_str[2:] # Remove leading "0x"
  if hex_str[-1:] == "L":
    hex_str = hex_str[:-1] # Removing trailing L
  if not bit_length is None:
    hex_str = hex_str.zfill(bit_length / 4) # Add leading zeros
  return hex_str

################################################################################################
# Elliptic Curve Functions
################################################################################################

class curve:
  def __init__(self, a, b, p, r, g):
    self.a = a
    self.b = b
    self.p = p
    self.r = r
    self.g = g

  def mod_inv(self, x):
    return pow(x, self.p - 2, self.p)

  def add_points(self, p, q):
    s = (p.y - q.y) * self.mod_inv(p.x - q.x) % self.p
    x = (s*s - (p.x + q.x)) % self.p
    y = (s * (p.x - x) - p.y) % self.p
    return point(x, y)

  def point_double(self, p):
    s = (3 * p.x * p.x + self.a) * self.mod_inv(2 * p.y) % self.p
    x = (s*s - 2 * p.x) % self.p
    y = (s * (p.x - x) - p.y) % self.p
    return point(x, y)

  def multiply_point(self, c, n):
    r = None
    cpow2 = c
    while (n > 0):
      if (n & 1 == 1):
        if (r is None):
          r = cpow2
        else:
          r = self.add_points(r, cpow2)
      n = (n >> 1)
      cpow2 = self.point_double(cpow2)
    return r

class point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False

  def __ne__(self, other):
    return not self.__eq__(other)

  def __str__(self):
    return "(" + str(self.x) + ", " + str(self.y) + ")"

  def as_hex(self):
    prefix = "04"
    x_data = int_to_hex(self.x, 256)
    y_data = int_to_hex(self.y, 256)
    return prefix + x_data + y_data

  def as_bin(self):
    hex = self.as_hex()
    return binascii.unhexlify(hex)

################################################################################################
# Certicom Curve SEC P-256 (secp256k1)
################################################################################################

# From: http://www.secg.org/sec2-v2.pdf

# Certicom SEC P-256
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F # 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1
r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
a = 0
b = 7

Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

G = point(Gx, Gy)

secp256k1 = curve(a, b, p, r, G)

################################################################################################
# Encoding Functions
################################################################################################

class base58:
  def __init__(self):
    self.alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

  def encode(self, hex_input):
    num = int(hex_input, 16)
    encoded = ""
    while (num > 0):
      remainder = num % 58
      num /= 58
      encoded = self.alphabet[remainder] + encoded
    return encoded

  def decode(self, b58_encoded):
    result = 0
    mul = 1
    reversed = b58_encoded[::-1]
    for c in reversed:
      result += mul * self.alphabet.index(c)
      mul *= 58
    return int_to_hex(result)

class mnemonic:
  def __init__(self):
    self.dict = "abandon ability able about above absent absorb abstract absurd abuse access accident account accuse achieve acid acoustic acquire across act action actor actress actual adapt add addict address adjust admit adult advance advice aerobic affair afford afraid again age agent agree ahead aim air airport aisle alarm album alcohol alert alien all alley allow almost alone alpha already also alter always amateur amazing among amount amused analyst anchor ancient anger angle angry animal ankle announce annual another answer antenna antique anxiety any apart apology appear apple approve april arch arctic area arena argue arm armed armor army around arrange arrest arrive arrow art artefact artist artwork ask aspect assault asset assist assume asthma athlete atom attack attend attitude attract auction audit august aunt author auto autumn average avocado avoid awake aware away awesome awful awkward axis baby bachelor bacon badge bag balance balcony ball bamboo banana banner bar barely bargain barrel base basic basket battle beach bean beauty because become beef before begin behave behind believe below belt bench benefit best betray better between beyond bicycle bid bike bind biology bird birth bitter black blade blame blanket blast bleak bless blind blood blossom blouse blue blur blush board boat body boil bomb bone bonus book boost border boring borrow boss bottom bounce box boy bracket brain brand brass brave bread breeze brick bridge brief bright bring brisk broccoli broken bronze broom brother brown brush bubble buddy budget buffalo build bulb bulk bullet bundle bunker burden burger burst bus business busy butter buyer buzz cabbage cabin cable cactus cage cake call calm camera camp can canal cancel candy cannon canoe canvas canyon capable capital captain car carbon card cargo carpet carry cart case cash casino castle casual cat catalog catch category cattle caught cause caution cave ceiling celery cement census century cereal certain chair chalk champion change chaos chapter charge chase chat cheap check cheese chef cherry chest chicken chief child chimney choice choose chronic chuckle chunk churn cigar cinnamon circle citizen city civil claim clap clarify claw clay clean clerk clever click client cliff climb clinic clip clock clog close cloth cloud clown club clump cluster clutch coach coast coconut code coffee coil coin collect color column combine come comfort comic common company concert conduct confirm congress connect consider control convince cook cool copper copy coral core corn correct cost cotton couch country couple course cousin cover coyote crack cradle craft cram crane crash crater crawl crazy cream credit creek crew cricket crime crisp critic crop cross crouch crowd crucial cruel cruise crumble crunch crush cry crystal cube culture cup cupboard curious current curtain curve cushion custom cute cycle dad damage damp dance danger daring dash daughter dawn day deal debate debris decade december decide decline decorate decrease deer defense define defy degree delay deliver demand demise denial dentist deny depart depend deposit depth deputy derive describe desert design desk despair destroy detail detect develop device devote diagram dial diamond diary dice diesel diet differ digital dignity dilemma dinner dinosaur direct dirt disagree discover disease dish dismiss disorder display distance divert divide divorce dizzy doctor document dog doll dolphin domain donate donkey donor door dose double dove draft dragon drama drastic draw dream dress drift drill drink drip drive drop drum dry duck dumb dune during dust dutch duty dwarf dynamic eager eagle early earn earth easily east easy echo ecology economy edge edit educate effort egg eight either elbow elder electric elegant element elephant elevator elite else embark embody embrace emerge emotion employ empower empty enable enact end endless endorse enemy energy enforce engage engine enhance enjoy enlist enough enrich enroll ensure enter entire entry envelope episode equal equip era erase erode erosion error erupt escape essay essence estate eternal ethics evidence evil evoke evolve exact example excess exchange excite exclude excuse execute exercise exhaust exhibit exile exist exit exotic expand expect expire explain expose express extend extra eye eyebrow fabric face faculty fade faint faith fall false fame family famous fan fancy fantasy farm fashion fat fatal father fatigue fault favorite feature february federal fee feed feel female fence festival fetch fever few fiber fiction field figure file film filter final find fine finger finish fire firm first fiscal fish fit fitness fix flag flame flash flat flavor flee flight flip float flock floor flower fluid flush fly foam focus fog foil fold follow food foot force forest forget fork fortune forum forward fossil foster found fox fragile frame frequent fresh friend fringe frog front frost frown frozen fruit fuel fun funny furnace fury future gadget gain galaxy gallery game gap garage garbage garden garlic garment gas gasp gate gather gauge gaze general genius genre gentle genuine gesture ghost giant gift giggle ginger giraffe girl give glad glance glare glass glide glimpse globe gloom glory glove glow glue goat goddess gold good goose gorilla gospel gossip govern gown grab grace grain grant grape grass gravity great green grid grief grit grocery group grow grunt guard guess guide guilt guitar gun gym habit hair half hammer hamster hand happy harbor hard harsh harvest hat have hawk hazard head health heart heavy hedgehog height hello helmet help hen hero hidden high hill hint hip hire history hobby hockey hold hole holiday hollow home honey hood hope horn horror horse hospital host hotel hour hover hub huge human humble humor hundred hungry hunt hurdle hurry hurt husband hybrid ice icon idea identify idle ignore ill illegal illness image imitate immense immune impact impose improve impulse inch include income increase index indicate indoor industry infant inflict inform inhale inherit initial inject injury inmate inner innocent input inquiry insane insect inside inspire install intact interest into invest invite involve iron island isolate issue item ivory jacket jaguar jar jazz jealous jeans jelly jewel job join joke journey joy judge juice jump jungle junior junk just kangaroo keen keep ketchup key kick kid kidney kind kingdom kiss kit kitchen kite kitten kiwi knee knife knock know lab label labor ladder lady lake lamp language laptop large later latin laugh laundry lava law lawn lawsuit layer lazy leader leaf learn leave lecture left leg legal legend leisure lemon lend length lens leopard lesson letter level liar liberty library license life lift light like limb limit link lion liquid list little live lizard load loan lobster local lock logic lonely long loop lottery loud lounge love loyal lucky luggage lumber lunar lunch luxury lyrics machine mad magic magnet maid mail main major make mammal man manage mandate mango mansion manual maple marble march margin marine market marriage mask mass master match material math matrix matter maximum maze meadow mean measure meat mechanic medal media melody melt member memory mention menu mercy merge merit merry mesh message metal method middle midnight milk million mimic mind minimum minor minute miracle mirror misery miss mistake mix mixed mixture mobile model modify mom moment monitor monkey monster month moon moral more morning mosquito mother motion motor mountain mouse move movie much muffin mule multiply muscle museum mushroom music must mutual myself mystery myth naive name napkin narrow nasty nation nature near neck need negative neglect neither nephew nerve nest net network neutral never news next nice night noble noise nominee noodle normal north nose notable note nothing notice novel now nuclear number nurse nut oak obey object oblige obscure observe obtain obvious occur ocean october odor off offer office often oil okay old olive olympic omit once one onion online only open opera opinion oppose option orange orbit orchard order ordinary organ orient original orphan ostrich other outdoor outer output outside oval oven over own owner oxygen oyster ozone pact paddle page pair palace palm panda panel panic panther paper parade parent park parrot party pass patch path patient patrol pattern pause pave payment peace peanut pear peasant pelican pen penalty pencil people pepper perfect permit person pet phone photo phrase physical piano picnic picture piece pig pigeon pill pilot pink pioneer pipe pistol pitch pizza place planet plastic plate play please pledge pluck plug plunge poem poet point polar pole police pond pony pool popular portion position possible post potato pottery poverty powder power practice praise predict prefer prepare present pretty prevent price pride primary print priority prison private prize problem process produce profit program project promote proof property prosper protect proud provide public pudding pull pulp pulse pumpkin punch pupil puppy purchase purity purpose purse push put puzzle pyramid quality quantum quarter question quick quit quiz quote rabbit raccoon race rack radar radio rail rain raise rally ramp ranch random range rapid rare rate rather raven raw razor ready real reason rebel rebuild recall receive recipe record recycle reduce reflect reform refuse region regret regular reject relax release relief rely remain remember remind remove render renew rent reopen repair repeat replace report require rescue resemble resist resource response result retire retreat return reunion reveal review reward rhythm rib ribbon rice rich ride ridge rifle right rigid ring riot ripple risk ritual rival river road roast robot robust rocket romance roof rookie room rose rotate rough round route royal rubber rude rug rule run runway rural sad saddle sadness safe sail salad salmon salon salt salute same sample sand satisfy satoshi sauce sausage save say scale scan scare scatter scene scheme school science scissors scorpion scout scrap screen script scrub sea search season seat second secret section security seed seek segment select sell seminar senior sense sentence series service session settle setup seven shadow shaft shallow share shed shell sheriff shield shift shine ship shiver shock shoe shoot shop short shoulder shove shrimp shrug shuffle shy sibling sick side siege sight sign silent silk silly silver similar simple since sing siren sister situate six size skate sketch ski skill skin skirt skull slab slam sleep slender slice slide slight slim slogan slot slow slush small smart smile smoke smooth snack snake snap sniff snow soap soccer social sock soda soft solar soldier solid solution solve someone song soon sorry sort soul sound soup source south space spare spatial spawn speak special speed spell spend sphere spice spider spike spin spirit split spoil sponsor spoon sport spot spray spread spring spy square squeeze squirrel stable stadium staff stage stairs stamp stand start state stay steak steel stem step stereo stick still sting stock stomach stone stool story stove strategy street strike strong struggle student stuff stumble style subject submit subway success such sudden suffer sugar suggest suit summer sun sunny sunset super supply supreme sure surface surge surprise surround survey suspect sustain swallow swamp swap swarm swear sweet swift swim swing switch sword symbol symptom syrup system table tackle tag tail talent talk tank tape target task taste tattoo taxi teach team tell ten tenant tennis tent term test text thank that theme then theory there they thing this thought three thrive throw thumb thunder ticket tide tiger tilt timber time tiny tip tired tissue title toast tobacco today toddler toe together toilet token tomato tomorrow tone tongue tonight tool tooth top topic topple torch tornado tortoise toss total tourist toward tower town toy track trade traffic tragic train transfer trap trash travel tray treat tree trend trial tribe trick trigger trim trip trophy trouble truck true truly trumpet trust truth try tube tuition tumble tuna tunnel turkey turn turtle twelve twenty twice twin twist two type typical ugly umbrella unable unaware uncle uncover under undo unfair unfold unhappy uniform unique unit universe unknown unlock until unusual unveil update upgrade uphold upon upper upset urban urge usage use used useful useless usual utility vacant vacuum vague valid valley valve van vanish vapor various vast vault vehicle velvet vendor venture venue verb verify version very vessel veteran viable vibrant vicious victory video view village vintage violin virtual virus visa visit visual vital vivid vocal voice void volcano volume vote voyage wage wagon wait walk wall walnut want warfare warm warrior wash wasp waste water wave way wealth weapon wear weasel weather web wedding weekend weird welcome west wet whale what wheat wheel when where whip whisper wide width wife wild will win window wine wing wink winner winter wire wisdom wise wish witness wolf woman wonder wood wool word work world worry worth wrap wreck wrestle wrist write wrong yard year yellow you young youth zebra zero zone zoo".split(" ")
    assert len(self.dict) == 2048, "Dictionary is corrupted"

  def encode(self, entropy):
    assert len(entropy) == 32, "Insufficient entropy provided"
    checksum = sha256(entropy).digest()[:1]
    to_encode = entropy + checksum
    number_to_encode = int(binascii.hexlify(to_encode), 16)
    word_string = ""
    for i in range(24):
      index = number_to_encode & 2047
      word_string = self.dict[index] + " " + word_string
      number_to_encode /= 2048
    return word_string.strip()

  def decode(self, input):
    data = ""
    tokens = input.split(" ")
    assert len(tokens) == 24, "Wrong number of words provided"
    number = 0
    for i in range(24):
      number += self.dict.index(tokens[i]) * pow(2048, 23-i)
    hex_number = int_to_hex(number, 264)
    encoded = binascii.unhexlify(hex_number)
    entropy = encoded[:-1]
    checksum = encoded[-1:]
    assert sha256(entropy).digest()[:1] == checksum, "Invalid phrase, checksum mismatch"
    return entropy
    
  def generate_seed(self, phrase, passphrase=""):
    return hashlib.pbkdf2_hmac('sha512', phrase, "mnemonic" + passphrase, 2048)

################################################################################################
# Bitcoin Functions
################################################################################################

class bitcoin_wallet:

  def __init__(self, private_key_int=None, private_key_wif=None):
    if (not private_key_int is None):
      self.private_key = int(private_key_int)
    elif (private_key_wif is not None):
      self.private_key = self.decode_wif(private_key_wif)
    else:
      raise Exception("No private key passed in constructor")
    self.public_key = None

  # Returns the private key as an integer
  def get_private_key_as_int(self):
    return self.private_key

  # Encodes private key as Hex
  def get_private_key_as_hex(self):
    return int_to_hex(self.private_key, 256)
    
  # Encodes private key as Binary
  def get_private_key_as_bin(self):
    return binascii.unhexlify(self.get_private_key_as_hex())

  # Encodes private key using Wallet Input Format
  def get_wif(self, compressed=False):
    private_key_hex = self.get_private_key_as_hex()
    if compressed:
      appended = binascii.unhexlify("80" + private_key_hex + "01")
    else:
      appended = binascii.unhexlify("80" + private_key_hex)
    checksum = sha256(sha256(appended).digest()).digest()[:4]
    combined = appended + checksum
    hex_combined = binascii.hexlify(combined)
    return base58().encode(hex_combined)
    
  def decode_wif(self, wif, compressed=False):
    hex_wif = base58().decode(wif)
    bin_wif = binascii.unhexlify(hex_wif)
    expected = bin_wif[-4:]
    checked_message = bin_wif[:-4]
    computed = sha256(sha256(checked_message).digest()).digest()[:4]
    assert expected == computed, "Invalid WIF, checksum mismatch"
    binary_private_key = checked_message[1:]
    if compressed:
      binary_private_key[:-1]
    hex_private_key = binascii.hexlify(binary_private_key)
    return int(hex_private_key, 16)

  def get_public_key_as_point(self):
    if self.public_key is None:
      self.public_key = point_mul(self.private_key)
    return self.public_key
    
  def get_address_as_hex(self, compressed=False):
    public_key = self.get_public_key_as_point()
    if compressed:
      hash_of_public = sha256(ser_p(public_key))
    else:
      hash_of_public = sha256(public_key.as_bin())
    ripemd = hashlib.new('ripemd160')
    ripemd.update(hash_of_public.digest())
    versioned_hash = '00' + ripemd.hexdigest()
    prechecksum = sha256(binascii.unhexlify(versioned_hash)).digest()
    checksum = sha256(prechecksum).hexdigest()[:8]
    return versioned_hash + checksum
 
  def get_address_as_b58(self, compressed=False):
    return '1' + base58().encode(self.get_address_as_hex(compressed))
    
def validate_wallet_input_format(wif):
  hex_wif = base58().decode(wif)
  bin_wif = binascii.unhexlify(hex_wif)
  expected = bin_wif[-4:]
  computed = sha256(sha256(bin_wif[:-4]).digest()).digest()[:4]
  return expected == computed

def validate_address(address):
  hex_address = base58().decode(address).zfill(50)
  bin_address = binascii.unhexlify(hex_address)
  expected = bin_address[-4:]
  computed = sha256(sha256(bin_address[:-4]).digest()).digest()[:4]
  return expected == computed

def point_mul(p):
  return secp256k1.multiply_point(secp256k1.g, p)

def ser_32(i):
  return struct.pack('>I', i)
    
def ser_256(p):
  return binascii.unhexlify(int_to_hex(p, 256))
    
def ser_p(point):
  parity = point.y % 2
  first_octet = chr(2 + parity)
  return first_octet + ser_256(point.x)

class child_key_derivation:
  def __init__(self, chain_code_hex, public_key, private_key=None, path=None, parent=None):
    if path is None:
      path = []
    self.chain_code_hex = chain_code_hex
    self.chain_code = binascii.unhexlify(chain_code_hex)
    self.public_key = public_key
    self.private_key = private_key
    self.path = path
    self.parent = parent

  def has_private(self):
    return not self.private_key is None

  def get_private_key(self):
    return self.private_key
    
  def get_public_key(self):
    return self.public_key
    
  def get_chain_code(self):
    return self.chain_code_hex
    
  def get_path(self):
    return self.path
    
  def parse(self, n_bytes):
    return int(binascii.hexlify(n_bytes), 16)

  def derive_subkey(self, i, hardened=False):
      
    if (hardened):
      i += pow(2, 31)
    
    if i >= pow(2, 31):
      # Create hardened child key
      if self.private_key == None:
        raise Exception("Need private key")
      message = chr(0) + ser_256(self.private_key) + ser_32(i)
    else:
      # Create child key
      message = ser_p(self.public_key) + ser_32(i)

    hmac_digest = hmac.new(self.chain_code, message, sha512).hexdigest()
    
    # Create child instance
    if not self.private_key == None:
      child_private_key = (int(hmac_digest[:64], 16) + self.private_key) % secp256k1.r
      child_public_key = point_mul(child_private_key)
    else:
      child_private_key = None
      child_key = int(hmac_digest[:64], 16) % secp256k1.r
      point = point_mul(child_key)
      child_public_key = secp256k1.add_points(self.public_key, point)
      
    child_child_code_hex = hmac_digest[64:]
    child_path = self.path[:]
    child_path.append(i)
    
    return child_key_derivation(child_child_code_hex, child_public_key, child_private_key, child_path, self)
    
  def compute_checksum(self, hex_encoding):
    binary_encoding = binascii.unhexlify(hex_encoding)
    prechecksum = sha256(binary_encoding).digest()
    checksum = sha256(prechecksum).hexdigest()[:8]
    return checksum
    
  def compute_fingerprint(self):
    binary_encoding = ser_p(self.public_key)
    prechecksum = sha256(binary_encoding).digest()
    ripemd = hashlib.new('ripemd160')
    ripemd.update(prechecksum)
    fingerprint = ripemd.hexdigest()[:8]
    return fingerprint
    
  def serialize_private(self):
    result = "0488ADE4" # xprv magic
    depth = len(self.path)
    result += int_to_hex(depth, 8)
    if depth == 0:
      result += "00000000" # Parent fingerprint
      result += "00000000" # i value
    else:
      result += self.parent.compute_fingerprint()
      result += binascii.hexlify(ser_32(self.path[-1])) # i value
    result += self.chain_code_hex
    result += "00" + binascii.hexlify(ser_256(self.private_key))
    return base58().encode(result + self.compute_checksum(result))

  def serialize_public(self):
    result = "0488B21E" # xpub magic
    depth = len(self.path)
    result += int_to_hex(depth, 8)
    if depth == 0:
      result += "00000000" # Parent fingerprint
      result += "00000000" # i value
    else:
      result += self.parent.compute_fingerprint()
      result += binascii.hexlify(ser_32(self.path[-1])) # i value
    result += self.chain_code_hex
    result += binascii.hexlify(ser_p(self.public_key))
    return base58().encode(result + self.compute_checksum(result))
  
# Parses a Hierarchical Path, e.g., "m/44'/0'/0'/0"  
def parse_path(seed, path):
  seed_hmac = hmac.new("Bitcoin seed", seed, sha512).hexdigest()
  secret_key = seed_hmac[:64]
  chain_code_hex = seed_hmac[64:]
  private_key = int(secret_key, 16)
  if (private_key > secp256k1.r):
    raise Exception("Private key is too large!!!")
  wallet = bitcoin_wallet(private_key_int=private_key)

  levels = path.split("/")
  assert levels[0].lower() == 'm', "Invalid address, path must start with 'm'"
  node = child_key_derivation(chain_code_hex, wallet.get_public_key_as_point(), private_key) 
  
  for i in range(1, len(levels)):
    index = levels[i]
    hardened = False
    if index[-1:] == "'":
      hardened = True
      index = index[:-1]
    int_index = int(index)
    node = node.derive_subkey(int_index, hardened)
  return node

def run_tests():
  import test_vectors
  test_vectors.bip32_tests().execute_all_tests()
  test_vectors.bip39_tests().execute_all_tests()
  test_vectors.bip44_tests().execute_all_tests()
  print "All tests completed successfully"
  
################################################################################################
# CLI Functions
################################################################################################

def print_usage_and_exit():
  print "USAGE: python btc.py test"
  print "USAGE: python btc.py generate [additional entropy] [passphrase]"
  print "USAGE: python btc.py recover \"mnemonic phrase\" [passphrase]"
  exit(1)

################################################################################################
# Generate random seed
################################################################################################

def main():

  # Parse command line options
  if len(argv) < 2:
    print_usage_and_exit()
    exit(1)

  supplied_entropy = ""
  passphrase = ""

  if len(argv) >= 2:

    word_encoder = mnemonic()

    if (argv[1].lower() == "test"):
      run_tests()
      exit(0)
	
    if (argv[1].lower() == "generate"):
      if len(argv) >= 3:
        supplied_entropy = argv[2]
      if len(argv) >= 4:
        passphrase = argv[3]
	  
      print "Generating new private key..."
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
        print "USAGE: python btc.py recover \"mnemonic phrase\" [passphrase]"
        exit(1)
      if len(argv) >= 4:
        passphrase = argv[3]
        
      print "Restoring existing private key..."
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

  wallet = bitcoin_wallet(private_key_int=private_key)

  print "Private Key as Int:   ", wallet.get_private_key_as_int()

  private_key_hex = wallet.get_private_key_as_hex()
  print "Private Key as Hex:   ", private_key_hex

  print

  ################################################################################################
  # Export and Import WIF
  ################################################################################################

  wif = wallet.get_wif()
  print "Private Key as WIF:   ", wif

  valid = validate_wallet_input_format(wif)
  print "WIF is valid:         ", valid 
  assert valid == True, "WIF is invalid"

  imported_wallet = bitcoin_wallet(private_key_wif=wif)
  assert wallet.get_private_key_as_int() == imported_wallet.get_private_key_as_int()
  assert wallet.get_address_as_b58() == imported_wallet.get_address_as_b58()
  assert validate_address(imported_wallet.get_address_as_b58())
  assert wallet.get_address_as_b58(True) == imported_wallet.get_address_as_b58(True)
  assert validate_address(imported_wallet.get_address_as_b58(True))

  # Create Wallet form WIF
  print

  ################################################################################################
  # Compute Public Key
  ################################################################################################

  # Derive Public Key from Private Key
  public_key = wallet.get_public_key_as_point()
  print "Public Key Point:     ", public_key
  print "Public Key as Hex:    ", public_key.as_hex()

  print

  ################################################################################################
  # Compute Address
  ################################################################################################

  # Form bitcoin address
  hex_address = wallet.get_address_as_hex()
  print "Hex address:          ", hex_address

  # Convert to base 58
  address = wallet.get_address_as_b58()
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
  ckd = child_key_derivation(chain_code_hex, public_key, private_key)
  print "BIP 32 Root Private:  ", ckd.serialize_private()
  print "BIP 32 Root Public:   ", ckd.serialize_public()

  print

  # Derive child key using private key
  child1 = ckd.derive_subkey(0)

  # Derive child key from public key only
  ckd2 = child_key_derivation(chain_code_hex, public_key)
  child2 = ckd2.derive_subkey(0)
  assert child1.get_public_key() == child2.get_public_key()
  assert child1.get_chain_code() == child2.get_chain_code()

  path = "m/44'/0'/0'"
  account_extended_key = parse_path(seed, path)
  print "Acct Ext Private Key: ", account_extended_key.serialize_private()
  print "Acct Ext Public Key:  ", account_extended_key.serialize_public()
  print "Acct Ext 44 Path:     ", account_extended_key.get_path()

  print

  path = "m/44'/0'/0'/0"
  bip_44_key = account_extended_key.derive_subkey(0)
  bip_44_key_2 = parse_path(seed, path)
  print "BIP 44 Private Key:   ", bip_44_key.serialize_private()
  print "BIP 44 Public Key:    ", bip_44_key.serialize_public()
  print "BIP 44 Path:          ", bip_44_key.get_path()

  assert bip_44_key.serialize_private() == bip_44_key_2.serialize_private()
  assert bip_44_key.serialize_public() == bip_44_key_2.serialize_public()
  assert bip_44_key.get_path() == bip_44_key_2.get_path()

  print

  path = "m/44'/0'/0'/0/0"
  address_0 = bip_44_key.derive_subkey(0)
  address_0_2 = parse_path(seed, path)
  print "Private Key 0:        ", bitcoin_wallet(address_0.get_private_key()).get_wif(True)
  print "Public Key 0:         ", binascii.hexlify(ser_p(address_0.get_public_key()))
  print "Address 0:            ", bitcoin_wallet(address_0.get_private_key()).get_address_as_b58(True)

  assert validate_address(bitcoin_wallet(address_0.get_private_key()).get_address_as_b58(True))
  assert validate_address(bitcoin_wallet(address_0.get_private_key()).get_address_as_b58(False))

  assert bitcoin_wallet(address_0.get_private_key()).get_wif(True) == bitcoin_wallet(address_0_2.get_private_key()).get_wif(True)
  assert binascii.hexlify(ser_p(address_0.get_public_key())) == binascii.hexlify(ser_p(address_0_2.get_public_key()))
  assert bitcoin_wallet(address_0.get_private_key()).get_address_as_b58(True) == bitcoin_wallet(address_0_2.get_private_key()).get_address_as_b58(True)

  print

  path = "m/44'/0'/0'/0/1"
  address_1 = bip_44_key.derive_subkey(1)
  address_1_2 = parse_path(seed, path)
  print "Private Key 1:        ", bitcoin_wallet(address_1.get_private_key()).get_wif(True)
  print "Public Key 1:         ", binascii.hexlify(ser_p(address_1.get_public_key()))
  print "Address 1:            ", bitcoin_wallet(address_1.get_private_key()).get_address_as_b58(True)

  assert validate_address(bitcoin_wallet(address_1.get_private_key()).get_address_as_b58(True))
  assert validate_address(bitcoin_wallet(address_1.get_private_key()).get_address_as_b58(False))

  assert bitcoin_wallet(address_1.get_private_key()).get_wif(True) == bitcoin_wallet(address_1_2.get_private_key()).get_wif(True)
  assert binascii.hexlify(ser_p(address_1.get_public_key())) == binascii.hexlify(ser_p(address_1_2.get_public_key()))
  assert bitcoin_wallet(address_1.get_private_key()).get_address_as_b58(True) == bitcoin_wallet(address_1_2.get_private_key()).get_address_as_b58(True)

  print

if __name__ =='__main__':
  main()