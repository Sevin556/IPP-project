 

import re,sys,os
import os.path
from parsing import interprets,ReturnValue


IsFirst = InputEnable = XMLEnable = HelpEnable = False
SourceFile = InputEnable = ""
for argument in sys.argv:
    if argument=="--help":
        HelpEnable = True
    elif re.match('--source=.*',argument):
        XMLEnable = True
        argument, SourceFile = argument.split("=",1)
        if not os.path.exists(SourceFile):
            sys.stderr.write("Neexistujuci subor XML\n")
            exit (ReturnValue.INPUT_FILE_ERR)
    elif re.match('--input=.*',argument):
        InputEnable = True
        argument, InputFile = argument.split("=",1)
        if not os.path.exists(InputFile):
            sys.stderr.write("Neexistujuci subor inputu\n")
            exit (ReturnValue.INPUT_FILE_ERR)
    elif not IsFirst:
        IsFirst = True
    else :
        sys.stderr.write("NEZNAMY PARAMETER\n")
        exit(ReturnValue.BAD_PARAMS)

if HelpEnable:
    if XMLEnable or InputEnable:
        exit (ReturnValue.BAD_PARAMS)
    print("Skript typu filtr (parse.php v jazyce PHP 7.4) načte ze standardního vstupu zdrojový kód v IPP-"
    "code20 (viz sekce 6), zkontroluje lexikální a syntaktickou správnost kódu a vypíše na standardní"
    "výstup XML reprezentaci programu.")
    exit(ReturnValue.SUCCESS)

if not InputEnable and not XMLEnable:
    sys.stderr.write("Nezadany src ani input file, koncim\n")
    exit(ReturnValue.BAD_PARAMS)
elif InputEnable and XMLEnable:
    #print("OBA ENABLE")
    interprets.BOTHGiven(SourceFile,InputFile,interprets)
elif InputEnable and not XMLEnable:
    #print("INPUT ENABLE")
    interprets.INPUTGiven(InputFile,interprets)
else :
    #print("XML ENABLE")
    interprets.XMLGiven(SourceFile,interprets) 




