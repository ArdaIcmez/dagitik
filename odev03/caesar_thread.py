import sys


def main():
    configParam = []
    if len(sys.argv) == 4:
        for e in range(1,4):
            if sys.argv[e].isdigit():
                configParam.append(sys.argv[e])
            else:
                print "parameters other than filename have to be integers"
                sys.exit()
    else:
        print "usage : <filename> <shift> <numThread> <length> "
        sys.exit()
    for x in configParam:
        print x
    
    myFile = None
    try:
        myFile = open('metin.txt','r')
    except:
        print "Opening failed"
        exit
if __name__ == '__main__':
    main()