import sys
import os
import glob

collector = {} #all samples 
want = [] #only studies with >=10 tumor and normal samples


################################################################
### From "get_data_all_samples.log" download log count up the number of samples

with open("get_data_all_samples.log", 'r') as fil:
    for line in fil:
        spl = line.split()
        #print proj_id, sam_type, len(fil_list), len(uniq_fil_list)
        if (len(spl) != 4):
             continue
        proj_id = spl[0]
        sam_type = spl[1]
        num_sam  = int(spl[2])

        #update collector data object
        if not(proj_id in collector):
            collector[proj_id] = {}
        if not(sam_type in collector[proj_id]):
            collector[proj_id][sam_type] = num_sam

################################################################
### Isolate those proj_id (tcga studies) with >= 10 tumor and normal samples

for proj_id in collector:
    if "Primary-Tumor" in collector[proj_id]:
        if collector[proj_id]["Primary-Tumor"] >= 10:
            if "Solid-Tissue-Normal" in collector[proj_id]:
                if collector[proj_id]["Solid-Tissue-Normal"] >= 10:
                    print proj_id, collector[proj_id]["Primary-Tumor"], collector[proj_id]["Solid-Tissue-Normal"]
                    want.append(proj_id)



################################################################
### Extract and compile hitlists

topDir = "/home/bfochtman/bioXpress/download/files_tcga"
for proj_id in want:
    print proj_id
    primDir = os.path.join(topDir, proj_id)

    for sam_type in ["Primary-Tumor", "Solid-Tissue-Normal"]:
        sam_typeDir = os.path.join(primDir, sam_type)
        if os.path.isdir(sam_typeDir):
            intermed_results = os.path.join(topDir, proj_id+"_"+sam_type+"_intermediate")
            #print intermed_results
            if os.path.isdir(intermed_results):
                os.system("rm -r "+intermed_results)
            os.mkdir(intermed_results)
            os.chdir(sam_typeDir)
            dwnldPath = os.path.join(sam_typeDir, "results.tar.gz")
            if (os.path.isfile(dwnldPath)):
                os.system("tar -xvzf "+dwnldPath)
                print "uncompressing",dwnldPath
            for sample in glob.glob("*"):
                sampleDir = os.path.join(sam_typeDir, sample)
                if os.path.isdir(sampleDir):
                    os.chdir(sampleDir)
                    for tmpFilGZ in glob.glob("*gz"):
                        os.system("gunzip -f "+tmpFilGZ)
                    for tmpFil in glob.glob("*counts"):
                        #os.system("cp "+tmpFil+" "+intermed_results+"/")
                        #os.system("mv "+intermed_results+"/"+tmpFil+" "+intermed_results+"/"+sample+".htseq.counts")
                        os.system("cp "+tmpFil+" "+intermed_results+"/"+sample+".htseq.counts")


    

