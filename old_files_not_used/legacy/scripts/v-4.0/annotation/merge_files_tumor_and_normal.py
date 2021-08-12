import sys
import os
import glob


class DF:
    def __init__(self):
        self.counts = {}
        self.transList = [] #to maintain order
        self.geneList  = []
        self.fileList = [] #to maintain order
        self.nameDict = {}
    def addFile(self, file, id1, id2):
        self.nameDict[id1] = {"status":id2}
        self.fileList.append(id1)
        with open(file, 'r') as inpt:
            for line in inpt:
                #expect
                #ENSG00000000003.13      5290
                #ENSG00000000005.5       0
                #ENSG00000000419.11      1954
                spl = line.split("\t")
                trans = spl[0].split(".")[0] #remove version - we do not have this for the mappings
                count = spl[1].rstrip() #can keep as string 
             
                if not(trans in self.counts): #need to add
                    self.transList.append(trans)
                    self.counts[trans] = {}
                self.counts[trans][id1] = count

    def updateGene(self, trans, gene, filter):
        if ("MIR" in gene):
            return
        if ("ENSGR" in trans):
            return
        seenGene = False
        if not(gene in self.geneList):
            self.geneList.append(gene)
            self.counts[gene] = {}
        else:
            seenGene = True
        
        for file in self.fileList:
            if not(seenGene):
                self.counts[gene][file] = 0
            self.counts[gene][file] += int(self.counts[trans][file]) #was treated as string for transcripts

    def trans2Genes(self, trans2gene, ret2new, filter=True):
       #trans2gene and ret2new are transcript keyed dictionaries
       #filter wil remove transcripts with ENGR and genes with MIR TODO clean this
        for trans in self.transList:
           if trans in trans2gene: 
              self.updateGene(trans, trans2gene[trans], filter)
           elif trans in ret2new:
              transNew = ret2new[trans] 
              self.updateGene(trans, trans2gene[transNew], filter) #use count from old, gene name from new
           else:
               #print "{} not mapped to gene.".format(trans)
               continue

    
    def writeHitList(self, output_file):
        #print self.fileList
        if os.path.isfile(output_file):
            print "Warning: Overwritting ",output_file
        with open(output_file, "w") as opt:
            string = "transcript"+","
            string += ",".join(self.fileList)
            string += "\n"
            opt.write(string)
            for trans in self.transList:
                if trans[0] == "_": #ignore these
                    continue
                string = trans
                for id in self.fileList:
                    string += ","
                    try:
                        string += self.counts[trans][id]
                    except:
                        #no info for this trans and sample
                        string += 'NaN'
                string += "\n"
                opt.write(string)
        print "Completed writing of", output_file  

    def writeGeneHitList(self, output_file):
        #print self.fileList
        if os.path.isfile(output_file):
    	    print "Warning: Overwritting ",output_file
        with open(output_file, "w") as opt:
	    string = "gene"+","
	    string += ",".join(self.fileList)
	    string += "\n"
	    opt.write(string)
	    for gene in self.geneList:
	        if gene[0] == "_": #ignore these
		    continue
 	        string = gene 
	        for id in self.fileList:
		    string += ","
		    try:
		        string += str(self.counts[gene][id])
		    except:
		        #no info for this trans and sample
		        string += 'NaN'
	        string += "\n"
	        opt.write(string)
        print "Completed writing of", output_file  



    def writeCategoryTable(self, output_file):    
        if os.path.isfile(output_file):
            print "Warning: Overwritting ",output_file
        with open(output_file, "w") as opt:
            string = "id,status"
            string += "\n"
            opt.write(string)
            for id in self.fileList:
                string = id
                string += ","
                try:
                    string += self.nameDict[id]["status"]
                except:
                    #no info for this trans and sample
                    string += 'NaN'
                string += "\n"
                opt.write(string)
        print "Completed writing of", output_file  





def main():
    intermediate_dir_fragment = sys.argv[1]
    final_dir = sys.argv[2]
   
    if not(os.path.isdir(final_dir)):
        os.mkdir(final_dir)


    #######
    #create dictionary mapping transcripts to gene names
    trans2gene = {}
    with open(sys.argv[3]) as trans2geneHand: #mart_exort.txt for ones that are trivially mapped
        first = True
        for line in trans2geneHand:
            if (first):
                first = False
                spl = line.split("\t")
                if ("Gene name" == spl[0]):
                    geneIdx = 0
                    transIdx = 1
                else:
                    geneIdx = 1
                    transIdx = 0

                continue
            else:
                spl = line.split("\t")
                trans = spl[transIdx].rstrip()
                gene  = spl[geneIdx].rstrip()
                trans2gene[trans] = gene   
    with open(sys.argv[4], 'r') as retTrans2geneHand: #mart_export_remap_retired.txt 
        first = True
        for line in retTrans2geneHand:
            if (first):
                first = False
                if ("Gene name" == spl[0]):
                    geneIdx = 0
                    transIdx = 1
                else:
                    geneIdx = 1
                    transIdx = 0
                continue
            else:
                spl = line.split("\t")
                trans = spl[transIdx].rstrip()
                gene  = spl[geneIdx].rstrip()
                trans2gene[trans] = gene   
  
    print "awww yea we have this many entries in our list mothafucka {}".format(len(trans2gene))


    ####
    # create updated idmapping list (new ids for retired ids)
    ret2new = {}
    with open(sys.argv[5], 'r') as ret2newHand: #new_mappings.txt created by idmappings, no header 
        for line in ret2newHand:
            spl = line.split()
            ret2new[spl[0]] = spl[1] 


 
    name_frag = intermediate_dir_fragment.split("/")[-1] #last part of path

    id_dict = {} #id:status
    frame = DF() 


    for status in ["Primary-Tumor", "Solid-Tissue-Normal"]:
        intermediate_dir = intermediate_dir_fragment+"_"+status+"_intermediate"
        files = os.listdir(intermediate_dir)
        id_dict[status] = []

        #################################################################
        ##### Get all file ids from file names
        print "Reading file ids from", intermediate_dir
        for file in files:
            if ".htseq.counts" in file:
                id = file.replace(".htseq.counts","")
                id_dict[status].append(id)

            else:
                #counts not in filename
                print "WARNING, non count file in intermediate directory", file
                #sys.exit()


        #################################################################
        ##### upload all files in directory into frame
        #TODO this is highly ram heavy
        print "Starting merge" 
        
        for id in id_dict[status]:
            full_path = id+".htseq.counts"
            full_path = os.path.join(intermediate_dir, full_path) 
            #print "adding", full_path
            frame.addFile(full_path, id, status)
        
    #############################################################
    #collapse transcripts into genes by summation
    frame.trans2Genes(trans2gene, ret2new, True) 

    #################################################################
    ##### print DF after both status
    print "Beginning writeHitList"    
    output_file = os.path.join(final_dir, name_frag+".htseq.counts")
    #frame.writeHitList(output_file)
    frame.writeGeneHitList(output_file)
    output_file = os.path.join(final_dir, name_frag+".categories")
    frame.writeCategoryTable(output_file)

main()
