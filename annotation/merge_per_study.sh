in_dir="/data/projects/bioxpress/v-4.0/downloads/tcga/files_tcga/"
out_dir="/data/projects/bioxpress/v-4.0/generated/annotation/per_study/"
log_file="$out_dir/merge_per_study.log"
map_file_one="/data/projects/bioxpress/v-4.0/downloads/ensembl/mart_export.txt"
map_file_two="/data/projects/bioxpress/v-4.0/downloads/ensembl/mart_export_remap_retired.txt"
map_file_three="/data/projects/bioxpress/v-4.0/downloads/ensembl/new_mappings.txt"



rm $log_file
touch $log_file

for study in `cat ./toy.dat`
do
echo $study



echo "######################################################################" >> $log_file
echo "python merge_per_study.py $in_dir/${study} $out_dir $map_file_one $map_file_two $map_file_three"  >> $log_file
python merge_per_study.py $in_dir/${study} $out_dir $map_file_one $map_file_two $map_file_three >> $log_file

done
