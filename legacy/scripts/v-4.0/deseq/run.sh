cur_dir=`pwd`
for study in `cat ./toRun.dat`
do
echo $study

#create directory
mkdir $study

#run script in ${study} directory
Rscript deseq.R ${study}                                   \
                ${cur_dir}/merged_gene_collapsed_filtered/${study}.htseq.counts \
                ${cur_dir}/merged_gene_collapsed_filtered/${study}.categories   \
                ${study}.log                                
               
done
