in_dir="/data/projects/bioxpress/v-4.0/downloads/tcga/files_tcga/"
out_dir="/data/projects/bioxpress/v-4.0/generated/downloader/merged_gene_filtered/"
log_file="$out_dir/merge_files_tumor_and_normal.log"

rm $log_file
touch $log_file

for study in `cat ./toy.dat`
do
echo $study

echo "############################################################################" >> $log_file
echo "python merge_files_tumor_and_normal.py $in_dir/${study}  $out_dir" >> $log_file
python merge_files_tumor_and_normal.py $in_dir/${study}  $out_dir >> $log_file

done
