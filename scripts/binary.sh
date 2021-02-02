#!/bin/bash

set -x

abspath=`readlink -f $0`
basedir=`dirname ${abspath}`
rootdir=${basedir}/..

pushd ${rootdir}
pyinstaller --clean -F etchy.py -n etchy
cp -f dist/etchy .
popd
