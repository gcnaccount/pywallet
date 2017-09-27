################################################################################################
# Test Functions
################################################################################################

from lib import coin_types

from lib.base import *

coin = coin_types.bch

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
    w = parse_path(coin, seed, "m")
    assert w.serialize_public() == "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8"
    assert w.serialize_private() == "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"
    print "passed"
    
    print "Testing chain m/0'...",
    w = parse_path(coin, seed, "m/0'")
    assert w.serialize_public() == "xpub68Gmy5EdvgibQVfPdqkBBCHxA5htiqg55crXYuXoQRKfDBFA1WEjWgP6LHhwBZeNK1VTsfTFUHCdrfp1bgwQ9xv5ski8PX9rL2dZXvgGDnw"
    assert w.serialize_private() == "xprv9uHRZZhk6KAJC1avXpDAp4MDc3sQKNxDiPvvkX8Br5ngLNv1TxvUxt4cV1rGL5hj6KCesnDYUhd7oWgT11eZG7XnxHrnYeSvkzY7d2bhkJ7"
    print "passed"
    
    print "Testing chain m/0'/1...",
    w = parse_path(coin, seed, "m/0'/1")
    assert w.serialize_public() == "xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ"
    assert w.serialize_private() == "xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs"
    print "passed"
    
    print "Testing chain m/0'/1/2'...",
    w = parse_path(coin, seed, "m/0'/1/2'")
    assert w.serialize_public() == "xpub6D4BDPcP2GT577Vvch3R8wDkScZWzQzMMUm3PWbmWvVJrZwQY4VUNgqFJPMM3No2dFDFGTsxxpG5uJh7n7epu4trkrX7x7DogT5Uv6fcLW5"
    assert w.serialize_private() == "xprv9z4pot5VBttmtdRTWfWQmoH1taj2axGVzFqSb8C9xaxKymcFzXBDptWmT7FwuEzG3ryjH4ktypQSAewRiNMjANTtpgP4mLTj34bhnZX7UiM"
    print "passed"
    
    print "Testing chain m/0'/1/2'/2...",
    w = parse_path(coin, seed, "m/0'/1/2'/2")
    assert w.serialize_public() == "xpub6FHa3pjLCk84BayeJxFW2SP4XRrFd1JYnxeLeU8EqN3vDfZmbqBqaGJAyiLjTAwm6ZLRQUMv1ZACTj37sR62cfN7fe5JnJ7dh8zL4fiyLHV"
    assert w.serialize_private() == "xprvA2JDeKCSNNZky6uBCviVfJSKyQ1mDYahRjijr5idH2WwLsEd4Hsb2Tyh8RfQMuPh7f7RtyzTtdrbdqqsunu5Mm3wDvUAKRHSC34sJ7in334"
    print "passed"
    
    print "Testing chain m/0'/1/2'/2/1000000000...",
    w = parse_path(coin, seed, "m/0'/1/2'/2/1000000000")
    assert w.serialize_public() == "xpub6H1LXWLaKsWFhvm6RVpEL9P4KfRZSW7abD2ttkWP3SSQvnyA8FSVqNTEcYFgJS2UaFcxupHiYkro49S8yGasTvXEYBVPamhGW6cFJodrTHy"
    assert w.serialize_private() == "xprvA41z7zogVVwxVSgdKUHDy1SKmdb533PjDz7J6N6mV6uS3ze1ai8FHa8kmHScGpWmj4WggLyQjgPie1rFSruoUihUZREPSL39UNdE3BBDu76"
    print "passed"


  def test_vector_2(self):
    seed = binascii.unhexlify("fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542")
    
    print "Testing chain m...",
    w = parse_path(coin, seed, "m")
    assert w.serialize_public() == "xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCGu8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJY47LJhkJ8UB7WEGuduB"
    assert w.serialize_private() == "xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U"
    print "passed"
    
    print "Testing chain m/0...",
    w = parse_path(coin, seed, "m/0")
    assert w.serialize_public() == "xpub69H7F5d8KSRgmmdJg2KhpAK8SR3DjMwAdkxj3ZuxV27CprR9LgpeyGmXUbC6wb7ERfvrnKZjXoUmmDznezpbZb7ap6r1D3tgFxHmwMkQTPH"
    assert w.serialize_private() == "xprv9vHkqa6EV4sPZHYqZznhT2NPtPCjKuDKGY38FBWLvgaDx45zo9WQRUT3dKYnjwih2yJD9mkrocEZXo1ex8G81dwSM1fwqWpWkeS3v86pgKt"
    print "passed"
    
    print "Testing chain m/0/2147483647'...",
    w = parse_path(coin, seed, "m/0/2147483647'")
    assert w.serialize_public() == "xpub6ASAVgeehLbnwdqV6UKMHVzgqAG8Gr6riv3Fxxpj8ksbH9ebxaEyBLZ85ySDhKiLDBrQSARLq1uNRts8RuJiHjaDMBU4Zn9h8LZNnBC5y4a"
    assert w.serialize_private() == "xprv9wSp6B7kry3Vj9m1zSnLvN3xH8RdsPP1Mh7fAaR7aRLcQMKTR2vidYEeEg2mUCTAwCd6vnxVrcjfy2kRgVsFawNzmjuHc2YmYRmagcEPdU9"
    print "passed"
    
    print "Testing chain m/0/2147483647'/1...",
    w = parse_path(coin, seed, "m/0/2147483647'/1")
    assert w.serialize_public() == "xpub6DF8uhdarytz3FWdA8TvFSvvAh8dP3283MY7p2V4SeE2wyWmG5mg5EwVvmdMVCQcoNJxGoWaU9DCWh89LojfZ537wTfunKau47EL2dhHKon"
    assert w.serialize_private() == "xprv9zFnWC6h2cLgpmSA46vutJzBcfJ8yaJGg8cX1e5StJh45BBciYTRXSd25UEPVuesF9yog62tGAQtHjXajPPdbRCHuWS6T8XA2ECKADdw4Ef"
    print "passed"
    
    print "Testing chain m/0/2147483647'/1/2147483646'...",
    w = parse_path(coin, seed, "m/0/2147483647'/1/2147483646'")
    assert w.serialize_public() == "xpub6ERApfZwUNrhLCkDtcHTcxd75RbzS1ed54G1LkBUHQVHQKqhMkhgbmJbZRkrgZw4koxb5JaHWkY4ALHY2grBGRjaDMzQLcgJvLJuZZvRcEL"
    assert w.serialize_private() == "xprvA1RpRA33e1JQ7ifknakTFpgNXPmW2YvmhqLQYMmrj4xJXXWYpDPS3xz7iAxn8L39njGVyuoseXzU6rcxFLJ8HFsTjSyQbLYnMpCqE2VbFWc"
    print "passed"
    
    print "Testing chain m/0/2147483647'/1/2147483646'/2...",
    w = parse_path(coin, seed, "m/0/2147483647'/1/2147483646'/2")
    assert w.serialize_public() == "xpub6FnCn6nSzZAw5Tw7cgR9bi15UV96gLZhjDstkXXxvCLsUXBGXPdSnLFbdpq8p9HmGsApME5hQTZ3emM2rnY5agb9rXpVGyy3bdW6EEgAtqt"
    assert w.serialize_private() == "xprvA2nrNbFZABcdryreWet9Ea4LvTJcGsqrMzxHx98MMrotbir7yrKCEXw7nadnHM8Dq38EGfSh6dqA9QWTyefMLEcBYJUuekgW4BYPJcr9E7j"
    print "passed"

  def test_vector_3(self):
    seed = binascii.unhexlify("4b381541583be4423346c643850da4b320e46a87ae3d2a4e6da11eba819cd4acba45d239319ac14f863b8d5ab5a0d0c64d2e8a1e7d1457df2e5a3c51c73235be")
    
    print "Testing chain m...",
    w = parse_path(coin, seed, "m")
    assert w.serialize_public() == "xpub661MyMwAqRbcEZVB4dScxMAdx6d4nFc9nvyvH3v4gJL378CSRZiYmhRoP7mBy6gSPSCYk6SzXPTf3ND1cZAceL7SfJ1Z3GC8vBgp2epUt13"
    assert w.serialize_private() == "xprv9s21ZrQH143K25QhxbucbDDuQ4naNntJRi4KUfWT7xo4EKsHt2QJDu7KXp1A3u7Bi1j8ph3EGsZ9Xvz9dGuVrtHHs7pXeTzjuxBrCmmhgC6"
    print "passed"
    
    print "Testing chain m/0'...",
    w = parse_path(coin, seed, "m/0'")
    assert w.serialize_public() == "xpub68NZiKmJWnxxS6aaHmn81bvJeTESw724CRDs6HbuccFQN9Ku14VQrADWgqbhhTHBaohPX4CjNLf9fq9MYo6oDaPPLPxSb7gwQN3ih19Zm4Y"
    assert w.serialize_private() == "xprv9uPDJpEQgRQfDcW7BkF7eTya6RPxXeJCqCJGHuCJ4GiRVLzkTXBAJMu2qaMWPrS7AANYqdq6vcBcBUdJCVVFceUvJFjaPdGZ2y9WACViL4L"
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
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "xprv9s21ZrQH143K32qBagUJAMU2LsHg3ka7jqMcV98Y7gVeVyNStwYS3U7yVVoDZ4btbRNf4h6ibWpY22iRmXq35qgLs79f312g2kj5539ebPM"
    print "passed"
    
    entropy = "7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth title"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "bc09fca1804f7e69da93c2f2028eb238c227f2e9dda30cd63699232578480a4021b146ad717fbb7e451ce9eb835f43620bf5c514db0f8add49f5d121449d3e87"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "xprv9s21ZrQH143K3Y1sd2XVu9wtqxJRvybCfAetjUrMMco6r3v9qZTBeXiBZkS8JxWbcGJZyio8TrZtm6pkbzG8SYt1sxwNLh3Wx7to5pgiVFU"
    print "passed"
    
    entropy = "8080808080808080808080808080808080808080808080808080808080808080"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic bless"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "c0c519bd0e91a2ed54357d9d1ebef6f5af218a153624cf4f2da911a0ed8f7a09e2ef61af0aca007096df430022f7a2b6fb91661a9589097069720d015e4e982f"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "xprv9s21ZrQH143K3CSnQNYC3MqAAqHwxeTLhDbhF43A4ss4ciWNmCY9zQGvAKUSqVUf2vPHBTSE1rB2pg4avopqSiLVzXEU8KziNnVPauTqLRo"
    print "passed"
    
    entropy = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo vote"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "dd48c104698c30cfe2b6142103248622fb7bb0ff692eebb00089b32d22484e1613912f0a5b694407be899ffd31ed3992c456cdf60f5d4564b8ba3f05a69890ad"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "xprv9s21ZrQH143K2WFF16X85T2QCpndrGwx6GueB72Zf3AHwHJaknRXNF37ZmDrtHrrLSHvbuRejXcnYxoZKvRquTPyp2JiNG3XcjQyzSEgqCB"
    print "passed"
    
    entropy = "68a79eaca2324873eacc50cb9c6eca8cc68ea5d936f98787c60c7ebc74e6ce7c"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "64c87cde7e12ecf6704ab95bb1408bef047c22db4cc7491c4271d170a1b213d20b385bc1588d9c7b38f1b39d415665b8a9030c9ec653d75e65f847d8fc1fc440"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "xprv9s21ZrQH143K2XTAhys3pMNcGn261Fi5Ta2Pw8PwaVPhg3D8DWkzWQwjTJfskj8ofb81i9NP2cUNKxwjueJHHMQAnxtivTA75uUFqPFeWzk"
    print "passed"
    
    entropy = "9f6a2878b2520799a44ef18bc7df394e7061a224d2c33cd015b157d746869863"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "panda eyebrow bullet gorilla call smoke muffin taste mesh discover soft ostrich alcohol speed nation flash devote level hobby quick inner drive ghost inside"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "72be8e052fc4919d2adf28d5306b5474b0069df35b02303de8c1729c9538dbb6fc2d731d5f832193cd9fb6aeecbc469594a70e3dd50811b5067f3b88b28c3e8d"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "xprv9s21ZrQH143K2WNnKmssvZYM96VAr47iHUQUTUyUXH3sAGNjhJANddnhw3i3y3pBbRAVk5M5qUGFr4rHbEWwXgX4qrvrceifCYQJbbFDems"
    print "passed"

    entropy = "066dca1a2bb7e8a1db2832148ce9933eea0f3ac9548d793112d9a95c9407efad"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "all hour make first leader extend hole alien behind guard gospel lava path output census museum junior mass reopen famous sing advance salt reform"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "26e975ec644423f4a4c4f4215ef09b4bd7ef924e85d1d17c4cf3f136c2863cf6df0a475045652c57eb5fb41513ca2a2d67722b77e954b4b3fc11f7590449191d"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "xprv9s21ZrQH143K3rEfqSM4QZRVmiMuSWY9wugscmaCjYja3SbUD3KPEB1a7QXJoajyR2T1SiXU7rFVRXMV9XdYVSZe7JoUXdP4SRHTxsT1nzm"
    print "passed"

    entropy = "f585c11aec520db57dd353c69554b21a89b20fb0650966fa0a9d6f74fd989d8f"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "void come effort suffer camp survey warrior heavy shoot primary clutch crush open amazing screen patrol group space point ten exist slush involve unfold"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "01f5bced59dec48e362f2c45b5de68b9fd6c92c6634f44d6d40aab69056506f0e35524a518034ddc1192e1dacd32c1ed3eaa3c3b131c88ed8e7e54c49a5d0998"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "xprv9s21ZrQH143K39rnQJknpH1WEPFJrzmAqqasiDcVrNuk926oizzJDDQkdiTvNPr2FYDYzWgiMiC63YmfPAa2oPyNB23r2g7d1yiK6WpqaQS"
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
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "xprv9s21ZrQH143K36J6xmaUWkrDFTgCAo8v3T5vgbcT7HQH55XD3XMF88CmYJDeXsbRcFw14kP5vDBCjDdX5JyRLM5LgbiQbfZXXo5G6nnPbM9"
    
    # Account Extended Keys
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'")
    assert w.serialize_private() == "xprv9ymfPsSR8x5aRgQJHedAZXLnh2P2JNzGPw2fNMFWLKd7Xgtaqru7XNEEdxWjciL1SZj7rJDoCS48hQj714bZozSispMLoLxmtp5CMDqQiQY"
    assert w.serialize_public() == "xpub6Cm1oNyJyKdseAUmPgAAvfHXF4DWhqi7m9xGAjf7tfA6QVDjPQDN5AYiVFggvDVyaCAkPWiaSDCAfGeqBQraqfQyCkNuk1LM8z77qY572i2"
   
    # BIP 32 Extended Keys
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'/0")
    assert w.serialize_private() == "xprvA2KASUhSAH6cGuM9SqZkyY8zEVuL5M7nMDdVNQBLGfu5hxKKmxJoLeHCVSuVyDyoVtiAuJy4VQ9abfsbCZ81Qqmg3pV24amS9WHVa1xUeiM"
    assert w.serialize_public() == "xpub6FJWqzEKzeeuVPRcYs6mLg5inXjpUoqdiSZ6Anawq1S4akeUKVd3tSbgLjoqPxHFbNaLj8LU7xbU2dGoEMJShF74cm1XTq2feTdthWNcULd"
   
    # Address 0
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'/0/0")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "1CsUBwrDeKrQdvCrTMojtPeB6CBvNEzE9V"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "02a5928c1cc4692761a0d99ccb8f0ade38968710d8e06fd7fa3992ca55d4e2dbb5"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "Ky1fGJxcrMTCSdwa2C47wR6VwMQqS3xx32vTR92JqpxZe4HcgS7U"
   
    # Address 1
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'/0/1")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "19jn6GtJHgeUKRuFyP3Kkoqp7kJXLmFgL3"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "03f2e5dce72dfb74dcf209222a55c59fc62f121c67c252ba46c42da1db64adf8fc"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "L1JJYqPh4MRvg14hhLAyfRU3yUgVeuvqBXuFEGW4Md8gh9zX4sur"
   
    # Address 2
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'/0/2")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "15Pk1H3dyg8i5S3Bq7JvtVudVFUkfASyFG"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "020d639ea1a4b91d97b576ac5288f0eca53fdfd14e742b0a1f853512f023ed2fca"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "L12wtwuL85nx3Rs34xRi7WREumjGCwM4V73R6ZD3mTeDJHj774Dh"
   
    print "passed"
    
  def test_vector_2(self):
    encoder = mnemonic()
    
    phrase = "swallow vivid casino crisp memory library employ mystery worry neglect hold alarm fix spoil correct spin claw vivid trust base subject mixed assist brief"
    passphrase = "pazzw0rd"
    print "Testing phrase: " + phrase + "...",
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "39f1e55f86f11067b555185d2e6d86cc813b51563f54e483607a7ed471db118eb00b385d2fb34fd5faf79e74cf35ba1c98522c7790c66f27c973768dcc086a9d"
    
    # BIP 32 Root Key
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "xprv9s21ZrQH143K2B39xaq7CnpdsqffCh85252NK394HisFHqgXXJ1xnfj4gzYacgksXQGPNhEej49RgJd3VLgLQegZW5xYU9Ez8rqLv1kCCTk"
    
    # Account Extended Keys
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'")
    assert w.serialize_private() == "xprv9ykUNwp9XmShzuefxtYL3Qa81HiVXdr6S8pqiucBPDzjtnYCXqFfHbMMeeErq8cmT97qG9gcAiLfUQkGQhG6PZa9v5vCgysbaZfnkNyPBXp"
    assert w.serialize_public() == "xpub6CjpnTM3N911DPj94v5LQYWrZKYyw6ZwoMkSXJ1nwZXimasM5NZuqPfqVtV3zASgWBYCssEZdRGJPernVNmnzdbJigNLFaMXoQo1HShNxhD"
   
    # BIP 32 Extended Keys
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'/0")
    assert w.serialize_private() == "xprvA1jCfdhVt3gZEYt2XYKfv1JYvAWKxuFSivsxVqSY16cuS8JcPHBLbfhXFzpwCzbVJSHSbue3g3jVR7N7zsqfPVEwM9FcmLXp8KXfMBxdD7Z"
    assert w.serialize_public() == "xpub6EiZ59EPiRErT2xVdZrgH9FHUCLpNMyJ69oZJDr9ZS9tJvdkvpVb9U217HKevnkefLqK7cLrnkSeF5bC8RvP98GYLEtQdiLDYb6nEGikYKc"
   
    # Address 0
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'/0/0")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "1AmqoU6jjtXU13MDygWAYU3gmDvWimq5CC"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "0288bbe33f2125dce5a9999afb73dafbb7adca3d0bac136a9a3be36e2c49d5c37c"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "KyP5sSEiRgTvQDroJuaTzLL2NpJ4mFZzvg4Y8Dy4aDydGwF8gdhy"
   
    # Address 1
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'/0/1")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "1DR7zk8S3Xp53UkNopex3F1eFhQnVnRude"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "02f381f9977920d66b2a43ae6da8e2f827a8674510ac593724c3f60e69ecaa8115"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "KwogkX9QQ1NfSXQgCaj9RyQTqAzisAELvywUDpha3qYKBvSqzpsr"
   
    # Address 2
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'/0/2")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "1MRMfAY5bQLVFCHaBQBgM6iPxEMKZKZnkU"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "03879acdad33885c130dd53f57e93ae5ed882d381b4779998cd88e5da2d3f79042"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "Kx7WMNvrfe1oGsQuZTMDEQxJtnn3UYVA88XJHpp7DSUdkPSGu5SZ"
    
    print "passed"
    
  def test_vector_3(self):
    encoder = mnemonic()
    
    phrase = "nominee twelve around island erupt square smoke half riot wire unable shift wave vote shock acid roof safe resemble giant front radar notice result"
    passphrase = "hi"
    print "Testing phrase: " + phrase + "...",
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "9fc772226b0f66662d78208595b0f8ff0977b43bfe35a02a8efef4234fcee7e9518eb77847cf7cc37d881d52d4ffe132ab96f10f5505ceb38f085f9b9a88986f"
    
    # BIP 32 Root Key
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "xprv9s21ZrQH143K2XsuohTCdKvLRBNW4f2kQkTCYzfa4VKy6VGSLHu1RgAzNshQ6QbNb11fKVmhDKHFXJENNJ3CoV918WDRxUDTDVQx3vaWUEC"
    
    # Account Extended Keys
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'")
    assert w.serialize_private() == "xprv9yEc6BLstPi24iicphk5GEyWR2YVtuSyu6egbmFgLoSTrsMumZSMsm4rPLJVZgW9oYA2YPCG6FSSJe5AoczYz6yQGwUL2j3tCaRf6BvkiAQ"
    assert w.serialize_public() == "xpub6CDxVgsmimGKHCo5vjH5dNvEy4NzJNAqGKaHQ9fHu8ySjfh4K6kcRZPLEbpMksJQVdPuPJESLW4uDfnLQ6Jtpz8vFsAGooN5qmgTsaVwAhy"
   
    # BIP 32 Extended Keys
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'/0")
    assert w.serialize_private() == "xprv9zrAp9LDrjoRUSxEUKDCeD9FJ2QztAQSdYCakHuuTNnCxwYCrYaPEjvc6jHMbuYU78uEbvUbG55R37rMqmegpxrpJarn9M549XpEvysM7Rz"
    assert w.serialize_public() == "xpub6DqXDes7h7Migw2haLkD1M5yr4FVHd8Hzm8BYgKX1iKBqjsMQ5tdnYF5wzjSumGWa29aQ7jfG7vNmLPezRVW4Kk8d13y9ytYRcqM2n7HStr"
   
    # Address 0
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'/0/0")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "1EWWNDPheZu1J29acSKFTkS5B86SozoSXi"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "02d79d4e9e66740cbd3e5f0caecf666f7a9f8a28a0b7fc0a9b373641d5b97f83b1"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "Ky2fjqFZs3heaRCjdZAPhrGCqnb3rFVTw1TyMQyXdJ4YqTUiCM4W"
   
    # Address 1
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'/0/1")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "1A8EDgMSd2V41hb9VKet8eCaNVUk87EGz3"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "03b308291a2f3f3246c9351c9f14786882c22a3b5703dea2ad51fd64e065b45064"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "L2XfMs3LxL4MFxXtLLbFyQehNeBDq6d3r83XG3nHmQpZVwtH3Lkb"
   
    # Address 2
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/145'/0'/0/2")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "14CibJgfQEbou6DQaqr48aDq48an9h8c9H"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "03bb786df6253de706fb8b521b6f9a61cd54cb9bd04359596811c1b24a9abdd572"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "L5WuBa8ExEdrYTd1DCmsUjoz8imjF23mavZmmFNp2TGAU6KV57oh"
   
    print "passed"
