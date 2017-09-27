from lib import coin_types
from test import bch_test_vectors

from lib.base import *

# Set type of coin to "BCH" - Bitcoin Fork for Bitcoin Cash
main(coin_types.bch, bch_test_vectors)
