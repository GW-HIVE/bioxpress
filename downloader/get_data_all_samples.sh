#wrapper to run download for both sample types


python get_data_all_samples.py /data/projects/bioxpress/v-5.0/downloads/gdc_sample_sheet.2021-04-28_normal.tsv | tee  /data/projects/bioxpress/v-5.0/downloads/get_data_all_samples_stn.log
python get_data_all_samples.py /data/projects/bioxpress/v-5.0/downloads/gdc_sample_sheet.2021-04-28.tsv | tee  /data/projects/bioxpress/v-5.0/downloads/get_data_all_samples_pt.log

cat /data/projects/bioxpress/v-5.0/downloads/get_data_all_samples_stn.log > /data/projects/bioxpress/v-5.0/downloads/get_data_all_samples.log
cat /data/projects/bioxpress/v-5.0/downloads/get_data_all_samples_pt.log >> /data/projects/bioxpress/v-5.0/downloads/get_data_all_samples.log

