in_dir="/data/projects/bioxpress/v-4.0/generated/annotation/per_case/"

for case in `cat generated/misc/cases.csv | grep -v case_id`
do
echo $case

#create directory
out_dir="/data/projects/bioxpress/v-4.0/generated/deseq/tmp/$case/"
mkdir -p $out_dir

#run script in ${outdir} directory
Rscript deseq.R ${out_dir}                                   \
                ${in_dir}/${case}.htseq.counts \
                ${in_dir}/${case}.categories   \
                ${case}.log                                
               
done
