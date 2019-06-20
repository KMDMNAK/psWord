import sys
import re

#sys.argv=[program_filename , whether it's modified or not (changed)]
if(__name__=="__main__"):
    modified=int(sys.argv[1])
    with open("setup.py","r") as f:
        setuppy = f.read()
        setuppy=setuppy.split("\n")
    pattern=r'version.*?=.*?(.\..\..).*?'
    for i in range(len(setuppy)):
        search=re.search(pattern,setuppy[i])
        if(search==None):
            continue
        version_splited=search.group(1).split(".")
        if(modified):
            version_splited[2]=str(int(version_splited[2])+1)
        else:
            version_splited[1],version_splited[2]=str(int(version_splited[1])+1),"0"
        newversion=".".join(version_splited)
        #setuppy[i]=re.sub(pattern,
        setuppy[i]=setuppy[i][:search.start(1)]+newversion+setuppy[i][search.end(1):]
        break
    new_setuppy="\n".join(setuppy)
    with open("setup.py","w") as f:
        f.write(new_setuppy)


