class coin_type:

  def __init__(self, name, symbol, public_magic, private_magic, bip32_code, public_key_version, address_prefix, wif_version):
    self.name = name
    self.symbol = symbol
    self.public_magic = public_magic
    self.private_magic = private_magic
    self.bip32_code = bip32_code
    self.public_key_version = public_key_version
    self.address_prefix = address_prefix
    self.wif_version = wif_version

# Bitcoin
btc = coin_type(
  name = "Bitcoin",
  symbol = "btc",
  public_magic = "0488B21E", # xpub
  private_magic = "0488ADE4", # xprv
  bip32_code = "0",
  public_key_version = "00",
  address_prefix = "1",
  wif_version = "80")

# Bitcoin cash
bch = coin_type(
  name = "Bitcoin Cash",
  symbol = "bch",
  public_magic = "0488B21E", # xpub
  private_magic = "0488ADE4", # xprv
  bip32_code = "145",
  public_key_version = "00",
  address_prefix = "1",
  wif_version = "80")

# Litecoin
ltc = coin_type(
  name = "Litecoin",
  symbol = "ltc",
  public_magic = "019DA462", # Ltub
  private_magic = "019D9CFE", # Ltpv
  bip32_code = "2",
  public_key_version = "30",
  address_prefix = "",
  wif_version = "B0")

