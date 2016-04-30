import os
import subprocess as sub 
from pick import pick
from pick import Picker
import curses
from time import sleep
rootDIR = './'

username = "aa"


def main():
    saveResult("Output for 4.54b:\n")
    #getFileList(rootDIR)


# save the pointer pos
def savePos(index):
    try:
        f = open(rootDIR+"pos.tmp",'w')
        f.write(str(index))
        f.close()
    except:
        pass



# read the pointer pos 
def readPos():
    index = 0
    try:
        f = open(rootDIR+"pos.tmp",'r')
        index = f.readline()
    except:
        pass
    return int(index)

def saveResult(output):
    DIR = rootDIR+"res/"
    print DIR
    try:
        os.stat(DIR)
    except:
        os.mkdir(DIR)
    index = readPos()
    global username
    f = open(DIR+str(username)+".html",'a')
    f.write(output)
    f.close()

def getFileList(rootDIR):
    global username
    while True:
        title = "Please choose the student UBIT name to grade"
        list_dirs = os.walk(rootDIR)
        options = []
        for root, dirs, files in list_dirs:
            for d in dirs:
                options.append(os.path.join(root, d))
        init_index = 0
        try:
            init_index = readPos()
        except:
            pass
        option, index = pick(options, title, indicator='=>', default_index=init_index)
        username = option
        savePos(index)


        title = "Please choose the file name that you want to grade ('.v','.zip','.tar','rar')."
        def go_back(picker):
            return (None, -1)

        for files in os.walk(rootDIR+option):
            f = files[2]
        picker = Picker(f, title, indicator='=>')
        picker.register_custom_handler(curses.KEY_LEFT,  go_back)
        option2, index2 = picker.start()
        #print option2
        # run autograding 
        print option+option2
        autoGrading(option+"/"+option2)

def combinPath(path):
    if len(path) == 2:
        return str(path[0]) + str(path[1])
    return ""


# main function for grading homework
# input: Student upload zip file (path+filename)
# output: grade report
def autoGrading(f):
    # get filepath and file suffix
    path, suffix = os.path.splitext(f)

    # if it is a zip file..
    if suffix == ".zip":
        p = sub.Popen(['unzip', f, '-d', path], stdout=sub.PIPE, stderr=sub.PIPE)
        output, errors = p.communicate()
        print output
        filesList = readUncompressedFile(output)

    elif suffix == '.rar':
        pass

    # generate Options for chossing files
    def pickChoice():
        file436Module, file436test = "", ""
        while True:
            while True:
                p436 = [f for f in filesList[0] if ".v" == f[1]]
                if file436Module == "":
                    try:
                        file436ModuleL = [f for f in p436 if 'tb' not in f[0]]
                        file436Module = file436ModuleL[0]
                    except:
                        pass
                if file436test == "":
                    try:
                        file436testL = [f for f in p436 if 'tb' in f[0]] 
                        file436test = file436testL[0]
                    except:
                        pass
                title = "The filename for problem 4.36: Module: "+combinPath(file436Module)+" TestBunch: " + combinPath(file436test) + ". Is this correct?"
                option = ["YES", "NO"]
                choice, idx = pick(option, title, indicator='=>')

                p436 = [f for f in filesList[2] if ".v" == f[1]]
                if choice == "YES":
                    break
                else:
                    p436.append("None")
                    title = "Please choose the *Module* file name for Problem 4.36:"
                    file436Module, index = pick(p436, title, indicator='=>')
                 
                    title = "Please choose the *TestBunch* file name for Problem 4.36:"
                    file436test, index = pick(p436, title, indicator='=>')

            p454 = [f for f in filesList[1] if ".v" == f[1] ] 
            p454.append("None")
            title = "Please choose the *Module* file name for Problem 4.54a (BCD):"
            file454AModule, index1 = pick(p454, title, indicator='=>')
         
            title = "Please choose the *TestBunch* file name for Problem 4.54a (BCD):"
            file454Atest, index2 = pick(p454, title, indicator='=>')
           
            title = "Please choose the *Module* file name for Problem 4.54b (GC):"
            file454BModule, index3 = pick(p454, title, indicator='=>')

            title = "Please choose the *TestBunch* file name for Problem 4.54b (GC):"
            file454Btest, index4 = pick(p454, title, indicator='=>')


            title = "Is this correct?"
            option = ["YES", "NO"]
            correct, idx = pick(option, title, indicator='=>')
            if correct == "YES":
                return file436Module, file436test, file454AModule, file454Atest, file454BModule, file454Btest
    file436Module, file436test, file454AModule, file454Atest, file454BModule, file454Btest = pickChoice()    
    #return file436Module, file436test, file454AModule, file454Atest, file454BModule, file454Btest

    # Run iverilog command to compile the files and using vvp to get the output result
    output436 = compileFile([file436Module, file436test])
    if output436:
        saveResult("Output for 4.36:\n")
        saveResult(output436)
        sleep(3)
    if file454AModule == file454BModule and file454Atest == file454Btest:
        output454 = compileFile([file454AModule, file454Atest])
        if output454:
            saveResult("Output for 4.54ab:\n")
            saveResult(output454)
            sleep(3)
    else:
        output454A = compileFile([file454AModule, file454Atest])
        if output454A:
            saveResult("Output for 4.54a:\n")
            saveResult(output454A)
            sleep(3)
        output454B = compileFile([file454BModule, file454Btest])
        if output454B:
            saveResult("Output for 4.54b:\n")
            saveResult(output454B)
            sleep(3)


# track the newly added (uncompressed) files
# because student tends to have different folder name and file names ....
def readUncompressedFile(output):
    rawData = output.split("\n")
    filesList = []
    for d in rawData:
        if "inflating" in d:
            d = d.split("inflating: ")[-1]
            if d != None:
                path, suffix = os.path.splitext(d)
                suffix = suffix.strip()
                filesList.append((path,suffix))
    # import Tkinter,tkFileDialog
    # root = Tkinter.Tk()
    # homework454 = tkFileDialog.askopenfilenames(initialdir=workingPath , parent=root, title='Choose files for Problem 4.54')
    # print root.tk.splitlist(homework454)
    homework454 = [54, 454]
    homework454_a = ['BCD', 'bcd','a','1']
    homework454_b = ['GC', 'gc', 'b','2']
    homework436 = [36, 436]
    homework454_files = groupFiles(homework454,filesList)
    #homework454_files_a = groupFiles(homework454_a, homework454_files)
    #homework454_files_b = groupFiles(homework454_b, homework454_files)
    homework436_files = groupFiles(homework436,filesList)
    final_list = [homework436_files, homework454_files, filesList]
    return final_list
    

# groupFiles for different homework problems
# input: a list of keywords for certain problems, like [54, 454] for homework 4.54
# output: all the files related to that problem
def groupFiles(keywords, filesList):
    res = []
    for f in filesList:
        for k in keywords:
            #print str(k), os.path.basename(f[0]) , str(k) in os.path.basename(f[0]) 
            if str(k) in os.path.basename(f[0]) and f not in res:
                res.append(f)
    return res

# compile *.v" file and get res
# input: model file and test bunch 
# output: result
def compileFile(file, customTag="a"):
    moduleFile = file[0][0]+file[0][1]
    testFile = file[1][0] + file[1][1]
    p = sub.call(['iverilog', moduleFile, testFile, '-o', rootDIR+"out"])
    #output, errors = p.communicate()
    q = sub.Popen(['vvp', './a.out'], stdout=sub.PIPE, stderr=sub.PIPE)
    output, errors = q.communicate()
    sleep(3)
    return output  
    #readUncompressedFile(output) 





#autoGrading("./alee22/hwk4.zip")
main()