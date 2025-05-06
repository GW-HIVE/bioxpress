#!/bin/bash
set -e # Exit on any error

# Get today's date in yyyy_mm_dd format
TODAY=$(date +"%Y_%m_%d")

cd /data/shared/repos/bioxpress/downloads
mkdir -p "$TODAY"
ln -sfn "$TODAY" current