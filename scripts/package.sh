#!/bin/bash

set -ex

abspath=`readlink -f $0`
basedir=`dirname ${abspath}`
rootdir=${basedir}/..

function build_rpm {
  pushd ${rootdir}
    cargo epack build --release -t --name etchy
  popd
}

mkdir -p ${rootdir}/target/release
cp -f ${rootdir}/dist/etchy ${rootdir}/target/release
build_rpm ecgw
find target -name "*.rpm" | xargs -I{} cp -f {} ${rootdir}
