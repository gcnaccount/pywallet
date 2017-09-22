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