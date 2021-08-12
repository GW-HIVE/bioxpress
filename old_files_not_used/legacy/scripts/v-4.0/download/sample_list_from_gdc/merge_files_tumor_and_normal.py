import sys
import os
import glob


class DF:
    def __init__(self):
        self.counts = {}
        self.geneList = [] #to maintain order
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
                gene = spl[0]
                count = spl[1].rstrip() #can keep as string 
             
                if not(gene in self.counts): #need to add
                    self.geneList.append(gene)
                    self.counts[gene] = {}
                self.counts[gene][id1] = count
    
    def writeHitList(self, output_file):
        #print self.fileList
        if os.path.isfile(output_file):
            print "Warning: Overwritting ",output_file
        with open(output_file, "w") as opt:
            string = "transcript"+","
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
                        string += self.counts[gene][id]
                    except:
                        #no info for this gene and sample
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
                    #no info for this gene and sample
                    string += 'NaN'
                string += "\n"
                opt.write(string)
        print "Completed writing of", output_file  





def main():
    intermediate_dir_fragment = sys.argv[1]
    final_dir = sys.argv[2]
   
    if not(os.path.isdir(final_dir)):
        os.mkdir(final_dir)


 
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
        
        

    #################################################################
    ##### print DF after both status
    print "Beginning writeHitList"    
    output_file = os.path.join(final_dir, name_frag+".htseq.counts")
    frame.writeHitList(output_file)
    output_file = os.path.join(final_dir, name_frag+".categories")
    frame.writeCategoryTable(output_file)

main()
