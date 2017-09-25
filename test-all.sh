#!/bin/sh


echo "Running BTC Tests"
./test-btc.sh
if [ "$?" -ne "0" ]
then
  echo "BTC tests failed"
  exit 1
fi

echo "Running BCH Tests"
./test-bch.sh
if [ "$?" -ne "0" ]
then
  echo "BCH tests failed"
  exit 1
fi

echo "Running LTC Tests"
./test-ltc.sh
if [ "$?" -ne "0" ]
then
  echo "LTC tests failed"
  exit 1
fi

