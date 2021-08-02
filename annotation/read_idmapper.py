########
#   grep -B1 -e  '^[[:space:]]$' unmapped.idmapper.txt | grep -v Old | grep -v -e '^[[:space:]]$' | grep -v "\-\-" | grep -v retired
########
def rmVers(versID):
    return versID.split(".")[0]


class id:
    def __init__(self, old, new, score):
        self.old_id = rmVers(old)
        self.new_id = rmVers(new)
        self.mapScore = score
    def update(self, new, score):
        self.new_id = rmVers(new)
        self.mapScore = score.rstrip()
    def retired(self):
        return ('retired' in self.new_id)

def main():
    idDict = {}
    with open ("unmapped.idmapper.txt", 'r') as idHand:
    #with open ("all.idmapper.txt", 'r') as idHand:
        for line in idHand:
            if "Old" in line: #new entry, start new id object
                new = True
            else:
                spl = line.split(",")
                if not(len(spl) == 4):
                    continue
                old = rmVers(spl[0])
                if (new):
                    idDict[old] = id(spl[0], spl[1], spl[3])
                else:
                    idDict[old].update(spl[1], spl[3])
                new = False

    for key, value in idDict.iteritems():
        if not (value.retired()):
            print value.old_id, value.new_id, value.mapScore
         







main()
