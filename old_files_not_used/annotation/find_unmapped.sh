sdiff sort_ensembl_noVers.txt  sort_mapped_noVers.txt  | grep "<" | awk '{print $1}' > sort_unmapped_noVers.txt
