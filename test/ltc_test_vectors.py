################################################################################################
# Test Functions
################################################################################################

from lib import coin_types

from lib.base import *

coin = coin_types.ltc

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
    assert w.serialize_public() == "Ltub2SSUS19CirucWFod2ZsYA2J4v4U76YiCXHdcQttnoiy5aGanFHCPDBX7utfG6f95u1cUbZJNafmvzNCzZZJTw1EmyFoL8u1gJbGM8ipu491"
    assert w.serialize_private() == "Ltpv71G8qDifUiNetP6nmxPA5STrUVmv2J9YSmXajv8VsYBUyuPhvN9xCaQrfX2wo5xxJNtEazYCFRUu5FmokYMM79pcqz8pcdo4rNXAFPgyB4k"
    print "passed"
    
    print "Testing chain m/0'...",
    w = parse_path(coin, seed, "m/0'")
    assert w.serialize_public() == "Ltub2UhtRiSfp82berwLEKkB34QBEt2TUdCDCu4WNzGumvAMwYsxfWjULKsXhADxqy3cuDu3TnqoKJr1xmB8Wb2qzthWAtbb4CutpXPuSU1YMgG", w.serialize_public()
    assert w.serialize_private() == "Ltpv73XYpw28ZyVe2zEVyiFnxUZxoKLGQNdZ8NxUi1WcqjNmMBgtLbh3KimGSnPHCoLv1RmvxHs4dnKmo1oXQ8dXuDu8uroxrbVxZPA1gXboYvx", w.serialize_private()
    print "passed"
    
    print "Testing chain m/0'/1...",
    w = parse_path(coin, seed, "m/0'/1")
    assert w.serialize_public() == "Ltub2Wt1dVzZCpufVJymxae3doHqJG1ZUevW9DjLyG3iiYxaB6P6PK9nHtmm7EgYFukxrwX6FDHuRuLVZ4uwyvCjgYXSU6SSXqvATFvgjLDteZ8", w.serialize_public()
    assert w.serialize_private() == "Ltpv75hg2ia1xgNhsSGwhy9fZDTcrhKNQQMr4hdKJHHRnNAyajC24Q7MHHfVrqaLoj7xTWXcm7TViVHBvxKkXURWgPPaRdmgvMGpEBUPDQomMoz", w.serialize_private()
    print "passed"
    
    print "Testing chain m/0'/1/2'...",
    w = parse_path(coin, seed, "m/0'/1/2'")
    assert w.serialize_public() == "Ltub2ZVHg2pQuhm5MUmsDB3QzoKyXQt5kCWVUky2DbLstRL1awaDC4zDCLKgfFsNhnCHDTcprbGWoquU1Q4Eh1kGjzgH3zQacnyrAwqppbnDPZ9", w.serialize_public()
    assert w.serialize_private() == "Ltpv78Jx5FPsfZE7jc52xZZ2vDVm5rBtfwwqQErzYcaaxEYQzaP8s9wnBjDRQsnxmxdSxyZ1MaQR8u76AA4W7VLhoUqEnFLF5HWkqTDbr5DovYB", w.serialize_private()
    print "passed"
    
    print "Testing chain m/0'/1/2'/2...",
    w = parse_path(coin, seed, "m/0'/1/2'/2")
    assert w.serialize_public() == "Ltub2bigWTwN6BS4RxFauSFVtJVHcEApNnpgvErKUYsMCrtcx3CaFqgaPuncLarm7aM1gmjzzbkTraoaZpQEnKBUTb9XxmxmSysgBdkfyFbascs", w.serialize_public()
    assert w.serialize_private() == "Ltpv7AYLugWpr2u6p5Ykepm7oif5AfUdJYG2qikHoa74Gg72Mg1Vvve9PJgM6CCREd2t2mghyVdz3iZFdLxxJut3zsRHBVRLdNLTzRgmMZtMHv7", w.serialize_private()
    print "passed"
    
    print "Testing chain m/0'/1/2'/2/1000000000...",
    w = parse_path(coin, seed, "m/0'/1/2'/2/1000000000")
    assert w.serialize_public() == "Ltub2dSSz9YcDJpFxJ331ypEC1VHQTk8CHdiiVEsiqFVQwH7fAbxnFwEf1wfyQmhxqRjAU2YVwgGPnWBAEoFtAgKJrJeqKNrFTTJzbNbDMUZjYL", w.serialize_public()
    assert w.serialize_private() == "Ltpv7CG7PN84yAHJLRLCmNKr7Rf4xu3w8354dy8r3rVCUkVX4oQtTLtoeQqQj3yd9Y9xeB5xkrcvtm6NdWyKqytn7q4pWzBZkH6BGmF86hsLPtJ", w.serialize_private()
    print "passed"


  def test_vector_2(self):
    seed = binascii.unhexlify("fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542")
    
    print "Testing chain m...",
    w = parse_path(coin, seed, "m")
    assert w.serialize_public() == "Ltub2SSUS19CirucVsJx8iwpcE1qAFcXnAy2CsRLhqdcn75wsFbyRRyKe5giFzkEouW3oZrGWDxXykHBi9wDgkDd4vEiqBznyPWLcxwTQjJTyxX", w.serialize_public()
    assert w.serialize_private() == "Ltpv71G8qDifUiNeszc7t7TSXeBcigvLhvQN8MKK2rsKqvJMGtQu6WvtdUaT1aozybX3YRdfLGzeXXX6AnVunxk3iX9PJQD4kyhoRd9PcKyWKRK", w.serialize_private()
    print "passed"
    
    print "Testing chain m/0...",
    w = parse_path(coin, seed, "m/0")
    assert w.serialize_public() == "Ltub2ViDhiqACsjh28uFGWKhg2RMXDMnV9TJm3Ahsef4rWwuZE3wzhKPnvFxqTi8bzWV1tLSNSxHNq89sKMuZtv3QWu17EjTsjeikT47quponTX", w.serialize_public()
    assert w.serialize_private() == "Ltpv74Xt6wQcxjCjQGCR1tqKbSb95efbQttegX4gCftmvLAJxrrsfnGxnK9hb65ocfMsx5sVEHQNxgwDXJ8jMFF6ekJnJad89TsYZ33wyaWm4kk", w.serialize_private()
    print "passed"
    
    print "Testing chain m/0/2147483647'...",
    w = parse_path(coin, seed, "m/0/2147483647'")
    assert w.serialize_public() == "Ltub2WsGxKrgamuoC17RgxKM9N6uuxah2dczrCFEo3ZqWFiJ1XHQcajhzz3ZSqxFMj7aoQFz2Hotg3YkXzEFLoQA8fMdeKMXETujcqKigf4Rx1P", w.serialize_public()
    assert w.serialize_private() == "Ltpv75gwMYS9LdNqa8QbSLpy4nGhUPtVxP4Lmg9D84oYa4vhRA6LHfhGzNwJCSZnLv6MrKCP1Jc21hSKxXsW5crEE3kLjJrTuyboLpPUjzJreuq", w.serialize_private()
    print "passed"
    
    print "Testing chain m/0/2147483647'/1...",
    w = parse_path(coin, seed, "m/0/2147483647'/1")
    assert w.serialize_public() == "Ltub2ZgFNLqckRCzHcnZkcTv7K39FVTC8pYGAdk6e7EAp94jgM9Zv6GQttRwHe9P9bosPaiXrvu8KAracnVGFhq7PzpYEbZNT1LwYbzfw9HojQB", w.serialize_public()
    assert w.serialize_private() == "Ltpv78VumZR5WGg2fk5jVzyY2jCvovm14Zyc67e4y8TssxH95yxVbBDytHKg3EmQNdJ4AGZ5kbgQRF7YHEef8WNcEXZds5PGm5aBpcpDDiG4cb2", w.serialize_private()
    print "passed"
    
    print "Testing chain m/0/2147483647'/1/2147483646'...",
    w = parse_path(coin, seed, "m/0/2147483647'/1/2147483646'")
    assert w.serialize_public() == "Ltub2arHHJmyMpAhaa2AV6HTUpjLADvZBoAmCLTzApvaeuKz8hUW1mCRRQo2vJGtLyLKM2NAfRxqMnBSGReewawd7MWzWVss1JSMQq5FU6xuG3b", w.serialize_public()
    assert w.serialize_private() == "Ltpv79fwgXMS7fdjxhKLEUo5QEu7ifEN7Yc77pMxVrAHiiYPYLHRgr9zQogmfwVo13gLhqqn4RTPoch86Mk2eTH6vNEoh1vauHbpACpjHV4yMM7", w.serialize_private()
    print "passed"
    
    print "Testing chain m/0/2147483647'/1/2147483646'/2...",
    w = parse_path(coin, seed, "m/0/2147483647'/1/2147483646'/2")
    assert w.serialize_public() == "Ltub2cDKEjzUszUwKqD4DAR9Ta7JZHTfS85qrW5sacH5HhBaCtp5BQ8Bbyk2zhMAUYh1s5aPwMUFFVCRkri9mgdXRcNa9fhwwfj668GS8jig9Sj", w.serialize_public()
    assert w.serialize_private() == "Ltpv7B2ydxZwdqwyhxWDxYvmNzH67imUMsXBmyyqudWnMWPycXczrV5kbNdmkMAoA4mQk9hWMB6DFiXp8udYNmeKyLyXVsS5xhjXraAHN6qF1PS", w.serialize_private()
    print "passed"

  def test_vector_3(self):
    seed = binascii.unhexlify("4b381541583be4423346c643850da4b320e46a87ae3d2a4e6da11eba819cd4acba45d239319ac14f863b8d5ab5a0d0c64d2e8a1e7d1457df2e5a3c51c73235be")
    
    print "Testing chain m...",
    w = parse_path(coin, seed, "m")
    assert w.serialize_public() == "Ltub2SSUS19CirucUvm7f7ScpDGs2twdY38HvDBu78fB3oAjqVqF5aDHbLvEjzHDdW5gyec8LDqYNR739Ta8XTG4VFtrxRu1hwxBQgT9wAsLQiK", w.serialize_public()
    assert w.serialize_private() == "Ltpv71G8qDifUiNes44HQVxEjdSebLFSTnZdqh5sS9tt7cP9F8eAkfArajoyVaYAvckNd8JQuCgkRxFoXS7E2PtUVzedpgmhxR3miLokGHs2qhF", w.serialize_private()
    print "passed"
    
    print "Testing chain m/0'...",
    w = parse_path(coin, seed, "m/0'")
    assert w.serialize_public() == "Ltub2UogAxyLQEGxgTrWtFn7sU2XjFZ1gtYCKhRqvNM1z7676Wxhf4z9fohx3i7jMrgSB26y7BbHDNJXmvWUThCF4WAodXquFoSytrp4bdcg2zD", w.serialize_public()
    assert w.serialize_private() == "Ltpv73dLaBYoA5k14b9gdeHjntCKHgrpcdyYFBKpFPaj3vJWW9mdL9wifCbgoLtXGa5J5Gwpv9Ud5gtGAykNbcUEFkrGFpgkhaKaqMmQDeHwDdo", w.serialize_private()
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
    assert w.serialize_private() == "Ltpv71G8qDifUiNet1Um2aWvJmgmY8kY8kFT9pPASdWy7L5jWn9KmaJzQJpdTGLERnF5WXww9CkEkbXC1XqWAep1ix3gpg6qLx5hq9Ly8WnWnGn"
    print "passed"
    
    entropy = "7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth title"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "bc09fca1804f7e69da93c2f2028eb238c227f2e9dda30cd63699232578480a4021b146ad717fbb7e451ce9eb835f43620bf5c514db0f8add49f5d121449d3e87"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "Ltpv71G8qDifUiNetWfT4va83aAe3DmJ1yGY59gSgyEnMGPBrrh2iCDk1NQqXWy9Bg9nXNsr4ESecwGYkbwq17F75fFMqXtYee6YkWWh9GFYqM1"
    print "passed"
    
    entropy = "8080808080808080808080808080808080808080808080808080808080808080"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic avoid letter advice cage absurd amount doctor acoustic bless"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "c0c519bd0e91a2ed54357d9d1ebef6f5af218a153624cf4f2da911a0ed8f7a09e2ef61af0aca007096df430022f7a2b6fb91661a9589097069720d015e4e982f"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "Ltpv71G8qDifUiNetB6MrGapBn3uN6kp3e8g7CdFCYRb4XT9dXHFdqJiMEya861TiD7qx2xZFy5kAvsgpBBfKvop5phqx6BeSH3kBB7HePfFskW"
    print "passed"
    
    entropy = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo vote"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "dd48c104698c30cfe2b6142103248622fb7bb0ff692eebb00089b32d22484e1613912f0a5b694407be899ffd31ed3992c456cdf60f5d4564b8ba3f05a69890ad"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "Ltpv71G8qDifUiNesUtpSzZkDsF9Q6FVwGdHWFwC8bQzegkNx65TdRC5j5jmXXksm1W3FYsCgR5AtcKSYTvdj3QpYZmKmbFtgD6ZR82t3wGS1Lf"
    print "passed"
    
    entropy = "68a79eaca2324873eacc50cb9c6eca8cc68ea5d936f98787c60c7ebc74e6ce7c"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel tennis maple dilemma loan word shrug inflict delay length"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "64c87cde7e12ecf6704ab95bb1408bef047c22db4cc7491c4271d170a1b213d20b385bc1588d9c7b38f1b39d415665b8a9030c9ec653d75e65f847d8fc1fc440"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "Ltpv71G8qDifUiNesW6k9sufxmbMU3Ux6FPQsZ3wtcnNa8yngqz169XYsFePR5CtdSmzahhHnf1uBhB2KU4pJmHFvTmWkXquEQD8tJ69tuYHucD"
    print "passed"
    
    entropy = "9f6a2878b2520799a44ef18bc7df394e7061a224d2c33cd015b157d746869863"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "panda eyebrow bullet gorilla call smoke muffin taste mesh discover soft ostrich alcohol speed nation flash devote level hobby quick inner drive ghost inside"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "72be8e052fc4919d2adf28d5306b5474b0069df35b02303de8c1729c9538dbb6fc2d731d5f832193cd9fb6aeecbc469594a70e3dd50811b5067f3b88b28c3e8d"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "Ltpv71G8qDifUiNesV2MmfvW4ym6LMx2w3o3hTS2QyMuWvdxB59cZvvvzUVMtpF4qmTNWXjmpazbzYxuqZyMzMVvAntQoRt2vbmgzw2Cf5SKL4g"
    print "passed"

    entropy = "066dca1a2bb7e8a1db2832148ce9933eea0f3ac9548d793112d9a95c9407efad"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "all hour make first leader extend hole alien behind guard gospel lava path output census museum junior mass reopen famous sing advance salt reform"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "26e975ec644423f4a4c4f4215ef09b4bd7ef924e85d1d17c4cf3f136c2863cf6df0a475045652c57eb5fb41513ca2a2d67722b77e954b4b3fc11f7590449191d"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "Ltpv71G8qDifUiNetptFHLPgYyeExypmXWDVMtiRaFxdjCKf4FNM5g5wb1iE5B4KgJPAL92HXEAzGvx9R2UZYecX8Yvz4skeqaS6EouN2F9bKCi"
    print "passed"

    entropy = "f585c11aec520db57dd353c69554b21a89b20fb0650966fa0a9d6f74fd989d8f"
    print "Testing entropy " + entropy + "...",
    phrase = encoder.encode(binascii.unhexlify(entropy))
    assert phrase == "void come effort suffer camp survey warrior heavy shoot primary clutch crush open amazing screen patrol group space point ten exist slush involve unfold"
    seed = binascii.hexlify(encoder.generate_seed(phrase, passphrase))
    assert seed == "01f5bced59dec48e362f2c45b5de68b9fd6c92c6634f44d6d40aab69056506f0e35524a518034ddc1192e1dacd32c1ed3eaa3c3b131c88ed8e7e54c49a5d0998"
    w = parse_path(coin, binascii.unhexlify(seed), 'm')
    assert w.serialize_private() == "Ltpv71G8qDifUiNet8WMrCoQxhEFReiAwzSWFpcRfhzvr2Vq9psgbdkra47QbUzwF7VDAenq52LEWntk33tjnHZ1SWLi8b12LdAepNLD9uAgfRx"
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
    assert w.serialize_private() == "Ltpv71G8qDifUiNet4wgQfd6fB4xSj94FnpFTS7Ue5zt6vzN5tJ5vA7oUxuRW4kfQbEcXNWH9G2c5HsriikbURxPyTSgeAfauccZLBhAAHHPwnd"
    
    # Account Extended Keys
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'")
    assert w.serialize_private() == "Ltpv774HJN2KE7tnapjYF54TN8EfEao1hRst1dsE7Jbs3nLQ8pJvTXe2HJ4BpbkBysxoehKor68a3HSamjA4i1FnS9JwVznEzPJJywA7bPzgaWA"
    assert w.serialize_public() == "Ltub2YEcu9SrUGRkChSNVgYqSi4sg9VCmgSY69yFnHN9yy7zjBVznSgTHuAT4x4pD9mZLew5yn7vjqMLxumUpEqGjmTEve8F7tHqnwSpPPL5K58"
   
    # BIP 32 Extended Keys
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'/0")
    assert w.serialize_private() == "Ltpv79GhE9tvGSHVcmYYo7vArZEGaZf4wvCG32SyoHnRghNkpezskrjE5bPrCbvKjzFuPqbzC88T5RJixyKKjGs9x7odMjhPQuvqkzSmUjGt8KF"
    assert w.serialize_public() == "Ltub2aT2pwKTWapTEeFP3jQYw94V28MG2Akv7YZ1UGYictAMR2Bx5mmf6CW7T1LntWDikEgL3g8puzRy2MGVg83FAbw2BGYQz9qjaXvXyiHt3VS"
   
    # Address 0
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'/0/0")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "LMmZDN5g66qUUwGm63gBrhcL4Mo8b6wsxH"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "031cb76d4373e0724c94d4c3b90796c77013b666b3846cfe501f46cdba7d074e52"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "T6TREaHcC2X5u2XExUb6h8bSkeLJooNSD1aXVQrooBV5XNf53fEp"
   
    # Address 1
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'/0/1")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "LcU5ynFcA66eiYsss6jzRiXxRTsnAioz8n"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "021fce1230f72f747e757165c50da11d1758c6afe15dc681bfbfa42b6279870e97"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "T76xTmqLqFndu68VenCFMNFfFVDzsMKKM5wVFzThizP3QirvzpPY"
   
    # Address 2
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'/0/2")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "Lc6nqe7uNnXooU1zsvrCuyogmgUEsrKidS"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "02a0dcdff5eb706e4a025c4db767e44ce1df2a047de7a767560cb2581042cd6630"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "T8Hc5iP2Y5aAeRGm5A4kwtbdXWHStonC9FEWxjRfvJBH91kuhqL3"
   
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
    assert w.serialize_private() == "Ltpv71G8qDifUiNes9gjQUsjMD3P578XHgoQS43vGXXVHNTLJeTQPvnX9WRiem5bVQQ4SWqfTCtAt8r5fok7tTfK3m3uTeuin6J1wFTEyVpKpUB"
    
    # Account Extended Keys
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'")
    assert w.serialize_private() == "Ltpv77MVahmVhSqhJBVihyTaUJqpvaLKTXnE65GHR1JDqZk5DJr8jHGkc3zx5M8qnVpAV3929fFCfhqgRAt96gLn5hg4cDLkxJXJHpgtc2wAhhu"
    assert w.serialize_public() == "Ltub2YXqBVC2wbNev4CYxawxYtg3N92WXnLtAbNK5z4WmkXfog3D4CKBcf7DKjqJbRvRL1xQdghafrmGRQjt6gwCPHrkyhvdV9meK5CxQ5iiM7t"
   
    # BIP 32 Extended Keys
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'/0")
    assert w.serialize_private() == "Ltpv796nKbPLtoaaLbGxotku9LBuGfGgo4Begr8i394UVntbHvSFsiQjsuvUv2RoEWrSXFmvjGXzsxBnUqZR2eDnJVFtsk6FRLpaz9n8JbcycpT"
    assert w.serialize_public() == "Ltub2aH7vNot8x7XxTyo4WFHDv27iDxssJkJmNEji7pmRygBtHdLCdTAtX2kASCwUT6hTWUWoTFwUq8ET3pZ2MhZbkobpsg99QE7ERNiz4XZbtH"
   
    # Address 0
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'/0/0")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "LUBcSCMewAGstz14hbmYdwgkErZy85uGPm"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "0226624b4f8e91645251f4b16a0d4ce81cefcf5af2bcfa216f5696d1ee01d1a06f"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "T8mZQbKmZDkUfu4epuhxJDLojhzKUzKJjdZm72jST94RXHrwtLUj"
   
    # Address 1
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'/0/1")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "Lc61u3FD42GMXKfQMTnG1FAh6zFWUfQE5o"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "03693801444c1cded793f38571b954cd30bd12319ecdbec6ee14ed67a9f6640c77"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "TAfLvSPhewck1XhtMYJubyqqAbCCp5khC3cPyR5jEMeQ1zoNhRVk"
   
    # Address 2
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'/0/2")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "LWoNycg8pKVPrrnVRpe6fe7X74dQ3gN3iR"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "02c648c12f74bab045e12269c5c8ac8b0890bcc67546f8e5c0e77926021e1438e7"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "TARc5t58Qs6BfYdhgCSYJzVDr3uCFM8539by1359aDtkdqS67gAs"
    
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
    assert w.serialize_private() == "Ltpv71G8qDifUiNesWXVFbVpmk95cSqN9ei5pjUkWV4148v47J3KCvfZnWseLeEQy8EZW7awQ1RDNPyuWoMSmR2BSbWM65AcGRGV1t2r7JTxhpj"
    
    # Account Extended Keys
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'")
    assert w.serialize_private() == "Ltpv78mnhbvapquk7bLwY8bpCdkk8ctqW1VpdF59Hp6X2VfAf84y4mPtZfHG9YDkKXMSFiXu2BQ5ZWFkmZvuQtPFbZFJ2yKzy4d2Pxu1TfkXDYs"
    assert w.serialize_public() == "Ltub2Zx8JPM84zShjU3mnk6CHDaxaBb2aG4UhmBAxnroxgSmFVG3PgSKaGPXPtT79oPrpofb23CHComio7XJTjEPKN8ADbXKv9D6pXQgJULF1zg"
   
    # BIP 32 Extended Keys
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'/0")
    assert w.serialize_private() == "Ltpv79GuDnEECVxDZkdRaZWykezA9cco9RkdcWGu7neTHQ6gGTdda6MmyUcbqGNrEndxoR2BfAZndRNSjocYmqow5wLyy61AYbUFvPAPhU4ce8Z"
    assert w.serialize_public() == "Ltub2aTEpZemSeVBBdLFqB1MqEpNbBJzDgKHh2NvnmQkDatGrpphu1QCz5is5eiix68287NGSkoqUmgsYjZEhxHY7iaRMdzFD9t7NugbB2zwM1D"
   
    # Address 0
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'/0/0")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "LbKThttYijLBPkewZ1ozZqJD1ytNveoUZc"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "030124b907c411c4b481dfae1b090ca89608d6e4b8c33b8b61fce6377c870f0919"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "T4aYVxxW8QuyEaMu16Lqojbx3V8RHfPFedoDJrnJRcAZ8vWWbXBP"
   
    # Address 1
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'/0/1")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "LUNXdUau8MdsoqgEh7am6DsHTNipapsArF"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "0362f57c3dce07d456680f5366b89158c391b38935f5513b1c712d83da73853eeb"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "TAqj9bzkTGmzxqALpFpXQ7t21jEPku3C625UW4TjsdP9uKUx2RaH"
   
    # Address 2
    w = parse_path(coin, binascii.unhexlify(seed), "m/44'/2'/0'/0/2")
    assert wallet(coin, w.get_private_key()).get_address_as_b58(True) == "LayaSMF44QgptLTZKUiyYZPfv5rqVdkQxT"
    assert binascii.hexlify(ser_p(w.get_public_key())) == "0333b608d523e51bad91dfec89fb964031f590a798350abbd61f58990077549006"
    assert wallet(coin, w.get_private_key()).get_wif(True) == "T8MqFrXnb17eqTexYzA8aemdAff58EkXuQ3wSQnB5J7jW3rxfKY4"
   
    print "passed"
