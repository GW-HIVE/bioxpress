#wrapper to run download for both sample types


python get_data_all_samples.py gdc_sample_sheet.solid_tissue_normal.tsv | tee  get_data_all_samples_stn.log
python get_data_all_samples.py gdc_sample_sheet.primary_tumor.tsv       | tee  get_data_all_samples_pt.log

cat get_data_all_samples_stn.log > get_data_all_samples.log
cat get_data_all_samples_pt.log >> get_data_all_samples.log

