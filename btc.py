#!/usr/bin/python

# Implements: https://www.ledgerwallet.com/support/bip39-standalone.html (wallet generation)
# 
# Enables secure, offline key generation, according to BIP 32, BIP 44, and BIP 39.
#
# It outputs the seed as a 24-word (264-bit) mnemonic which can be written on paper or in 
# a fire proof cryptosteel.com device.  The mnemonic phrase may be imported into Wallet Apps 
# such as Electrum, Mycelium, and Coinomi
#
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
# Usage:
#
# Generate new private key:
#
# $ pthon btc.py test
#
# This runs a suite of tests to ensure correct operation using published test vectors. This 
# should be run at least once on the machine on which you intend to generate keys.
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

def egcd(a, b):
  if a == 0:
    return (b, 0, 1)
  g, y, x = egcd(b % a,a)
  return (g, x - (b // a) * y, y)

def modinv(a, m):
  g, x, y = egcd(a, m)
  if g != 1:
    raise Exception('No modular inverse')
  return x % m

class curve:
  def __init__(self, a, b, p, r, g):
    self.a = a
    self.b = b
    self.p = p
    self.r = r
    self.g = g

  def mod_inv(self, x):
    if (x < 0):
      x += self.p
    return modinv(x, self.p)

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
    assert len(self.dict) == 2048

  def encode(self, entropy):
    assert len(entropy) == 32
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
    assert len(tokens) == 24
    number = 0
    for i in range(24):
      number += self.dict.index(tokens[i]) * pow(2048, 23-i)
    hex_number = int_to_hex(number, 264)
    encoded = binascii.unhexlify(hex_number)
    entropy = encoded[:-1]
    checksum = encoded[-1:]
    assert sha256(entropy).digest()[:1] == checksum
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
    assert expected == computed
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
  assert levels[0].lower() == 'm'
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
  
################################################################################################
# Test Functions
################################################################################################

class bip32_tests:

  def __init__(self):
    pass
    
  def execute_all_tests(self):
    print "Running BIP 32 Tests:"
    print "Running test_vector_1 tests:"
    self.test_vector_1()
    print "Running test_vector_2 tests:"
    self.test_vector_2()
    print "Running test_vector_3 tests:"
    self.test_vector_3()
    
  def test_vector_1(self):
    seed = binascii.unhexlify("000102030405060708090a0b0c0d0e0f")
    
    print "Testing chain m...",
    wallet = parse_path(seed, "m")
    assert wallet.serialize_public() == "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8"
    assert wallet.serialize_private() == "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"
    print "passed"
    
    print "Testing chain m/0'...",
    wallet = parse_path(seed, "m/0'")
    assert wallet.serialize_public() == "xpub68Gmy5EdvgibQVfPdqkBBCHxA5htiqg55crXYuXoQRKfDBFA1WEjWgP6LHhwBZeNK1VTsfTFUHCdrfp1bgwQ9xv5ski8PX9rL2dZXvgGDnw"
    assert wallet.serialize_private() == "xprv9uHRZZhk6KAJC1avXpDAp4MDc3sQKNxDiPvvkX8Br5ngLNv1TxvUxt4cV1rGL5hj6KCesnDYUhd7oWgT11eZG7XnxHrnYeSvkzY7d2bhkJ7"
    print "passed"
    
    print "Testing chain m/0'/1...",
    wallet = parse_path(seed, "m/0'/1")
    assert wallet.serialize_public() == "xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ"
    assert wallet.serialize_private() == "xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs"
    print "passed"
    
    print "Testing chain m/0'/1/2'...",
    wallet = parse_path(seed, "m/0'/1/2'")
    assert wallet.serialize_public() == "xpub6D4BDPcP2GT577Vvch3R8wDkScZWzQzMMUm3PWbmWvVJrZwQY4VUNgqFJPMM3No2dFDFGTsxxpG5uJh7n7epu4trkrX7x7DogT5Uv6fcLW5"
    assert wallet.serialize_private() == "xprv9z4pot5VBttmtdRTWfWQmoH1taj2axGVzFqSb8C9xaxKymcFzXBDptWmT7FwuEzG3ryjH4ktypQSAewRiNMjANTtpgP4mLTj34bhnZX7UiM"
    print "passed"
    
    print "Testing chain m/0'/1/2'/2...",
    wallet = parse_path(seed, "m/0'/1/2'/2")
    assert wallet.serialize_public() == "xpub6FHa3pjLCk84BayeJxFW2SP4XRrFd1JYnxeLeU8EqN3vDfZmbqBqaGJAyiLjTAwm6ZLRQUMv1ZACTj37sR62cfN7fe5JnJ7dh8zL4fiyLHV"
    assert wallet.serialize_private() == "xprvA2JDeKCSNNZky6uBCviVfJSKyQ1mDYahRjijr5idH2WwLsEd4Hsb2Tyh8RfQMuPh7f7RtyzTtdrbdqqsunu5Mm3wDvUAKRHSC34sJ7in334"
    print "passed"
    
    print "Testing chain m/0'/1/2'/2/1000000000...",
    wallet = parse_path(seed, "m/0'/1/2'/2/1000000000")
    assert wallet.serialize_public() == "xpub6H1LXWLaKsWFhvm6RVpEL9P4KfRZSW7abD2ttkWP3SSQvnyA8FSVqNTEcYFgJS2UaFcxupHiYkro49S8yGasTvXEYBVPamhGW6cFJodrTHy"
    assert wallet.serialize_private() == "xprvA41z7zogVVwxVSgdKUHDy1SKmdb533PjDz7J6N6mV6uS3ze1ai8FHa8kmHScGpWmj4WggLyQjgPie1rFSruoUihUZREPSL39UNdE3BBDu76"
    print "passed"


  def test_vector_2(self):
    seed = binascii.unhexlify("fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542")
    
    print "Testing chain m...",
    wallet = parse_path(seed, "m")
    assert wallet.serialize_public() == "xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCGu8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJY47LJhkJ8UB7WEGuduB"
    assert wallet.serialize_private() == "xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U"
    print "passed"
    
    print "Testing chain m/0...",
    wallet = parse_path(seed, "m/0")
    assert wallet.serialize_public() == "xpub69H7F5d8KSRgmmdJg2KhpAK8SR3DjMwAdkxj3ZuxV27CprR9LgpeyGmXUbC6wb7ERfvrnKZjXoUmmDznezpbZb7ap6r1D3tgFxHmwMkQTPH"
    assert wallet.serialize_private() == "xprv9vHkqa6EV4sPZHYqZznhT2NPtPCjKuDKGY38FBWLvgaDx45zo9WQRUT3dKYnjwih2yJD9mkrocEZXo1ex8G81dwSM1fwqWpWkeS3v86pgKt"
    print "passed"
    
    print "Testing chain m/0/2147483647'...",
    wallet = parse_path(seed, "m/0/2147483647'")
    assert wallet.serialize_public() == "xpub6ASAVgeehLbnwdqV6UKMHVzgqAG8Gr6riv3Fxxpj8ksbH9ebxaEyBLZ85ySDhKiLDBrQSARLq1uNRts8RuJiHjaDMBU4Zn9h8LZNnBC5y4a"
    assert wallet.serialize_private() == "xprv9wSp6B7kry3Vj9m1zSnLvN3xH8RdsPP1Mh7fAaR7aRLcQMKTR2vidYEeEg2mUCTAwCd6vnxVrcjfy2kRgVsFawNzmjuHc2YmYRmagcEPdU9"
    print "passed"
    
    print "Testing chain m/0/2147483647'/1...",
    wallet = parse_path(seed, "m/0/2147483647'/1")
    assert wallet.serialize_public() == "xpub6DF8uhdarytz3FWdA8TvFSvvAh8dP3283MY7p2V4SeE2wyWmG5mg5EwVvmdMVCQcoNJxGoWaU9DCWh89LojfZ537wTfunKau47EL2dhHKon"
    assert wallet.serialize_private() == "xprv9zFnWC6h2cLgpmSA46vutJzBcfJ8yaJGg8cX1e5StJh45BBciYTRXSd25UEPVuesF9yog62tGAQtHjXajPPdbRCHuWS6T8XA2ECKADdw4Ef"
    print "passed"
    
    print "Testing chain m/0/2147483647'/1/2147483646'...",
    wallet = parse_path(seed, "m/0/2147483647'/1/2147483646'")
    assert wallet.serialize_public() == "xpub6ERApfZwUNrhLCkDtcHTcxd75RbzS1ed54G1LkBUHQVHQKqhMkhgbmJbZRkrgZw4koxb5JaHWkY4ALHY2grBGRjaDMzQLcgJvLJuZZvRcEL"
    assert wallet.serialize_private() == "xprvA1RpRA33e1JQ7ifknakTFpgNXPmW2YvmhqLQYMmrj4xJXXWYpDPS3xz7iAxn8L39njGVyuoseXzU6rcxFLJ8HFsTjSyQbLYnMpCqE2VbFWc"
    print "passed"
    
    print "Testing chain m/0/2147483647'/1/2147483646'/2...",
    wallet = parse_path(seed, "m/0/2147483647'/1/2147483646'/2")
    assert wallet.serialize_public() == "xpub6FnCn6nSzZAw5Tw7cgR9bi15UV96gLZhjDstkXXxvCLsUXBGXPdSnLFbdpq8p9HmGsApME5hQTZ3emM2rnY5agb9rXpVGyy3bdW6EEgAtqt"
    assert wallet.serialize_private() == "xprvA2nrNbFZABcdryreWet9Ea4LvTJcGsqrMzxHx98MMrotbir7yrKCEXw7nadnHM8Dq38EGfSh6dqA9QWTyefMLEcBYJUuekgW4BYPJcr9E7j"
    print "passed"

  def test_vector_3(self):
    seed = binascii.unhexlify("4b381541583be4423346c643850da4b320e46a87ae3d2a4e6da11eba819cd4acba45d239319ac14f863b8d5ab5a0d0c64d2e8a1e7d1457df2e5a3c51c73235be")
    
    print "Testing chain m...",
    wallet = parse_path(seed, "m")
    assert wallet.serialize_public() == "xpub661MyMwAqRbcEZVB4dScxMAdx6d4nFc9nvyvH3v4gJL378CSRZiYmhRoP7mBy6gSPSCYk6SzXPTf3ND1cZAceL7SfJ1Z3GC8vBgp2epUt13"
    assert wallet.serialize_private() == "xprv9s21ZrQH143K25QhxbucbDDuQ4naNntJRi4KUfWT7xo4EKsHt2QJDu7KXp1A3u7Bi1j8ph3EGsZ9Xvz9dGuVrtHHs7pXeTzjuxBrCmmhgC6"
    print "passed"
    
    print "Testing chain m/0'...",
    wallet = parse_path(seed, "m/0'")
    assert wallet.serialize_public() == "xpub68NZiKmJWnxxS6aaHmn81bvJeTESw724CRDs6HbuccFQN9Ku14VQrADWgqbhhTHBaohPX4CjNLf9fq9MYo6oDaPPLPxSb7gwQN3ih19Zm4Y"
    assert wallet.serialize_private() == "xprv9uPDJpEQgRQfDcW7BkF7eTya6RPxXeJCqCJGHuCJ4GiRVLzkTXBAJMu2qaMWPrS7AANYqdq6vcBcBUdJCVVFceUvJFjaPdGZ2y9WACViL4L"
    print "passed"

class bip39_tests:

  def __init__(self):
    pass
    
  def execute_all_tests(self):
    print "Running BIP 39 Tests:"
    encoder = mnemonic()
    passphrase = "TREZOR"
        
    entropy = "0000000000000000000000000000000000000000000000000000000000000000"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "bda85446c68413707090a52022edd26a1c9462295029f2e60cd7c4f2bbd3097170af7a4d73245cafa9c3cca8d561a7c3de6f5d4a10be8ed2a5e608d68f92fcc8"
    wallet = parse_path(binascii.unhexlify(seed), 'm')
    assert wallet.serialize_private() == "xprv9s21ZrQH143K32qBagUJAMU2LsHg3ka7jqMcV98Y7gVeVyNStwYS3U7yVVoDZ4btbRNf4h6ibWpY22iRmXq35qgLs79f312g2kj5539ebPM"
    print "passed"
    
    entropy = "7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth title"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "bc09fca1804f7e69da93c2f2028eb238c227f2e9dda30cd63699232578480a4021b146ad717fbb7e451ce9eb835f43620bf5c514db0f8add49f5d121449d3e87"
    wallet = parse_path(binascii.unhexlify(seed), 'm')
    assert wallet.serialize_private() == "xprv9s21ZrQH143K3Y1sd2XVu9wtqxJRvybCfAetjUrMMco6r3v9qZTBeXiBZkS8JxWbcGJZyio8TrZtm6pkbzG8SYt1sxwNLh3Wx7to5pgiVFU"
    print "passed"
    
    entropy = "8080808080808080808080808080808080808080808080808080808080808080"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic bless"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "c0c519bd0e91a2ed54357d9d1ebef6f5af218a153624cf4f2da911a0ed8f7a09e2ef61af0aca007096df430022f7a2b6fb91661a9589097069720d015e4e982f"
    wallet = parse_path(binascii.unhexlify(seed), 'm')
    assert wallet.serialize_private() == "xprv9s21ZrQH143K3CSnQNYC3MqAAqHwxeTLhDbhF43A4ss4ciWNmCY9zQGvAKUSqVUf2vPHBTSE1rB2pg4avopqSiLVzXEU8KziNnVPauTqLRo"
    print "passed"
    
    entropy = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo vote"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "dd48c104698c30cfe2b6142103248622fb7bb0ff692eebb00089b32d22484e1613912f0a5b694407be899ffd31ed3992c456cdf60f5d4564b8ba3f05a69890ad"
    wallet = parse_path(binascii.unhexlify(seed), 'm')
    assert wallet.serialize_private() == "xprv9s21ZrQH143K2WFF16X85T2QCpndrGwx6GueB72Zf3AHwHJaknRXNF37ZmDrtHrrLSHvbuRejXcnYxoZKvRquTPyp2JiNG3XcjQyzSEgqCB"
    print "passed"
    
    entropy = "68a79eaca2324873eacc50cb9c6eca8cc68ea5d936f98787c60c7ebc74e6ce7c"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "64c87cde7e12ecf6704ab95bb1408bef047c22db4cc7491c4271d170a1b213d20b385bc1588d9c7b38f1b39d415665b8a9030c9ec653d75e65f847d8fc1fc440"
    wallet = parse_path(binascii.unhexlify(seed), 'm')
    assert wallet.serialize_private() == "xprv9s21ZrQH143K2XTAhys3pMNcGn261Fi5Ta2Pw8PwaVPhg3D8DWkzWQwjTJfskj8ofb81i9NP2cUNKxwjueJHHMQAnxtivTA75uUFqPFeWzk"
    print "passed"
    
    entropy = "9f6a2878b2520799a44ef18bc7df394e7061a224d2c33cd015b157d746869863"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "panda eyebrow bullet gorilla call smoke muffin taste mesh discover soft ostrich alcohol speed nation flash devote level hobby quick inner drive ghost inside"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "72be8e052fc4919d2adf28d5306b5474b0069df35b02303de8c1729c9538dbb6fc2d731d5f832193cd9fb6aeecbc469594a70e3dd50811b5067f3b88b28c3e8d"
    wallet = parse_path(binascii.unhexlify(seed), 'm')
    assert wallet.serialize_private() == "xprv9s21ZrQH143K2WNnKmssvZYM96VAr47iHUQUTUyUXH3sAGNjhJANddnhw3i3y3pBbRAVk5M5qUGFr4rHbEWwXgX4qrvrceifCYQJbbFDems"
    print "passed"

    entropy = "066dca1a2bb7e8a1db2832148ce9933eea0f3ac9548d793112d9a95c9407efad"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "all hour make first leader extend hole alien behind guard gospel lava path output census museum junior mass reopen famous sing advance salt reform"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "26e975ec644423f4a4c4f4215ef09b4bd7ef924e85d1d17c4cf3f136c2863cf6df0a475045652c57eb5fb41513ca2a2d67722b77e954b4b3fc11f7590449191d"
    wallet = parse_path(binascii.unhexlify(seed), 'm')
    assert wallet.serialize_private() == "xprv9s21ZrQH143K3rEfqSM4QZRVmiMuSWY9wugscmaCjYja3SbUD3KPEB1a7QXJoajyR2T1SiXU7rFVRXMV9XdYVSZe7JoUXdP4SRHTxsT1nzm"
    print "passed"

    entropy = "f585c11aec520db57dd353c69554b21a89b20fb0650966fa0a9d6f74fd989d8f"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "void come effort suffer camp survey warrior heavy shoot primary clutch crush open amazing screen patrol group space point ten exist slush involve unfold"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "01f5bced59dec48e362f2c45b5de68b9fd6c92c6634f44d6d40aab69056506f0e35524a518034ddc1192e1dacd32c1ed3eaa3c3b131c88ed8e7e54c49a5d0998"
    wallet = parse_path(binascii.unhexlify(seed), 'm')
    assert wallet.serialize_private() == "xprv9s21ZrQH143K39rnQJknpH1WEPFJrzmAqqasiDcVrNuk926oizzJDDQkdiTvNPr2FYDYzWgiMiC63YmfPAa2oPyNB23r2g7d1yiK6WpqaQS"
    print "passed"

class bip44_tests:

  def __init__(self):
    pass

  def execute_all_tests(self):
    print "Running BIP 44 Tests:"
    print "Running test_vector_1 tests:"
    self.test_vector_1()
    print "Running test_vector_2 tests:"
    self.test_vector_2()
    print "Running test_vector_3 tests:"
    self.test_vector_3()
    
  def test_vector_1(self):
    encoder = mnemonic()
    
    phrase = "cover tube shrug thought trick scout extra orphan spin banana civil error hockey ranch vivid round logic stable brass error fork duck bomb soup"
    passphrase = ""
    print "Testing phrase: " + phrase + "...",
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "a12e010b3cfad9dff772d098d101558171ecda084cd93417f9ecce999bfdeab251b9fa6427fb095bcd2dc07a8507b4bb0585574eb029bddeeeae70cb1bb1c741"
    
    # BIP 32 Root Key
    wallet = parse_path(binascii.unhexlify(seed), 'm')
    assert wallet.serialize_private() == "xprv9s21ZrQH143K36J6xmaUWkrDFTgCAo8v3T5vgbcT7HQH55XD3XMF88CmYJDeXsbRcFw14kP5vDBCjDdX5JyRLM5LgbiQbfZXXo5G6nnPbM9"
    
    # Account Extended Keys
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'")
    assert wallet.serialize_private() == "xprv9yGa4qdGEike4bgpvnSca1rLvDh8uXiKrZoxaiK1UAts1Ljz4ZmYwGeZeDVGpiMwM3TtSSvUd7ZdrwKWMwuBPD78U2jMMmiWs5Jp61o46aa"
    assert wallet.serialize_public() == "xpub6CFvUMAA56JwH5mJ2oycw9o5UFXdJzSBDnjZP6id2WRqt958c75oV4y3VWN6Ro1dewtP9cdEV5VDUvWBJpENWxBAoQv6d88m3bhZfjmEQ33"
   
    # BIP 32 Extended Keys
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'/0")
    assert wallet.serialize_private() == "xprv9zxbcTUDnJNjgh2ijkGP2iyQfsauooNT3msQdrJXjCuSLKXkPdGo3crfLQKByxRT5H5zG8tZVX5HbXNMRqvaxqLBGtHWD4pEWXiWmbVvMH1"
    assert wallet.serialize_public() == "xpub6Dwx1y17cfw2uB7BqmoPPrv9DuRQDG6JQzo1SEi9HYSRD7rtwAb3bRB9BffNUHBVEQWmRgea42PNuvAEWqNj8bsgc2wT9jpWNeFdA3rRmPU"
   
    # Address 0
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'/0/0")
    assert bitcoin_wallet(wallet.get_private_key()).get_address_as_b58(True) == "1Gx1DxJk8wLup9Fs3Xby75oFwPmDWSzes"
    assert binascii.hexlify(ser_p(wallet.get_public_key())) == "0240f1633ccfcbc1b8caae951a61ed4986f43a74f33b95133a9d6a845f4da0bb30"
    assert bitcoin_wallet(wallet.get_private_key()).get_wif(True) == "KyfmZGPLDfo64TRhf6y6RLDAZBvrRu6qJ3vue1mftbStUvHgCj2A"
   
    # Address 1
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'/0/1")
    assert bitcoin_wallet(wallet.get_private_key()).get_address_as_b58(True) == "1GCWs7cepowJUTxnqxG69UJtqff9vbZ86W"
    assert binascii.hexlify(ser_p(wallet.get_public_key())) == "02c4071687f6c5cfad040e4fdf18ae75c4571d77b030a02c9509f2ec5aa77678ca"
    assert bitcoin_wallet(wallet.get_private_key()).get_wif(True) == "L2ktncxrucystNusuuPopH8W2vrQXQPoLxLrHWkFzUrS1o5ZuspJ"
   
    # Address 2
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'/0/2")
    assert bitcoin_wallet(wallet.get_private_key()).get_address_as_b58(True) == "1FbJuUBa1SnvNCZhWeubM1TgSoyYxLzGWD"
    assert binascii.hexlify(ser_p(wallet.get_public_key())) == "0246b08c5ebbfc4bd6c8a638cb24414eea67d772b8dbc576f965789532848f001f"
    assert bitcoin_wallet(wallet.get_private_key()).get_wif(True) == "KwpYqM7wnweUJJYG3bS9SCZr3Cz83S9HvweDHAT79mKfxWRbYZAu"
   
    print "passed"
    
  def test_vector_2(self):
    encoder = mnemonic()
    
    phrase = "swallow vivid casino crisp memory library employ mystery worry neglect hold alarm fix spoil correct spin claw vivid trust base subject mixed assist brief"
    passphrase = "pazzw0rd"
    print "Testing phrase: " + phrase + "...",
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "39f1e55f86f11067b555185d2e6d86cc813b51563f54e483607a7ed471db118eb00b385d2fb34fd5faf79e74cf35ba1c98522c7790c66f27c973768dcc086a9d"
    
    # BIP 32 Root Key
    wallet = parse_path(binascii.unhexlify(seed), 'm')
    assert wallet.serialize_private() == "xprv9s21ZrQH143K2B39xaq7CnpdsqffCh85252NK394HisFHqgXXJ1xnfj4gzYacgksXQGPNhEej49RgJd3VLgLQegZW5xYU9Ez8rqLv1kCCTk"
    
    # Account Extended Keys
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'")
    assert wallet.serialize_private() == "xprv9yBLtnxPg435inGujiffBUCNWozD75fQH5NgdmqdeYfA8WxKs4LkwFePGXyMq7uhsQTbYnouArukJ82jk45tTukjfT9UoJnxEncjg1hWWxY"
    assert wallet.serialize_public() == "xpub6CAhJJVHWRbNwGMNqkCfYc974qphWYPFeJJHSAFFCtC91KHUQbf1V3xs7nbSaWcXhuHN6hwpUnVgjUkME9Cs2TEo35GfV7JQmiwkd6UpoUn"
   
    # BIP 32 Extended Keys
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'/0")
    assert wallet.serialize_private() == "xprvA27wJkVzRgyC9DS85DCGCrbctAUEE1ux6jiViXkK65J7AUZAXf2749LnkMDkFadGJkNmTKufkw61P4M4WiE4YuuuMvQDdEJ9bjjLCgy1TsF"
    assert wallet.serialize_public() == "xpub6F7HiG2tG4XVMhWbBEjGZzYMSCJidUdoTxe6Wv9veQq63GtK5CLMbwfGbetBn391UfeoXJ43KM6acczuesZfVhTRWcK3JtfpvjBftpNtdam"
   
    # Address 0
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'/0/0")
    assert bitcoin_wallet(wallet.get_private_key()).get_address_as_b58(True) == "1DDiejXEZ2uecBVKhWo1pLj4hqfiz8r2XQ"
    assert binascii.hexlify(ser_p(wallet.get_public_key())) == "03a91a3236334af3ea8997bed5cf33d25c84954d9a033a8ac8c5d23d3ca8f72fd7"
    assert bitcoin_wallet(wallet.get_private_key()).get_wif(True) == "KzdV7wCFEBbv1WF2ZSyiaZkWSm4fjVy2Hri7pL5Cq9VwEdWWDkPR"
   
    # Address 1
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'/0/1")
    assert bitcoin_wallet(wallet.get_private_key()).get_address_as_b58(True) == "1NyRQ9HPPv2FWZqhXzkjedSSYV61i4FcRV"
    assert binascii.hexlify(ser_p(wallet.get_public_key())) == "03a9948a0c53dc5325cb34e032c5935c7d631efb0b90f722f2bde0cc9962553925"
    assert bitcoin_wallet(wallet.get_private_key()).get_wif(True) == "L2RbrcUxn4zFLYKeXXWN8UntHe2mnLUiWTs4ahikHsHAEuk1Qx87"
   
    # Address 2
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'/0/2")
    assert bitcoin_wallet(wallet.get_private_key()).get_address_as_b58(True) == "1Ke1A63TvAEe5gnjfmPNqaR1rbmKQAYMV9"
    assert binascii.hexlify(ser_p(wallet.get_public_key())) == "0234a3c3b8f2b33496959c854be320605d1a5db677b2fa98c0169dcce9840b9ac5"
    assert bitcoin_wallet(wallet.get_private_key()).get_wif(True) == "L2r1UqVqJJm9q2FVG7TgtDKGimuhqFicrwRPWjtP7fu8DPKZYk1N"
   
    print "passed"
    
  def test_vector_3(self):
    encoder = mnemonic()
    
    phrase = "nominee twelve around island erupt square smoke half riot wire unable shift wave vote shock acid roof safe resemble giant front radar notice result"
    passphrase = "hi"
    print "Testing phrase: " + phrase + "...",
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "9fc772226b0f66662d78208595b0f8ff0977b43bfe35a02a8efef4234fcee7e9518eb77847cf7cc37d881d52d4ffe132ab96f10f5505ceb38f085f9b9a88986f"
    
    # BIP 32 Root Key
    wallet = parse_path(binascii.unhexlify(seed), 'm')
    assert wallet.serialize_private() == "xprv9s21ZrQH143K2XsuohTCdKvLRBNW4f2kQkTCYzfa4VKy6VGSLHu1RgAzNshQ6QbNb11fKVmhDKHFXJENNJ3CoV918WDRxUDTDVQx3vaWUEC"
    
    # Account Extended Keys
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'")
    assert wallet.serialize_private() == "xprv9xkVb8fbs1KjBB1YdoqFN1VMbctzX56JKhKLPTg3PGipT2nxhc6Xa3L1xWTdWsi2RGHiwEGVvMkZogQnkre45cB1vtjhFpEtkc7chnNW2A3"
    assert wallet.serialize_public() == "xpub6BjqzeCVhNt2Pf61jqNFj9S69ejUvXp9gvEwBr5ewcFoKq87F9Qn7qeVomshXnqhHMVsZVYzeobhuKEeMMEoFZHqfzSBdKodVKdYTtxQo1L"
   
    # BIP 32 Extended Keys
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'/0")
    assert wallet.serialize_private() == "xprv9zxz4jzwncgQLqnBhcJAKdNQYvqXbr7rceB5LrWwKcGs347pJqwZkKW3gV8aJsFtSuNDVEdocyzBoNn4c4XgFVyok3GrEndnRTwVq23GnGZ"
    assert wallet.serialize_public() == "xpub6DxLUFXqczEhZKreodqAgmK96xg21Jqhys6g9EvYswoqurSxrPFpJ7pXXkS6HoKNyNJVEECoGu8gVho2M6n6wFScC8AuL89qvD7eTN4JMTp"
   
    # Address 0
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'/0/0")
    assert bitcoin_wallet(wallet.get_private_key()).get_address_as_b58(True) == "15ofBkYCJRdSfxjUdRd5cFYSGD9tdXCosE"
    assert binascii.hexlify(ser_p(wallet.get_public_key())) == "02867ba08c5e22f9d8e7094fa95a8e3dd2e284625715a1bafaa8e267a96dd22611"
    assert bitcoin_wallet(wallet.get_private_key()).get_wif(True) == "Kwo4GS7QFdmQGUVGZWbtkKaQYJBFTccQSbnDNfVAqjWfqGcHgFuK"
   
    # Address 1
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'/0/1")
    assert bitcoin_wallet(wallet.get_private_key()).get_address_as_b58(True) == "1PvJWvJHjWbJGbV4rA7vTX1Xp22NtLr6A4"
    assert binascii.hexlify(ser_p(wallet.get_public_key())) == "0258fb30ce3a54142a8f751580cac9e7b82e1f7a03c16d1eddd1ca3e1759956d12"
    assert bitcoin_wallet(wallet.get_private_key()).get_wif(True) == "L2T7ZN5g9QSyJm6y5hSMr6Ub8mQHv7ArRpMXu1fHDZ9cFqP7BCEs"
   
    # Address 2
    wallet = parse_path(binascii.unhexlify(seed), "m/44'/0'/0'/0/2")
    assert bitcoin_wallet(wallet.get_private_key()).get_address_as_b58(True) == "1MNUXYaKSDD5f5124xYr6BV5r65Go3QTq8"
    assert binascii.hexlify(ser_p(wallet.get_public_key())) == "03558d25d3ecad28501b5654b5c3ec106a926410d9b7f5eee51f978aeb93dfe8b5"
    assert bitcoin_wallet(wallet.get_private_key()).get_wif(True) == "L4b2xRBcdQw7GMKMrCmpwZ2pvuTrQQFfjwf7M9eXnnnGnEyvTEBM"
   
    print "passed"

def run_tests():
  bip32_tests().execute_all_tests()
  bip39_tests().execute_all_tests()
  bip44_tests().execute_all_tests()
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
    assert entropy == recovered
    print "Entropy as words:     ", word_set

  elif (argv[1].lower() == "recover"):
    if len(argv) >= 3:
      word_set = argv[2].strip().lower()
      word_encoder.decode(word_set)
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
assert valid == True

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
assert valid == True

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
print "BIP 44 Private Key:   ", bip_44_key.serialize_private()
print "BIP 44 Public Key:    ", bip_44_key.serialize_public()
print "BIP 44 Path:          ", bip_44_key.get_path()

print

path = "m/44'/0'/0'/0/0"
address_0 = bip_44_key.derive_subkey(0)
print "Private Key 0:        ", bitcoin_wallet(address_0.get_private_key()).get_wif(True)
print "Private Key 0:        ", binascii.hexlify(ser_p(address_0.get_public_key()))
print "Address 0:            ", bitcoin_wallet(address_0.get_private_key()).get_address_as_b58(True)

print

path = "m/44'/0'/0'/0/1"
address_1 = bip_44_key.derive_subkey(1)
print "Private Key 1:        ", bitcoin_wallet(address_1.get_private_key()).get_wif(True)
print "Private Key 1:        ", binascii.hexlify(ser_p(address_1.get_public_key()))
print "Address 1:            ", bitcoin_wallet(address_1.get_private_key()).get_address_as_b58(True)

print
