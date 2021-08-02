in_dir="/data/projects/bioxpress/v-4.0/generated/annotation/per_study/"

for study in `cat generated/misc/studies.csv | grep -v study_id`
do
echo $study

#create directory
#out_dir="/data/projects/bioxpress/v-4.0/generated/deseq/per_study/$study/"
out_dir="/data/projects/bioxpress/v-4.0/generated/deseq/tmp/$study/"

mkdir -p $out_dir

#run script in ${outdir} directory
Rscript deseq.R ${out_dir}                                   \
#Rscript logfc.R ${out_dir}
                ${in_dir}/${study}.htseq.counts \
                ${in_dir}/${study}.categories   \
                ${study}.log                                
               
done
