import collections

import sys
import gc

import html

class FileFormater:
    def __init__(self, file):
        self.file = file
    def __iter__(self):
        return self
    def seek(self):
        self.file.seek(0)
    def close(self):
        self.file.close()
    def __next__(self):
        line = self.file.readline()
        if line == '':
            raise StopIteration

        line = line[1:-3]

        inQuotes = False
        special = False
        offset = 0
        for index, char in enumerate(line):
            if char == ',' and inQuotes:
                line = line[:index + offset] + "\\" + line[index + offset:]
                offset += 1
            
            if char == "\"" and special == False:
                inQuotes = not inQuotes
           
            if char == "\\" and special:
                special = False
                continue
            
            special = False;
            if char == "\\":
                special = True

        # TODO: Merge into one loop... shouldn't realy affect performance that much tho. 
        inQuotes = False
        special = False
        offset = 0
        lineSplit = []  
        sectionLen = -1
        for index, char in enumerate(line):
            sectionLen += 1
            if char == ',' and not inQuotes:
                lineSplit.append(line[index - sectionLen:index])
                sectionLen = -1

            if char == "\"" and special == False:
                inQuotes = not inQuotes

            if char == "\\" and special:
                special = False
                continue

            special = False;
            if char == "\\":
                special = True

        line = lineSplit
        tokens = []
        for token in line:
            token = token.split("\":", 1)

            if len(token) != 2:
                print ("FAILURE!")
                print (line)
                print (token)
                raise AssertionError
                continue
            token[0] = token[0][1:] 
            if token[1].startswith('"') and token[1].endswith('"'):
                token[1] = token[1][1:-1]
            tokens.append(token)
        return tokens

def Main():
    fileName = sys.argv[1]

    #input("Press enter to handle: " + fileName + "...")
    
    ff = FileFormater(open("./Decompressed/" + fileName))

    cols = set()

    for tokens in ff:
        for token in tokens:
            cols.add(token[0])

    print (cols)

    #input("Press enter to handle: " + fileName + "...")
    ff.seek()

    # drop first line
    ff.__next__()

    fo = open("./FormatedConv/" + fileName, 'w')
    
    cols = list(cols)

    for col in cols[:-1]:
        fo.write(col + ",")
    fo.write(cols[-1:][0] + "\n")

    for tokens in ff:
        for col in cols[:-1]:
            found = False
            for token in tokens:
                if col == token[0]:
                    token[1] = token[1].replace("\\\"", "\"\"")
                    token[1] = token[1].replace("\\,", ",")
                    
                    token[1] = html.escape(token[1]).encode('ascii', 'xmlcharrefreplace').decode()

                    if token[1] == "null":
                        fo.write(",")
                    elif token[1] == "false":
                        fo.write("0,")
                    elif token[1] == "true":
                        fo.write("1,")
                    else:
                        fo.write("\"" + token[1] + "\",")
                    found = True
            if not found:
                fo.write(",")

        found = False
        for token in tokens:
            if cols[-1:][0] == token[0]:
                token[1] = token[1].replace("\\\"", "\"\"")
                token[1] = token[1].replace("\\,", ",")
                
                token[1] = html.escape(token[1]).encode('ascii', 'xmlcharrefreplace').decode()

                if token[1] == "null":
                    fo.write("\n")
                elif token[1] == "false":
                    fo.write("0\n")
                elif token[1] == "true":
                    fo.write("1\n")
                else:
                    fo.write("\"" + token[1] + "\"\n")
                found = True
        if not found:
            fo.write("\n")

    fo.close()
    ff.close()
Main()
