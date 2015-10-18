import sys , profile
def createKey(shift,alphabet):
    encryptedText = ""
    myLenght = len(alphabet)
    for i in alphabet:
        encryptedText += alphabet[(alphabet.index(i)-shift)%myLenght]
    return encryptedText

def main():
    configParam = []
    if len(sys.argv) == 4:
        for e in range(1,4):
            if sys.argv[e].isdigit():
                configParam.append(int(sys.argv[e]))
            else:
                print "parameters other than filename have to be integers"
                sys.exit()
    else:
        print "usage : <filename> <shift> <numThread> <length> "
        sys.exit()
    alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    keyAlphabet =  createKey(configParam[0],alphabet)
    print keyAlphabet
    """
    myFile = None
    try:
        myFile = open('metin.txt','r')
    except:
        print "Opening failed"
        exit
      """  
    
#myfile.close()
if __name__ == '__main__':
    profile.run('print main(); print')