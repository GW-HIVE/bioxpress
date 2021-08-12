in_dir="/data/projects/bioxpress/v-5.0/downloads/"
out_dir="/data/projects/bioxpress/v-5.0/downloads/merged_gene_filtered"
log_file="$out_dir/merge_files_tumor_and_normal.log"

rm $log_file
touch $log_file

for study in `cat ./studies.dat`
do
echo $study

echo "############################################################################" >> $log_file
echo "python merge_files_tumor_and_normal.py $in_dir/${study}  $out_dir" >> $log_file
python merge_files_tumor_and_normal.py $in_dir/${study}  $out_dir >> $log_file

done
