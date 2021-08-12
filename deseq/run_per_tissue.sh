in_dir="/data/projects/bioxpress/v-5.0/generated/annotation/per_tissue/"

for tissue in `cat list_files/tissue.dat`
do
echo $tissue

#create directory
out_dir="/data/projects/bioxpress/v-5.0/generated/deseq/per_tissue/$tissue/"
mkdir -p $out_dir

#run script in ${outdir} directory
Rscript deseq.R ${out_dir} ${in_dir}/${tissue}.htseq.counts ${in_dir}/${tissue}.categories ${tissue}.log                                
               
done
