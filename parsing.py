#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re,sys,os,copy
class ReturnValue:
    SUCCESS = 0 # bez problemu
    BAD_PARAMS = 10 # chyba paramatrov
    INPUT_FILE_ERR = 11 # chyba vstupneho suboru
    OUTPUT_FILE_ERR = 12 # chyba vystupneho suboru
    BAD_HEADER = 21 # chyba headeru .IPPcode20
    BAD_OPCODE = 22 # neplatny opcode
    PARSE_ERR = 23 # parser error
    BAD_XML = 31 # chybny xml format
    LEX_ERROR = 32 # zly order, element mimo strukturu
    REDEF_ERR = 52 # redefinition error
    BAD_TYPES = 53 # zly typ operandov
    BAD_VAR = 54 # neexistujuca premenna
    NOFRAME = 55 # neexistuje ramec
    MISSING_VAL = 56 # premenna nema hodnotu
    BAD_VALUE = 57 # neplatna hodnota (delenie nulou..)
    BAD_STRING = 58 # chybna praca s retazcom
    INTERNAL_ERR = 99 # interny error

class notDefined:
    emptyString=""

class interprets:
    LastOrder=0 
    variables={}
    LFNumber=0
    TFNumber=0
    stack={}
    stackTop=-1
    readFromFile = False
    labels={}
    LineCounter=0
    returnStack={}
    RetStackCounter=-1
    inType = False
    def BOTHGiven(SourceFile, InputFile,self):
        self.variables[0]={}
        InputFile = sys. path[0]+"/"+InputFile
        SourceFile = sys. path[0]+"/"+SourceFile
        sys.stderr.write(SourceFile)
        try:
            XMLCode = ET.parse(SourceFile)
        except:
            sys.stderr.write("Chyba so vstupnym suborom XML")
            exit(ReturnValue.INPUT_FILE_ERR)
        try:
            
            self.InputCode = open(InputFile, "r")  
            self.readFromFile = True
        except:
            sys.stderr.write("Chyba so vstupnym suborom INT")
            exit(ReturnValue.INPUT_FILE_ERR)
        self.root = XMLCode.getroot()
        self.LastOrder=-1

        if not re.match('ippcode20$',self.root.attrib['language'],re.IGNORECASE):
            sys.stderr.write("NEPLATNY JAZYK:")
            sys.stderr.write(self.root.attrib['language'])
            exit(ReturnValue.LEX_ERROR)
        
        self.FindLabels(self)
        self.LineCounter = 0
        while 1:
            if self.LineCounter == len(self.root):
                break
            instruction = self.root[self.LineCounter]
            if "order" in instruction.attrib:
                
                if int(instruction.attrib['order']) == self.LastOrder:
                    sys.stderr.write("Rovnaky order...koncim")
                    exit(ReturnValue.LEX_ERROR)
                else :
                    self.LastOrder=int(instruction.attrib['order'])
                self.OrderArgs(self.root[self.LineCounter],self)
            else:
                sys.stderr.write("No order in instruction \n")
                exit(ReturnValue.LEX_ERROR)
            self.LineCounter+=1
            if self.LineCounter == len(self.root):
                break
        return 0
        

##############################   INPUT GIVEN

    def INPUTGiven(InputFile,self):
        self.variables[0]={}
        InputFile= sys. path[0]+"/"+InputFile
        try:
            self.InputCode = open(InputFile,"r")
            self.readFromFile = True
        except:
            sys.stderr.write("Chyba so vstupnym suborom")
            exit(ReturnValue.INPUT_FILE_ERR)
        XMLCode = read()
        root = ET.fromstring(XMLCode)
        self.LastOrder=-1

        if not re.match('ippcode20$',self.root.attrib['language'],re.IGNORECASE):
            sys.stderr.write("NEPLATNY JAZYK",self.root.attrib['language'])
            exit(ReturnValue.LEX_ERROR)
        
        self.FindLabels(self)
        self.LineCounter = 0
        while 1:
            if self.LineCounter == len(self.root):
                break
            instruction = self.root[self.LineCounter]
            if "order" in instruction.attrib:
                
                if int(instruction.attrib['order']) == self.LastOrder:
                    sys.stderr.write("Rovnaky order...koncim")
                    exit(ReturnValue.LEX_ERROR)
                else :
                    self.LastOrder=int(instruction.attrib['order'])
                self.DoInstruction(self.root[self.LineCounter],self)
            else:
                sys.stderr.write("No order in instruction \n")
                exit(ReturnValue.LEX_ERROR)
            self.LineCounter+=1
            if self.LineCounter == len(self.root):
                break
        
##############################     XML SOURCE GIVEN

    def XMLGiven(SourceFile,self):
        self.variables[0]={}
        SourceFile = sys. path[0]+"/"+SourceFile 
        try:
            XMLCode = ET.parse(SourceFile)
            self.readFromFile = False
        except:
            sys.stderr.write("Chyba so vstupnym suborom")
            exit(ReturnValue.INPUT_FILE_ERR)
        self.root = XMLCode.getroot()
        self.LastOrder=-1

        if not re.match('ippcode20$',self.root.attrib['language'],re.IGNORECASE):
            sys.stderr.write("NEPLATNY JAZYK",self.root.attrib['language'])
            exit(ReturnValue.LEX_ERROR)
        
        self.FindLabels(self)
        self.LineCounter = 0
        while 1:
            if self.LineCounter == len(self.root):
                break
            instruction = self.root[self.LineCounter]
            if "order" in instruction.attrib:
                
                if int(instruction.attrib['order']) == self.LastOrder:
                    sys.stderr.write("Rovnaky order...koncim")
                    exit(ReturnValue.LEX_ERROR)
                else :
                    self.LastOrder=int(instruction.attrib['order'])
                self.DoInstruction(self.root[self.LineCounter],self)
            else:
                sys.stderr.write("No order in instruction \n")
                exit(ReturnValue.LEX_ERROR)
            self.LineCounter+=1
            if self.LineCounter == len(self.root):
                break
        return 0

#################################################################################
#                           CHECKING INSTRUCTIONS
#################################################################################

    def DoInstruction(instruction,self):
        ######################          MOVE            #######################
        if re.match("^move$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=2:
                sys.stderr.write("Neplatny pocet argumentov v move\n")
                exit(ReturnValue.LEX_ERROR)
            nameOfVar=""
            ValueToWrite=""
            if "type" in instruction[1].attrib:
                ValueToWrite,typHodnoty=self.CheckType(instruction[1],self)
                
            else:
                sys.stderr.write("No type in move\n")
                exit(ReturnValue.LEX_ERROR)

            if "type" in instruction[0].attrib:

                if re.match("^var$",instruction[0].attrib['type']):
                    
                    self.SaveToVar(instruction[0],ValueToWrite,self)

                else:
                    sys.stderr.write("Bad type in move\n")
                    exit(ReturnValue.LEX_ERROR)
            else:
                sys.stderr.write("No type in move\n")
                exit(ReturnValue.LEX_ERROR)
            return 0
        ##########################      DEFVAR         ############################                
        elif re.match("^defvar$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=1:
                sys.stderr.write("Neplatny pocet argumentov v defvar\n")
                exit(ReturnValue.LEX_ERROR)
            for arg in instruction:
                if "type" in arg.attrib:
                
                    if re.match("^var$",arg.attrib['type']):
                        temp = arg.text
                        temp = temp.split("@",1)
                ######################################################GLOBAL FRAME
                        if re.match("^GF$",temp[0],re.IGNORECASE):

                            if temp[1] in self.variables[0] :
                                sys.stderr.write("Redefinicia premennej\n")
                                exit(ReturnValue.REDEF_ERR)

                            self.variables[0][temp[1]]=notDefined()
                ######################################################LOKAL FRAME
                        elif re.match("^LF$",temp[0],re.IGNORECASE):
                            if self.LFNumber == 0:
                                sys.stderr.write("LF ramec neexistuje\n")
                                exit(ReturnValue.NOFRAME)

                            if temp[1] in self.variables[self.LFNumber] :
                                sys.stderr.write("Redefinicia premennej\n")
                                exit(ReturnValue.REDEF_ERR)

                            self.variables[self.LFNumber][temp[1]]=notDefined()
                ########################################################TEMP FRAME
                        elif re.match("^TF$",temp[0],re.IGNORECASE):

                            if self.TFNumber == 0:
                                sys.stderr.write("LF ramec neexistuje\n")
                                exit(ReturnValue.NOFRAME)
                            if temp[1] in self.variables[self.TFNumber] :
                                sys.stderr.write("Redefinicia premennej\n")
                                exit(ReturnValue.REDEF_ERR)
                            self.variables[self.TFNumber][temp[1]]=notDefined()
                        else:
                            sys.stderr.write("Nespecifikovany ramec")
                            exit(ReturnValue.LEX_ERROR)
                            
                        
                else :
                    sys.stderr.write("No type in defvar\n")
                    exit(ReturnValue.LEX_ERROR)
            return 0
        elif re.match("^createframe$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=0:
                sys.stderr.write("Neplatny pocet argumentov v crateframe\n")
                exit(ReturnValue.LEX_ERROR)
            if self.LFNumber+1 == self.TFNumber:
                
                self.variables[self.TFNumber]={}
            elif self.TFNumber == 0 : 
                self.TFNumber = self.LFNumber+1
                self.variables[self.TFNumber]={}
            else : 
                print("CHYBA VO FRAMOCH PREROB TO")              
            return 0
        elif re.match("^pushframe$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=0:
                sys.stderr.write("Neplatny pocet argumentov v pushframe\n")
                exit(ReturnValue.LEX_ERROR)
            if self.TFNumber == 0:
                sys.stderr.write("Neni co pushnut\n")
                exit(ReturnValue.NOFRAME)
            self.LFNumber+=1
            self.TFNumber=0
            return 0
        elif re.match("^popframe$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=0:
                sys.stderr.write("Neplatny pocet argumentov v popframe\n")
                exit(ReturnValue.LEX_ERROR)
            if self.LFNumber ==0:
                sys.stderr.write("Neni co popnut v popframe\n")
                exit(ReturnValue.NOFRAME)
            self.variables[self.TFNumber]={}
            self.TFNumber=self.LFNumber
            self.LFNumber-=1
            return 0
    ######################x        CALL                  ################x

        elif re.match("^call$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=1:
                sys.stderr.write("Neplatny pocet argumentov v CALL \n")
                exit(ReturnValue.LEX_ERROR)
            
            if "type" in instruction[0].attrib:
        
                if re.match("^label$",instruction[0].attrib['type']):
                    
                    LabelName = instruction[0].text
                    if LabelName in self.labels:
                        self.RetStackCounter+=1
                        self.returnStack[self.RetStackCounter]=self.LineCounter
                        self.LineCounter = self.labels[LabelName]
                        self.LastOrder = int(self.root[self.LineCounter-1].attrib["order"])
                    else :
                        sys.stderr.write("Bad type in CALL\n")
                        exit(ReturnValue.REDEF_ERR)
                else:
                    sys.stderr.write("Bad type in CALL\n")
                    exit(ReturnValue.LEX_ERROR)
                
            else:
                sys.stderr.write("No type in  CALL\n")
                exit(ReturnValue.LEX_ERROR)
            return 0
    ############################            RETURN
        elif re.match("^return$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=0:
                sys.stderr.write("Neplatny pocet argumentov v RETURN \n")
                exit(ReturnValue.LEX_ERROR)
            if self.RetStackCounter == -1:
                sys.stderr.write("RETURN bez CALL \n")
                exit(ReturnValue.MISSING_VAL)
            else :
                self.LineCounter= self.returnStack[self.RetStackCounter] 
                self.RetStackCounter-=1
                self.LastOrder = int(self.root[self.LineCounter-1].attrib["order"])
            return 0
    ###########################x              PUSHS
        elif re.match("^pushs$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=1:
                sys.stderr.write("Neplatny pocet argumentov v pushs\n")
                exit(ReturnValue.LEX_ERROR)
            if "type" in instruction[0].attrib:

                ValueToWrite,typHodnoty=self.CheckType(instruction[0],self)
            else:
                sys.stderr.write("No type in PUSHS\n")
                exit(ReturnValue.LEX_ERROR)
            self.stackTop+=1
            self.stack[self.stackTop]=ValueToWrite
            return 0
    #######################             POPS
        elif re.match("^pops$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=1:
                    sys.stderr.write("Neplatny pocet argumentov v pops\n")
                    exit(ReturnValue.LEX_ERROR)

            if self.stackTop == -1:
                 sys.stderr.write("Prazdny stack v pops\n")
                 exit(ReturnValue.MISSING_VAL)
            ValueToWrite=self.stack[self.stackTop]
            self.stack[self.stackTop]=""
            self.stackTop-=1
            if "type" in instruction[0].attrib:
    
                if re.match("^var$",instruction[0].attrib['type']):
                    
                    self.SaveToVar(instruction[0],ValueToWrite,self)

                else:
                    sys.stderr.write("Bad type in pops\n")
                    exit(ReturnValue.LEX_ERROR)
            else:
                sys.stderr.write("No type in pops\n")
                exit(ReturnValue.LEX_ERROR)
            return 0

    #######################  ADD
        elif re.match("^add$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v add\n")
                exit(ReturnValue.LEX_ERROR)
            
            self.DoOperation (instruction,self,"+")
            return 0

    #######################  SUB
        elif re.match("^sub$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v sub \n")
                exit(ReturnValue.LEX_ERROR)

            self.DoOperation (instruction,self,"-")
            return 0

    #######################  MUL
        elif re.match("^mul$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v mul\n")
                exit(ReturnValue.LEX_ERROR)

            self.DoOperation (instruction,self,"*")
            return 0

    #######################  IDIV
        elif re.match("^idiv$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v idiv\n")
                exit(ReturnValue.LEX_ERROR)

            self.DoOperation (instruction,self,"//")
            return 0

    #######################  LT
        elif re.match("^lt",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v LT\n")
                exit(ReturnValue.LEX_ERROR)

            self.DoOperation (instruction,self,"<")
            return 0

    ####################### Gt
        elif re.match("^gt$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v GT\n")
                exit(ReturnValue.LEX_ERROR)

            self.DoOperation (instruction,self,">")
            return 0

    ####################x        EQUAL
        elif re.match("^eq$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v EQUAL\n")
                exit(ReturnValue.LEX_ERROR)

            self.DoOperation (instruction,self,"==")
            return 0

     #####################        AND
        elif re.match("^and$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v and\n")
                exit(ReturnValue.LEX_ERROR)

            self.DoOperation (instruction,self,"and")
            return 0

    ####################        OR
        elif re.match("^or$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v or\n")
                exit(ReturnValue.LEX_ERROR)

            self.DoOperation (instruction,self,"or")
            return 0
    #######################  NOT
        elif re.match("^not$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=2:
                sys.stderr.write("Neplatny pocet argumentov v NOT\n")
                exit(ReturnValue.LEX_ERROR)

            
            if "type" in instruction[1].attrib:
                  
                ValueToNegate,typHodnoty=self.CheckType(instruction[1],self)
            else:
                sys.stderr.write("No type in NOT\n")
                exit(ReturnValue.LEX_ERROR)
            
            if typHodnoty == bool :
                ValueToNegate = not ValueToNegate
            else:
                sys.stderr.write("bad type of var in NOT\n")
                exit(ReturnValue.BAD_TYPES)

            if "type" in instruction[0].attrib:
        
                if re.match("^var$",instruction[0].attrib['type']):
                    
                    self.SaveToVar(instruction[0],ValueToNegate,self)

                else:
                    sys.stderr.write("Bad type in NOT\n")
                    exit(ReturnValue.LEX_ERROR)
            else:
                sys.stderr.write("No type in NOT\n")
                exit(ReturnValue.LEX_ERROR)
            return 0
        
    ###########################            INT2CHAR 
        elif re.match("^int2char$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=2:
                sys.stderr.write("Neplatny pocet argumentov v INT2CHAR \n")
                exit(ReturnValue.LEX_ERROR)
            if "type" in instruction[1].attrib:
    
                ValueToWrite,typHodnoty=self.CheckType(instruction[1],self)
            else:
                sys.stderr.write("No type in INT2CHAR\n")
                exit(ReturnValue.LEX_ERROR)
            
            if typHodnoty != int :
                sys.stderr.write("No INT in INT2CHAR\n")
                exit(ReturnValue.BAD_TYPES)


            if ValueToWrite >= 0x110000 or ValueToWrite < 0:
                sys.stderr.write("No unicode char for INT in INT2CHAR\n")
                exit(ReturnValue.BAD_STRING)
            
            ValueToWrite=str(chr(ValueToWrite))

            if "type" in instruction[0].attrib:
        
                if re.match("^var$",instruction[0].attrib['type']):
                    
                    self.SaveToVar(instruction[0],ValueToWrite,self)

                else:
                    sys.stderr.write("Bad type in INT2CHAR\n")
                    exit(ReturnValue.LEX_ERROR)
            else:
                sys.stderr.write("No type in INT2CHAR\n")
                exit(ReturnValue.LEX_ERROR)
            return 0

    #####################   STR2INT
        elif re.match("^stri2int$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v STR2INT \n")
                exit(ReturnValue.LEX_ERROR)
            if "type" in instruction[1].attrib:
    
                Text,typTextu=self.CheckType(instruction[1],self)
            else:
                sys.stderr.write("No type in  STR2INT\n")
                exit(ReturnValue.LEX_ERROR)
            
            if typTextu != str :
                sys.stderr.write("No string in  STR2INT\n")
                exit(ReturnValue.BAD_TYPES)

            if "type" in instruction[2].attrib:
        
                Index,typIndex=self.CheckType(instruction[2],self)
            else:
                sys.stderr.write("No type in  STR2INT\n")
                exit(ReturnValue.LEX_ERROR)
            
            if typIndex != int :
                sys.stderr.write("No int in  STR2INT\n")
                exit(ReturnValue.BAD_TYPES)
            elif Index <0:
                sys.stderr.write("Zaporny index  STR2INT\n")
                exit(ReturnValue.BAD_STRING)

            try:
                ValueToWrite = ord(Text[Index])
            except:
                sys.stderr.write("No int in  STR2INT\n")
                exit(ReturnValue.BAD_STRING)


            if "type" in instruction[0].attrib:
            
                if re.match("^var$",instruction[0].attrib['type']):
                    
                    self.SaveToVar(instruction[0],ValueToWrite,self)

                else:
                    sys.stderr.write("Bad type in STR2INT\n")
                    exit(ReturnValue.LEX_ERROR)
            else:
                sys.stderr.write("No type in STR2INT\n")
                exit(ReturnValue.LEX_ERROR)
            return 0

################################################       READ

        elif re.match("^read$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=2:
                sys.stderr.write("Neplatny pocet argumentov v READ \n")
                exit(ReturnValue.LEX_ERROR)
            
            if "type" in instruction[1].attrib:
                if re.match("^type$",instruction[1].attrib['type']):
                    hodnotaTypu=instruction[1].text
                else :
                    sys.stderr.write("No type in type in  READ\n")
                    exit(ReturnValue.BAD_TYPES)
            else:
                sys.stderr.write("No type in  READ\n")
                exit(ReturnValue.LEX_ERROR)

            if not self.readFromFile :
                try :
                    textInput = input()
                except EOFError:
                    textInput = ""
            else :
                textInput = self.InputCode.readline()
                textInput.strip('\n')
            if hodnotaTypu == "bool" :
                if re.match("^true$",textInput,re.IGNORECASE):
                    textInput = True
                else :
                    textInput = False
            elif hodnotaTypu == "int" :
                try :
                    textInput= int(textInput)
                except:
                    textInput = None
            elif hodnotaTypu == "string":
                pass
            elif hodnotaTypu == "nil":
                textInput = None 
            else :
                sys.stderr.write("Neplatný typ v READ")
                exit(ReturnValue.LEX_ERROR)



            if "type" in instruction[0].attrib:
                
                if re.match("^var$",instruction[0].attrib['type']):
                    
                    self.SaveToVar(instruction[0],textInput,self)

                else:
                    sys.stderr.write("Bad type in READ\n")
                    exit(ReturnValue.LEX_ERROR)
            else:
                sys.stderr.write("No type in READ\n")
                exit(ReturnValue.LEX_ERROR)

            return 0

    ##############################         WRITE

        elif re.match("^write$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=1:
                sys.stderr.write("Neplatny pocet argumentov v WrITE \n")
                exit(ReturnValue.LEX_ERROR)

            if "type" in instruction[0].attrib:
        
                Text,typTextu=self.CheckType(instruction[0],self)
            else:
                sys.stderr.write("No type in  WRITE\n")
                exit(ReturnValue.LEX_ERROR)
            if typTextu == bool:
                if Text == True:
                    print ("true", end ='')
                elif Text == False:
                    print("false", end ='')
            elif typTextu == None:
                print ("",end='')
            else :
                print(Text,end='')

            return 0

    ######################      CONCAT

        elif re.match("^concat$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v CONCAT \n")
                exit(ReturnValue.LEX_ERROR)

            if "type" in instruction[1].attrib:
        
                Text1,typTextu1=self.CheckType(instruction[1],self)
            else:
                sys.stderr.write("No type in  CONCAT \n")
                exit(ReturnValue.LEX_ERROR)
            
            if "type" in instruction[2].attrib:
            
                Text2,typTextu2=self.CheckType(instruction[2],self)
            else:
                sys.stderr.write("No type in  CONCAT \n")
                exit(ReturnValue.LEX_ERROR)

            if typTextu1 == str and typTextu2 == str :
                textOutput = Text1+Text2
            else :
                sys.stderr.write("No string in  CONCAT\n")
                exit(ReturnValue.BAD_TYPES)

            if "type" in instruction[0].attrib:
                
                if re.match("^var$",instruction[0].attrib['type']):
                    
                    self.SaveToVar(instruction[0],textOutput,self)

                else:
                    sys.stderr.write("Bad type in CONCAT\n")
                    exit(ReturnValue.LEX_ERROR)
            else:
                sys.stderr.write("No type in CONCAT\n")
                exit(ReturnValue.LEX_ERROR)
            return 0

    ############################### STRLEN 

        elif re.match("^strlen$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=2:
                sys.stderr.write("Neplatny pocet argumentov v STRLEN \n")
                exit(ReturnValue.LEX_ERROR)

            if "type" in instruction[1].attrib:
        
                Text,typTextu=self.CheckType(instruction[1],self)
            else:
                sys.stderr.write("No type in  STRLEN\n")
                exit(ReturnValue.LEX_ERROR)
            
            if not typTextu == str:
                sys.stderr.write("No string in  STRLEN \n")
                exit(ReturnValue.BAD_TYPES)

            PocetZnakov = len(Text)
            if "type" in instruction[0].attrib:
                
                if re.match("^var$",instruction[0].attrib['type']):
                    
                    self.SaveToVar(instruction[0],PocetZnakov,self)

                else:
                    sys.stderr.write("Bad type in STRLEN\n")
                    exit(ReturnValue.LEX_ERROR)
            else:
                sys.stderr.write("No type in STRLEN\n")
                exit(ReturnValue.LEX_ERROR)

            return 0
    
    ################################## GET CHAR 

        elif re.match("^getchar$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v GETCHAR \n")
                exit(ReturnValue.LEX_ERROR)
            if "type" in instruction[1].attrib:
    
                Text,typTextu=self.CheckType(instruction[1],self)
            else:
                sys.stderr.write("No type in  GETCHAR\n")
                exit(ReturnValue.LEX_ERROR)
            
            if typTextu != str :
                sys.stderr.write("No string in  GETCHAR\n")
                exit(ReturnValue.BAD_TYPES)

            if "type" in instruction[2].attrib:
        
                Index,typIndex=self.CheckType(instruction[2],self)
            else:
                sys.stderr.write("No type in  GETCHAR\n")
                exit(ReturnValue.LEX_ERROR)
            
            if typIndex != int :
                sys.stderr.write("No int in  GETCHAR\n")
                exit(ReturnValue.BAD_TYPES)
            elif Index < 0 :
                sys.stderr.write("Minus index in  GETCHAR\n")
                exit(ReturnValue.BAD_STRING)
            
            try:
                ValueToWrite = Text[Index]
            except:
                sys.stderr.write("INDEX overflow in  GETCHAR\n")
                exit(ReturnValue.BAD_STRING)


            if "type" in instruction[0].attrib:
            
                if re.match("^var$",instruction[0].attrib['type']):
                    
                    self.SaveToVar(instruction[0],ValueToWrite,self)

                else:
                    sys.stderr.write("Bad type in GETCHAR\n")
                    exit(ReturnValue.LEX_ERROR)
            else:
                sys.stderr.write("No type in GETCHAR\n")
                exit(ReturnValue.LEX_ERROR)
            return 0

    ######################## SET CHAR 

        elif re.match("^setchar$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v SETCHAR \n")
                exit(ReturnValue.LEX_ERROR)
            if "type" in instruction[0].attrib:
    
                Text,typTextu=self.CheckType(instruction[0],self)
            else:
                sys.stderr.write("No type in  SETCHAR\n")
                exit(ReturnValue.LEX_ERROR)
            
            if typTextu != str :
                sys.stderr.write("No string in  SETCHAR\n")
                exit(ReturnValue.BAD_TYPES)

            ############## nacitanie indexu
            if "type" in instruction[1].attrib:
        
                Index,typIndex=self.CheckType(instruction[1],self)
            else:
                sys.stderr.write("No type in  SETCHAR\n")
                exit(ReturnValue.LEX_ERROR)
            
            if typIndex != int :
                sys.stderr.write("No int in  SETCHAR\n")
                exit(ReturnValue.BAD_TYPES)
            elif Index <0:
                sys.stderr.write("No int in  SETCHAR\n")
                exit(ReturnValue.BAD_STRING)
            ############### NACITANIE VYMENY
            if "type" in instruction[2].attrib:
        
                Znak,typZnaku=self.CheckType(instruction[2],self)
            else:
                sys.stderr.write("No type in  SETCHAR\n")
                exit(ReturnValue.LEX_ERROR)
            
            if typZnaku != str :
                sys.stderr.write("No string in  SETCHAR\n")
                exit(ReturnValue.BAD_TYPES)

            if Index > (len(Text)-1):
                sys.stderr.write("Index overflow in  SETCHAR\n")
                exit(ReturnValue.BAD_STRING)
            Vysledok=""
            try:
                for i in range(0,len(Text)-1):
                    if i == Index:
                        Vysledok+=Znak[0]
                    else :
                        Vysledok+=Text[i]
            except:
                
                sys.stderr.write("Index overflow in  SETCHAR\n")
                exit(ReturnValue.BAD_STRING)


            if "type" in instruction[0].attrib:
            
                if re.match("^var$",instruction[0].attrib['type']):
                    
                    self.SaveToVar(instruction[0],Text,self)

                else:
                    sys.stderr.write("Bad type in SETCHAR\n")
                    exit(ReturnValue.LEX_ERROR)
            else:
                sys.stderr.write("No type in SETCHAR\n")
                exit(ReturnValue.LEX_ERROR)
            return 0
    #############################           TYPE           ###################
        elif re.match("^type$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=2:
                sys.stderr.write("Neplatny pocet argumentov v TYPE \n")
                exit(ReturnValue.LEX_ERROR)

            if "type" in instruction[1].attrib:
                self.inType=True
                Text,typTextu=self.CheckType(instruction[1],self)
                self.inType = False
            else:
                sys.stderr.write("No type in  TYPE\n")
                exit(ReturnValue.LEX_ERROR)
            
            if typTextu == str :
                Vysledok = "string"
            elif typTextu == int:
                Vysledok = "int"
            elif typTextu == bool :
                Vysledok = "bool"
            elif typTextu == None :
                Vysledok = "nil"
            elif Text == "":
                Vysledok = "nil"
            elif typTextu == "notDefined":
                Vysledok =""
            else:
                sys.stderr.write("VOLAKY DIVNY TYP V TYPE \n")
                exit(ReturnValue.BAD_TYPES)

            if "type" in instruction[0].attrib:
                
                if re.match("^var$",instruction[0].attrib['type']):
                    
                    self.SaveToVar(instruction[0],Vysledok,self)

                else:
                    sys.stderr.write("Bad type in TYPE\n")
                    exit(ReturnValue.LEX_ERROR)
            else:
                sys.stderr.write("No type in TYPE\n")
                exit(ReturnValue.LEX_ERROR)
            return 0

    ##########################xx               LABEL

        elif re.match("^label$",instruction.attrib['opcode'],re.IGNORECASE):
            return 0
   
    ##################################    JUMPEQ
        elif re.match("^jumpifeq$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v JUMPEQ \n")
                exit(ReturnValue.LEX_ERROR)
            if "type" in instruction[1].attrib:
    
                Hodnota1,typHodnoty1=self.CheckType(instruction[1],self)
            else:
                sys.stderr.write("No type in  JUMPIFEQ\n")
                exit(ReturnValue.LEX_ERROR)

            if "type" in instruction[2].attrib:
        
                Hodnota2,typHodnoty2=self.CheckType(instruction[2],self)
            else:
                sys.stderr.write("No type in  JUMPIFEQ\n")
                exit(ReturnValue.LEX_ERROR)
            
            if typHodnoty1 == typHodnoty2 or typHodnoty1 == None or typHodnoty2 == None :
                if not Hodnota1==Hodnota2:
                    return 0
            else :
                sys.stderr.write("Bad type in JUMPIFEQ\n")
                exit(ReturnValue.BAD_TYPES)
        

            if "type" in instruction[0].attrib:
            
                if re.match("^label$",instruction[0].attrib['type']):
                    
                    LabelName = instruction[0].text
                    if LabelName in self.labels:
                        self.LineCounter = self.labels[LabelName]
                        self.LastOrder = int(self.root[self.LineCounter-1].attrib["order"])
                    else :
                        sys.stderr.write("Label neexistuje in JUMPIFEQ\n")
                        exit(ReturnValue.REDEF_ERR)
                else:
                    sys.stderr.write("Bad type in JUMPIFEQ\n")
                    exit(ReturnValue.LEX_ERROR)
                
            else:
                sys.stderr.write("No type in  JUMPIFEQ\n")
                exit(ReturnValue.LEX_ERROR)
            return 0

        ################################      JUMPIFNQ
        elif re.match("^jumpifneq$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=3:
                sys.stderr.write("Neplatny pocet argumentov v JUMPIFNQ \n")
                exit(ReturnValue.LEX_ERROR)
            if "type" in instruction[1].attrib:
    
                Hodnota1,typHodnoty1=self.CheckType(instruction[1],self)
            else:
                sys.stderr.write("No type in  JUMPIFNQ\n")
                exit(ReturnValue.LEX_ERROR)

            if "type" in instruction[2].attrib:
        
                Hodnota2,typHodnoty2=self.CheckType(instruction[2],self)
            else:
                sys.stderr.write("No type in  JUMPIFNQ\n")
                exit(ReturnValue.LEX_ERROR)
            
            if typHodnoty1 == typHodnoty2 or typHodnoty1 == None or typHodnoty2 == None :
                if Hodnota1==Hodnota2:
                    return 0
            else :
                sys.stderr.write("Bad type in JUMPIFNQ\n")
                exit(ReturnValue.BAD_TYPES)

            if "type" in instruction[0].attrib:
            
                if re.match("^label$",instruction[0].attrib['type']):
                    
                    LabelName = instruction[0].text
                    if LabelName in self.labels:
                        self.LineCounter = self.labels[LabelName]
                        self.LastOrder = int(self.root[self.LineCounter-1].attrib["order"])
                    else :
                        sys.stderr.write("Bad type in JUMPIFNQ\n")
                        exit(ReturnValue.REDEF_ERR)
                else:
                    sys.stderr.write("Bad type in JUMPIFNQ\n")
                    exit(ReturnValue.LEX_ERROR)
                
            else:
                sys.stderr.write("No type in  JUMPIFNQ\n")
                exit(ReturnValue.LEX_ERROR)
            return 0

    ########################xx    JUMP
        elif re.match("^jump$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=1:
                sys.stderr.write("Neplatny pocet argumentov v JUMP \n")
                exit(ReturnValue.LEX_ERROR)
            
            if "type" in instruction[0].attrib:
        
                if re.match("^label$",instruction[0].attrib['type']):
                    
                    LabelName = instruction[0].text
                    if LabelName in self.labels:
                        self.LineCounter = self.labels[LabelName]
                        self.LastOrder = int(self.root[self.LineCounter-1].attrib["order"])
                    else :
                        sys.stderr.write("Bad type in JUMPL\n")
                        exit(ReturnValue.REDEF_ERR)
                else:
                    sys.stderr.write("Bad type in JUMP\n")
                    exit(ReturnValue.LEX_ERROR)
                
            else:
                sys.stderr.write("No type in  JUMP\n")
                exit(ReturnValue.LEX_ERROR)
            
            return 0
    #######################            EXIT

        elif re.match("^exit$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=1:
                sys.stderr.write("Neplatny pocet argumentov v EXIT \n")
                exit(ReturnValue.LEX_ERROR)
            if "type" in instruction[0].attrib:
        
                Code,codeType=self.CheckType(instruction[0],self)
            else:
                sys.stderr.write("No type in  EXIT\n")
                exit(ReturnValue.LEX_ERROR)
            if codeType ==int:
                if Code > 49 or Code < 0 :
                    sys.stderr.write("No type in  EXIT\n")
                    exit(ReturnValue.BAD_VALUE)
                exit(Code)
            else : 
                sys.stderr.write("No type in  EXIT\n")
                exit(ReturnValue.BAD_TYPES)
            return 0
    #######################  DPRINT
        elif re.match("^dprint$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=0:
                sys.stderr.write("Neplatny pocet argumentov v JUMP \n")
                exit(ReturnValue.LEX_ERROR)
            
            if "type" in instruction[0].attrib:
            
                Code,codeType=self.CheckType(instruction[0],self)
            else:
                sys.stderr.write("No type in  SETCHAR\n")
                exit(ReturnValue.LEX_ERROR)
            sys.stderr.write(Code)
            sys.stderr.write("\n")
            return 0
    #######################  BREAK
        elif re.match("^break$",instruction.attrib['opcode'],re.IGNORECASE):
            if len(instruction) !=0:
                sys.stderr.write("Neplatny pocet argumentov v JUMP \n")
                exit(ReturnValue.LEX_ERROR)
            sys.stderr.write("SOM NA RIADKU :")
            sys.stderr.write(str(self.LineCounter))
            sys.stderr.write("\n")

            for ramec in self.variables:
                sys.stderr.write("HODNOTY RAMCOV:")
                sys.stderr.write(str(self.variables))
                sys.stderr.write("\n")
            return 0
    ####################### DEFAULT
        else :
            sys.stderr.write("Neznamy OPCode\n")
            exit(ReturnValue.LEX_ERROR)
        
###################################################################################################
#                                           ZACINAJU FUNKCIE
###################################################################################################

######################################   CHECKVAR
    def CheckVar(arg,self):
        temp = arg.text
        temp = temp.split("@",1)
        if re.match("^GF$",temp[0],re.IGNORECASE):
            if temp[1] in self.variables[0] :
                valueOfVar=self.variables[0][temp[1]]
            else:
                sys.stderr.write("Neexistujuca premenna\n")
                exit(ReturnValue.BAD_VAR)
            ###########            LF              ####
        elif re.match("^LF$",temp[0],re.IGNORECASE):
            if self.LFNumber == 0:
                sys.stderr.write("LF ramec neexistuje\n")
                exit(ReturnValue.NOFRAME)
            if temp[1] in self.variables[self.LFNumber]:
                nameOfVar=temp[1]
                valueOfVar=self.variables[self.LFNumber][nameOfVar]
            else :
                sys.stderr.write("Neexistujuca premenna \n")
                exit(ReturnValue.BAD_VAR)

            #################      TF           #############
        elif re.match("^TF$",temp[0],re.IGNORECASE):

            if self.TFNumber == 0:
                sys.stderr.write("LF ramec neexistuje\n")
                exit(ReturnValue.NOFRAME)
            if temp[1] in self.variables[self.TFNumber] :
                nameOfVar=temp[1]
                valueOfVar=self.variables[self.TFNumber][nameOfVar]

            else:
                sys.stderr.write("Neexistujuca premenna\n")
                exit(ReturnValue.BAD_VAR)
        else:
            sys.stderr.write("Nespecifikovany ramec")
            exit(ReturnValue.LEX_ERROR)

        if valueOfVar.__class__.__name__ == "notDefined":
            if self.inType:
                return None,"notDefined"
            else:    
                sys.stderr.write("notDefined()")
                exit(ReturnValue.MISSING_VAL)
        elif valueOfVar == None:
            return None,None
        else :
            return valueOfVar,type(valueOfVar)



################################################   CHECK TYPE 
    def CheckType(arg,self):
        if re.match("^var$",arg.attrib['type']):
                    
            
            return  self.CheckVar(arg,self)
             
        elif re.match("^string$",arg.attrib['type']):
            if arg.text == None :
                return "",str
            elif not re.match("(^((\\\\[0-9][0-9][0-9])|([^\s#\\\\]))*$)?",arg.text):
                sys.stderr.write("Chybny str type")
                exit(ReturnValue.LEX_ERROR)
            return arg.text,str

        elif re.match("^int$",arg.attrib['type']):
            if not re.match("(^(\+|\-)?[\d]+(\.|\,)?[\d]*$)?",arg.text):
                sys.stderr.write("Chybny int type")
                exit(ReturnValue.LEX_ERROR)
            elif arg.text == None:
                sys.stderr.write("Chybny int type")
                exit(ReturnValue.LEX_ERROR)
            return int(arg.text),int

        elif re.match("^bool$",arg.attrib['type']):
            if arg.text == "true":
                return True,bool
            elif arg.text == "false":
                return False,bool
            else : 
                sys.stderr.write("Chybny bool type")
                exit(ReturnValue.LEX_ERROR)
            
            
        elif re.match("^nil$",arg.attrib['type']):
            if arg.text != "nil":
                sys.stderr.write("Chybny nil type")
                exit(ReturnValue.LEX_ERROR)
            return None,None

        else:
            sys.stderr.write("Bad type in move\n")
            exit(ReturnValue.LEX_ERROR)

############################        SAVE TO VAR
    def SaveToVar(arg,ValueToWrite,self):
        temp = arg.text
        temp = temp.split("@",1)
        if re.match("^GF$",temp[0],re.IGNORECASE):    
            if temp[1] in self.variables[0] :

                valueOfVar=self.variables[0][temp[1]]=ValueToWrite
            
            else:
                sys.stderr.write("Neexistujuca premenna na zapis\n")
                exit(ReturnValue.BAD_VAR)
            ###########            LF              ####
        elif re.match("^LF$",temp[0],re.IGNORECASE):
            if self.LFNumber == 0:
                sys.stderr.write("LF ramec neexistuje\n")
                exit(ReturnValue.NOFRAME)
            if temp[1] in self.variables[self.LFNumber]:

                self.variables[self.LFNumber][temp[1]]=ValueToWrite
            
            else :
                sys.stderr.write("Neexistujuca premenna na zapis\n")
                exit(ReturnValue.BAD_VAR)

            #################      TF           #############
        elif re.match("^TF$",temp[0],re.IGNORECASE):

            if self.TFNumber == 0:
                sys.stderr.write("TF ramec neexistuje\n")
                exit(ReturnValue.NOFRAME)
            if temp[1] in self.variables[self.TFNumber] :

                self.variables[self.TFNumber][temp[1]]=ValueToWrite

            else:
                sys.stderr.write("Neexistujuca premenna na zapis\n")
                exit(ReturnValue.BAD_VAR)
        else:
            sys.stderr.write("Nespecifikovany ramec")
            exit(ReturnValue.LEX_ERROR)



#############################    DO OPERATION
    def DoOperation (instruction,self,Operacia):
        Hodnota1=0
        Hodnota2=0
        if "type" in instruction[1].attrib:
    
            Hodnota1,typHodnoty1=self.CheckType(instruction[1],self)
        else:
            sys.stderr.write("No type in DoOperation\n")
            exit(ReturnValue.LEX_ERROR)

        if "type" in instruction[2].attrib:
        
            Hodnota2,typHodnoty2=self.CheckType(instruction[2],self)
        else:
            sys.stderr.write("No type in DoOperation\n")
            exit(ReturnValue.LEX_ERROR)

        if Operacia == "+":
            if typHodnoty1 == int and typHodnoty2 == int :
                Vysledok = Hodnota1+Hodnota2
            else :
                sys.stderr.write("Zly typ operandov")
                exit(ReturnValue.BAD_TYPES)
        elif Operacia == "-":
            if typHodnoty1 == int and typHodnoty2 == int :
                Vysledok = Hodnota1-Hodnota2
            else :
                sys.stderr.write("Zly typ operandov")
                exit(ReturnValue.BAD_TYPES)
        elif Operacia == "*":
            if typHodnoty1 == int and typHodnoty2 == int :
                Vysledok = Hodnota1*Hodnota2
            else :
                sys.stderr.write("Zly typ operandov")
                exit(ReturnValue.BAD_TYPES)
        elif Operacia == "//":
            if typHodnoty1 == int and typHodnoty2 == int :
                if Hodnota2 == 0:
                    sys.stderr.write("Delenie nulou")
                    exit(ReturnValue.BAD_VALUE)
                Vysledok = Hodnota1//Hodnota2
            else :
                sys.stderr.write("Zly typ operandov")
                exit(ReturnValue.BAD_TYPES)
        elif Operacia == "<":
            if typHodnoty1 == typHodnoty2 and typHodnoty2 !=None:
                Vysledok = Hodnota1<Hodnota2
            else:
                sys.stderr.write("Zly typ operandov")
                exit(ReturnValue.BAD_TYPES)
        elif Operacia == ">":
            if typHodnoty1 == typHodnoty2 and typHodnoty2 !=None:
                Vysledok = Hodnota1>Hodnota2
            else:
                sys.stderr.write("Zly typ operandov")
                exit(ReturnValue.BAD_TYPES)
        elif Operacia == "==":
            if typHodnoty1 == typHodnoty2 :
                Vysledok = Hodnota1==Hodnota2
            elif typHodnoty1 == None:
                Vysledok = Hodnota1==Hodnota2
            elif  typHodnoty2 == None:
                Vysledok = Hodnota1==Hodnota2
            else :
                sys.stderr.write("Zly typ operandov")
                exit(ReturnValue.BAD_TYPES)

        elif Operacia == "and":
            if typHodnoty1 == bool and typHodnoty2==bool:
                Vysledok = Hodnota1 and Hodnota2

            else:
                sys.stderr.write("Zly typ operandov")
                exit(ReturnValue.BAD_TYPES)
        elif Operacia == "or":
            if typHodnoty1 == bool and typHodnoty2==bool:
                Vysledok = Hodnota1 or Hodnota2
            else:
                sys.stderr.write("Zly typ operandov")
                exit(ReturnValue.BAD_TYPES)
        else :
            sys.stderr.write("VOLACO SA pokazilo V DoOperation")
            #################   ZAPIS
        if "type" in instruction[0].attrib:
        
            if re.match("^var$",instruction[0].attrib['type']):
                
                self.SaveToVar(instruction[0],Vysledok,self)

            else:
                sys.stderr.write("Bad type in do operation\n")
                exit(ReturnValue.LEX_ERROR)
        else:
            sys.stderr.write("No type in operation\n")
            exit(ReturnValue.LEX_ERROR)

    def FunctionCycle (self,LabelName):
        FuncCounter = self.labels[LabelName]
        self.FuncOrder = int(self.root[self.LineCounter-1].attrib["order"])

        for instruction in range(self.labels[LabelName],len(self.root)):
            instruction = self.root[functionCounter]
            functionCounter+=1
            if "order" in instruction.attrib:
                self.DoInstruction(instruction,self)
            else:
                sys.stderr.write("No order in instruction \n")
                exit(ReturnValue.LEX_ERROR)
            
            
    def FindLabels (self):
        for instruction in self.root:
            self.LineCounter+=1
            if re.match("^label$",instruction.attrib['opcode'],re.IGNORECASE):
                if len(instruction) !=1:
                    sys.stderr.write("Neplatny pocet argumentov v LABEL \n")
                    exit(ReturnValue.LEX_ERROR)

                if "type" in instruction[0].attrib:
    
                    if re.match("^label$",instruction[0].attrib['type']):
                    
                        LabelName = instruction[0].text
                        if LabelName in self.labels:
                            sys.stderr.write("Bad type in JUMPL\n")
                            exit(ReturnValue.REDEF_ERR)
                        else :
                            self.labels[LabelName] = self.LineCounter-1
                    
                    else:
                        sys.stderr.write("Bad type in TYPE\n")
                        exit(ReturnValue.LEX_ERROR)

                else:
                    sys.stderr.write("No type in  TYPE\n")
                    exit(ReturnValue.LEX_ERROR)
        return 0

    def OrderArgs (instruction,self):
        newInstruction = copy.deepcopy(instruction)
        NumberOfArgs=len(instruction)
        for arg in instruction:
            if re.match("^arg1$",arg.tag):
                if NumberOfArgs<1:
                    sys.stderr.write("Neplatne cislo argumentu\n")
                    exit(ReturnValue.LEX_ERROR)
                newInstruction[0]=arg
            elif re.match("^arg2$",arg.tag):
                if NumberOfArgs<2:
                    sys.stderr.write("Neplatne cislo argumentu\n")
                    exit(ReturnValue.LEX_ERROR)
                newInstruction[1]=arg
            elif re.match("^arg3$",arg.tag):
                if NumberOfArgs<3:
                    sys.stderr.write("Neplatne cislo argumentu\n")
                    exit(ReturnValue.LEX_ERROR)
                newInstruction[2]=arg
        self.DoInstruction(newInstruction,self)

        

