#!/bin/bash
if [ -d "ctr_util/src" ]; then
  rm -r ctr_util/src
fi
cp -r ../ctr_util/src ./ctr_util/src