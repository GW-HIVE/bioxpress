# Docker Container

Docker containers offer an easy and reproducible way to both run and provide building blocks for pipelines. Their value comes in 
the fact that they are sandboxed environment that have been constructed with the exact dependencies and versions the software in 
a pipeline needs to produce reproducible results.  The following are two examples of Docker containers in the Mazumder lab.  The 
first one showcases an image used for building more advanced pipelines with the BioMuta 3.0 dataset provided.  The second wraps 
the TCGA VarScan pipeline into an executable that can be run by an end user as a ‘black box’ application that generates variant 
calls from initial BAM and FASTA files.<br/>

Container that contains an installation of Biomuta for use as a base image.
  a. This container is a base image with an install of BioMuta.  BioMuta is a highly curated cancer associated SNV database 
     that draws from publicly accessible data such as TCGA, COSMIC, and ICGC, as well as variants that have been mined from 
     the literature at large.  The data set is additionally annotated with useful upstream information such as variation 
     frequency, gene name, functional impact, etc.  The BioMuta dataset is installed as a comma separated file in the 
     /biomuta directory of the docker container. 
   
   i. Login to your docker account.
   ```
   sudo docker login
   ```
   ii.	Pull Biomuta Docker:<br/>
   ```
   sudo docker pull mazumderlab/biomuta:1.0
   ```
   iii.	Check the image:
   ```
   sudo docker images
   ```
   iv.	Run the Image:
   ```
   sudo docker run -it mazumderlab/biomuta:1.0 /bin/bash
   ```
  b. In order to use this container, a user would construct a Dockerfile such as below:
  ```
  FROM mazumderlab/biomuta:1.0
  CMD [“/usr/bin/head”, “-n 5”, “/biomuta/BioMuta3.csv”]
  ```
        
  c. This is the entire Dockerfile.  This docker container is then set up as an executable that will give the user the ten initial            lines of the BioMuta database.
    
  d. An example of building it is entering the following win the directory with the Dockerfile:
  ```
  docker build –t myBioMutaExample:1.0 .
  ```
  e. An example of then running the container is the following:
  ```
  docker run –t myBioMutaExample:1.0
  ```
  f. Your output looks like the following:
  ```                                                                                                                         Index,UniProtKB_AC,Gene_Name,Refseq_Nucleotide_AC,Genomic_Position,Position(Nuc),Ref(Nuc),Var(Nuc),Position(AA),Ref(AA),Var(AA),Polyphen      ,PMID,Cancer_type,Source,Function,Study_type,Uberon_ID
    1000000,P14867,GABRA1,NM_001127648,chr5:161300148-161300148,281,G,A,94,R,H,probably damaging,-,DOID:11054 / Urinary bladder cancer       [UBC],COSMIC,Gain|Phosphorylation,SM,UBERON_0001255
    1000001,P14867,GABRA1,NM_001127644,chr5:161300148-161300148,281,G,A,94,R,H,probably damaging,-,DOID:11054 / Urinary bladder cancer       [UBC],COSMIC,Gain|Phosphorylation,SM,UBERON_0001255
    1000002,P14867,GABRA1,NM_001127645,chr5:161300148-161300148,281,G,A,94,R,H,probably damaging,-,DOID:11054 / Urinary bladder cancer       [UBC],COSMIC,Gain|Phosphorylation,SM,UBERON_0001255
    1000003,P14867,GABRA1,NM_000806,chr5:161300148-161300148,281,G,A,94,R,H,probably damaging,-,DOID:11054 / Urinary bladder cancer         [UBC],COSMIC,Gain|Phosphorylation,SM,UBERON_0001255
    1000004,P14867,GABRA1,NM_001127643,chr5:161300148-161300148,281,G,A,94,R,H,probably damaging,-,DOID:11054 / Urinary bladder cancer       [UBC],COSMIC,Gain|Phosphorylation,SM,UBERON_0001255
  ```  
  g. This illustrates the basic utility of having the BioMuta dataset accessible.  For most projects, the pipeline would be more advanced and involve certain computations done with the dataset along with downstream pipeline applications.  
      
