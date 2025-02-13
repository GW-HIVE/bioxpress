#!/bin/bash

output_dir="/home/maria.kim/bioxpress"
url="https://www.cbioportal.org/api/molecular-profiles?projection=SUMMARY&pageSize=100000&pageNumber=0&direction=ASC"
curl -G "${url}" \
     -H "accept: application/json" \
     -o "${output_dir}/all_molecular_profiles.json"