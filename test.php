<?php

final class ReturnValue
{
	public const
		SUCCESS = 0, // bez problemu
		BAD_PARAMS = 10, // chyba paramatrov
		INPUT_FILE_ERR = 11, // chyba vstupneho suboru
		OUTPUT_FILE_ERR = 12, // chyba vystupneho suboru
		BAD_HEADER = 21, // chyba headeru .IPPcode20
		BAD_OPCODE = 22, // neplatny opcode
		PARSE_ERR = 23, // parser error
		INTERNAL_ERR = 99; // internal error
}

class Params{
    public $directoryEnable=false;
    public $parseEnable =false;
    public $interpretEnable =false;
    public $jexamxmlEnable =  false;
    public $recursiveEnable = false;
    public $helpEnable = false;
    public $interpretOnly =false;
    public $parseOnly = false;
    public $counter = 0;
    public $counterSucces =0;
    public $parseFile="";
    public $interpretFile="";
    public $jexamxmlFile="";
}

#rekurzivne(ak je zadane --recursive) volana funkcia na prejdenie suborov v priecinku
function CheckDirectory($directoryName,$params){

    $files = scandir($directoryName);
    print("<tr><td colspan=\"5\" class= \"directory\">Directory :$directoryName</td></tr>");
    $dirCountSucc=0;
    $dirCount=0;
    foreach($files as $file){
        if ($file == '.' or $file==".."){
            continue;
        }
        $isdir="$directoryName/$file";
        if (is_dir($isdir)){
            if ($params->recursiveEnable){
                CheckDirectory($isdir,$params);
            }
        }
        #Najde subor s koncovkou .src a dogeneruje ostatne subory ak neexistuju
        if (preg_match("-.*\.src-u",$file)){
            $nameOfFile = preg_split("-\.-",$file);
            $nameOfFile=$nameOfFile[0];
            if (!is_file("$directoryName/$nameOfFile.in")){
                fclose(fopen("$directoryName/$nameOfFile.in", "w"));
            }
            if (!is_file("$directoryName/$nameOfFile.out")){
                fclose(fopen("$directoryName/$nameOfFile.out", "w"));
            }
            if (!is_file("$directoryName/$nameOfFile.rc")){
                $tempFilePtr =fopen("$directoryName/$nameOfFile.rc", "w");
                fwrite($tempFilePtr,"0");
                fclose($tempFilePtr);
            }
        
        #vynecha ak je len test interpretu
        if (!$params->interpretOnly){
            $temp ="php7.4 $params->parseFile <$directoryName/$file >$directoryName/My$nameOfFile.out; echo $?";
            $ReturnCode = shell_exec("$temp");
            
            $RCFile =fopen("$directoryName/$nameOfFile.rc","r");
            $RightRetCode =intval(fgets($RCFile));
            fclose($RCFile);
            if ($RightRetCode<30){
                if ($RightRetCode != $ReturnCode ){
                    $params->counter++;
                    
                    $dirCount++;
                    print("<tr><td class= \"napis\">$params->counter. Test $nameOfFile bol :</td> <td class=\"failed\">Failed Parse</td> <td style=\"background-color:rgb(60, 202, 60)\">$RightRetCode </td><td style=\"background-color:red\">$ReturnCode</td><td style=\"background-color:rgb(60, 202, 60)\">--</td></tr>");
                
                    continue;
            }
            }
           
        
        }
        
        if ($params->parseOnly){
           $DiffNumber = shell_exec("java -jar $params->jexamxmlFile $directoryName/$nameOfFile.out $directoryName/My$nameOfFile.out $directoryName/$nameOfFile.diffs.xml /D /pub/courses/ipp/jexamxml/options; echo $?");
            if ($DiffNumber == 0 ){
                $params->counter++;
                $params->counterSucces++;
                $dirCountSucc++;
                $dirCount++;    
                print("<tr><td class= \"napis\">$params->counter. Test $nameOfFile bol :</td>  <td class=\"succes\">Succes</td> <td style=\"background-color:rgb(60, 202, 60)\">$RightRetCode </td><td style=\"background-color:rgb(60, 202, 60)\">$ReturnCode</td><td style=\"background-color:rgb(60, 202, 60)\">OK</td></tr>");
                
    
            }else {
                $params->counter++;
                
                $dirCount++;
                print("<tr><td class= \"napis\">$params->counter. Test $nameOfFile bol :</td> <td class=\"failed\">Failed Parse</td> <td style=\"background-color:rgb(60, 202, 60)\">$RightRetCode </td><td style=\"background-color:rgb(60, 202, 60)\">$ReturnCode</td><td style=\"background-color:red\">NO</td></tr>");
                
    
            }
            ###################### ZACINA INTERPRET
        }else{
            if ($params->interpretOnly){
                $temp ="python3 $params->interpretFile --source=$directoryName/$nameOfFile.src --input=$directoryName/$nameOfFile.in >$directoryName/MyFinal$nameOfFile.out; echo $?";
            }else{
                $temp ="python3 $params->interpretFile --source=$directoryName/My$nameOfFile.out --input=$directoryName/$nameOfFile.in >$directoryName/MyFinal$nameOfFile.out; echo $?";
            }
            $RCFile =fopen("$directoryName/$nameOfFile.rc","r");
            $RightRetCode =intval(fgets($RCFile));
            fclose($RCFile);
            $ReturnCode = shell_exec("$temp");
            
            if ($ReturnCode == $RightRetCode ){
                #spravny return code, ak je 0 treba porovnat vystup
                if ($ReturnCode == 0)  {
                    $diffValue = shell_exec("diff $directoryName/MyFINAL$nameOfFile.out $directoryName/$nameOfFile.out; echo $?");
                    if ($diffValue == 0 ){
                        $params->counter++;
                        $params->counterSucces++;
                        $dirCountSucc++;
                        $dirCount++;
                        
                        print("<tr><td class= \"napis\">$params->counter. Test $nameOfFile bol :</td>  <td class=\"succes\">Succes</td> <td style=\"background-color:rgb(60, 202, 60)\">$RightRetCode </td><td style=\"background-color:rgb(60, 202, 60)\">$ReturnCode</td><td style=\"background-color:rgb(60, 202, 60)\">OK</td></tr>".PHP_EOL);
                        continue;
                    }else {
                        $params->counter++;
                        
                        $dirCount++;
                        print("<tr><td class= \"napis\">$params->counter. Test $nameOfFile bol :</td> <td class=\"failed\">Failed</td><td style=\"background-color:rgb(60, 202, 60)\">$RightRetCode </td><td style=\"background-color:rgb(60, 202, 60)\">$ReturnCode</td><td style=\"background-color:red\">NO</td></tr>".PHP_EOL);
                        continue;
                    } 
                }
                $params->counter++;
                $params->counterSucces++;
                $dirCountSucc++;
                $dirCount++;
                print("<tr><td class= \"napis\">$params->counter. Test $nameOfFile bol :</td>  <td class=\"succes\">Succes</td> <td style=\"background-color:rgb(60, 202, 60)\">$RightRetCode </td><td style=\"background-color:rgb(60, 202, 60)\">$ReturnCode</td><td style=\"background-color:rgb(60, 202, 60)\">--</td></tr> ".PHP_EOL);
             
            }else {
                #nespravny return code
                $params->counter++;
                $dirCount++;
                print("<tr><td class= \"napis\">$params->counter. Test $nameOfFile bol :</td> <td class=\"failed\">Failed</td><td style=\"background-color:rgb(60, 202, 60)\">$RightRetCode </td><td style=\"background-color:red\">$ReturnCode</td><td style=\"background-color:rgb(60, 202, 60)\">--</td></tr>".PHP_EOL);
            }
            
            }
        #mazanie docasnych suborov
        if (is_file("$directoryName/My$nameOfFile.out")){
            shell_exec("rm $directoryName/My$nameOfFile.out");
        }
        if (is_file("$directoryName/MyFinal$nameOfFile.out")){
            shell_exec("rm $directoryName/MyFinal$nameOfFile.out");
        }

        }
    }
    if ($dirCount !=0){
        print("<tr><td colspan=\"5\">$directoryName : úspešných: $dirCountSucc  z  $dirCount celkovo</td></tr>".PHP_EOL);
    }

return 0;
}
 


########################################zaciatok mainu####################x
$DirectoryToProceed="";
$first = true;
$params = new params;
#############################kontrola argumentov##############################################
$helpEnable = false;
foreach($argv as $argument){
    if ($first){
        $first = false;
        continue;
    }

    if (preg_match('~--help~u',$argument)){
        $helpEnable = true;
     }elseif(preg_match('~--directory=.*~u',$argument)){
        $params->directoryEnable = true;
        $fileName = preg_split('~=~',$argument);
        $DirectoryToProceed = $fileName[1];
        if (!(is_dir($DirectoryToProceed))){
            exit(ReturnValue::INPUT_FILE_ERR);
        }
        
    }elseif (preg_match('~--recursive~u',$argument)){
        $params->recursiveEnable = true;
    }elseif (preg_match('~--parse-script=.*~u',$argument)){
        $params->parseEnable = true;
        $fileName = preg_split('~=~',$argument);
        $params->parseFile = $fileName[1];
        if (!(is_file($params->parseFile))){
            exit(ReturnValue::BAD_PARAMS);
        }
    }elseif (preg_match('~--int-script=.*~u',$argument)){
        $params->interpretEnable = true;
        $fileName = preg_split('~=~',$argument);
        $params->interpretFile = $fileName[1];
        if (!(is_file($params->interpretFile))){
            exit(ReturnValue::BAD_PARAMS);
        }
    }elseif (preg_match('~--jexamxml=.*~u',$argument)){
        $params->jexamxmlEnable = true;
        $fileName = preg_split('~=~',$argument);
        $params->jexamxmlFile = $fileName[1];
        if (!(is_file($params->jexamxmlFile))){
            exit(ReturnValue::BAD_PARAMS);
        }
    }elseif (preg_match('~--parse-only~u',$argument)){
        $params->parseOnly = true;
    }elseif (preg_match('~--int-only~u',$argument)){
        $params->interpretOnly = true;
    }else {
        exit(ReturnValue::BAD_PARAMS);
    }
}

if ($helpEnable){ 
    if($params->recursiveEnable or $params->parseOnly or
         $params->parseEnable or $params->interpretEnable or $params->interpretOnly or $params->directoryEnable){
            fwrite(STDERR,"Help nemozno kombinovat s inymi parametrami".PHP_EOL);
            exit(ReturnValue::BAD_PARAMS);
        }
            print("Skript typu filtr (parse.php v jazyce PHP 7.4) načte ze standardního vstupu zdrojový kód v IPP-
            code20 (viz sekce 6), zkontroluje lexikální a syntaktickou správnost kódu a vypíše na standardní
            výstup XML reprezentaci programu.".PHP_EOL);
            exit(ReturnValue::SUCCESS);
}

if (!$params->parseEnable){
    $params->parseFile = "parse.php";
}
if (!$params->interpretEnable){
    $params->interpretFile = "interpret.py";
}
if (!$params->jexamxmlEnable){
    $params->jexamxmlFile = "/pub/courses/ipp/jexamxml/jexamxml.jar";
}
if (!$params->directoryEnable){
    $DirectoryToProceed = ".";
}
##################################x             zaciatok vypisu
print('<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Vysledky</title>
    <style>
    body{
        text-align:center;
        margin: auto;
        width:80%;
    }
    div {
        margin-top: 40px;
        font-size: 20px;
    }
    .napis {
        text-align:left;
        width:450px;
    }
    .succes{
        background-color: rgb(60, 202, 60);
        width:30%;
    }
    .failed {
        background-color: red;
        width:30%;
    }
    .directory{
        background-color:gray;
        color:white;
        font-size:25px;
        height:40px;
        
    }

    td {
        padding:5px;
        border:2px solid black;
        text-align:center;
    }
</style>
</head>
<body>
<div>
<h1>VYSLEDKY TESTOV</h1>
<table>
<thead>
<tr><td>Názov testu</td><td>Výsledok</td><td>Správný kód</td><td>Dostaný kód</td><td>OUTPUT</td></tr>
</thead>
');
#zaciatok prechadzania suborov
CheckDirectory($DirectoryToProceed,$params);

print("Celkový výsledok :<h1>$params->counterSucces úspešných z $params->counter celkových</h1></table></div></body>");

