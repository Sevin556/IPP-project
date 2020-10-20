<?php

/**

 * Class s return hodnotami
 */
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
		INTERNAL_ERR = 99; // interny error
}

class STATS{
    public $comments = 0;
    public $loc=0;
    public $labels=0;
    public $jumps=0;
    public $fileName = "";
    public $statsToPrint = " ";
}
/*
*Class s regularnymi vyrazmi pre kontrolu argumentov instrukcii
*/
class REGEXES
{
public const
		NULLT = '(?:(nil)@(nil))',
		INTT = '(?:(int)@((?:\+|\-)?\d+))',
		BOOLT = '(?:(bool)@(true|false))',
		STRINGT = '(?:(string)@((?:[^\s#\\\\]|(?:\\\\\d{3}))*))',
		CONST =
			'(?:' . self::NULLT . '|' .self::INTT . '|' . self::BOOLT . '|' . self::STRINGT . ')',
		SPEC_CHARS = '_\-\$&%\*!\?',
		ID =
			'(?:[[:alpha:]' . self::SPEC_CHARS . '][[:alnum:]' . self::SPEC_CHARS . ']*)',
		TYPE = '(int|bool|string)',
		VAR = '((?:GF|LF|TF)@' . self::ID . ')',
		SYMB = '(?:' . self::CONST .'|'. self::VAR . ')',
        LABEL = '(' . self::ID . ')';

public function CheckArgs($stats,$number,$words,$numberOfArgs) {
    if ($number > $numberOfArgs){
        if ($words[($numberOfArgs-1)][0] != '#'){
            fwrite(STDERR,"Chybny pocet operandov");
        return ReturnValue::PARSE_ERR;
        }
        $stats->comments++;
    }elseif ($words < $numberOfArgs){
        fwrite(STDERR,"Chybny pocet operandov");
        return ReturnValue::PARSE_ERR;
    }
}
}



# spracovanie argumentov a kontrola ci su spravne zadane, popr. v spravnej kombinacii
$first = true;
$helpEnable = false;
$statsEnable = false;
$stats = new STATS(0,0,0,0,"","");

foreach($argv as $argument){
    if ($first){
        $first = false;
        continue;
    }
    
    if (preg_match('~--help~u',$argument)){
       $helpEnable = true;
    }elseif (preg_match('~--stats=.*~u',$argument)){
        $statsEnable = true;
      
        $stats->fileName = preg_split('~=~',$argument);
    }elseif (preg_match('~--loc~u',$argument)){
        $stats->statsToPrint .= "loc ";
    }elseif (preg_match('~--comments~u',$argument)){
        $stats->statsToPrint .= "comments ";
    }elseif (preg_match('~--labels~u',$argument)){
        $stats->statsToPrint .= "labels ";
    }elseif (preg_match('~--jumps~u',$argument)){
        $stats->statsToPrint .= "jumps ";
    }
    else {
        fwrite(STDERR,"Chybne vstupne parametre");
        exit(ReturnValue::BAD_PARAMS);
    }

}
# vypis helpu a ukoncenie programu
if ($helpEnable){
    if ($statsEnable){
        fwrite(STDERR,"Help nemozno kombinovat s inymi parametrami");
        exit(ReturnValue::BAD_PARAMS);
    }
    print("Skript typu filtr (parse.php v jazyce PHP 7.4) načte ze standardního vstupu zdrojový kód v IPP-
    code20 (viz sekce 6), zkontroluje lexikální a syntaktickou správnost kódu a vypíše na standardní
    výstup XML reprezentaci programu.".PHP_EOL);
    exit(ReturnValue::SUCCESS);
}
if ((strlen($stats->statsToPrint)>1) && $statsEnable == false){
    fwrite(STDERR,"Chybne vstupne parametre");
    exit(ReturnValue::BAD_PARAMS);
}
$hlavicka = false;
$xw = xmlwriter_open_memory();
xmlwriter_set_indent($xw, 1);
$res = xmlwriter_set_indent_string($xw, ' ');

xmlwriter_start_document($xw, '1.0', 'utf-8');
xmlwriter_start_element($xw, 'program');
xmlwriter_start_attribute($xw, 'language');
xmlwriter_text($xw, 'IPPcode20');
xmlwriter_end_attribute($xw);
$counter=1;

while (($line =fgets(STDIN)) !== false){

    if (preg_match('~^\s*$~', $line)) {
        #prazdny riadok takze pokracuje
        continue;

    } elseif (preg_match('~^\s*#~u', $line)) {
        #komentar takze pokracuje
        $stats->comments++;
        continue;
    } elseif (!$hlavicka) {
        if (preg_match('~^\.IPPcode20\s*(#.*)?$~iu',$line)){
            #nasla sa hlavicka
            $hlavicka = true;
            continue;
        }else {
            fwrite(STDERR,"KOD NEZACINA .IPPcode20".PHP_EOL);
            exit(ReturnValue::BAD_HEADER);
        }
    }

    $stats->loc++;
    # rozdelenie riadku na slova
    $splitline = preg_split("~\s+~u",$line);
    
    # pocet slov na riadku prida "enter" za posledny riadok
    $numberOfWords = count($splitline);
    if ($splitline[($numberOfWords-1)] != ''){
        $numberOfWords++;
    }

    #da kod instrukcie na upper case kvoli jednoduchsej kontrole
    $OPcode = strtoupper($splitline[0]);
    switch ($OPcode){
        case "MOVE":

            $temp =  REGEXES::CheckARGS($stats,$numberOfWords,$splitline,4);
            if ($temp != 0){
                exit(ReturnValue::PARSE_ERR);
            }
            if (!preg_match('~'.REGEXES::VAR.'~ui',$splitline[1]) && !preg_match('~'.REGEXES::SYMB.'~ui',$splitline[2])){
                fwrite(STDERR,"Chybna lexika argumentov".PHP_EOL);
                exit(ReturnValue::PARSE_ERR);
            }
            $symb = preg_split("~@~u",$splitline[2]);
            xmlwriter_start_element($xw, 'instruction');
            xmlwriter_start_attribute($xw, 'order');
            xmlwriter_text($xw, $counter++);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_attribute($xw, 'opcode');
            xmlwriter_text($xw,'MOVE');
            xmlwriter_end_attribute($xw);
            xmlwriter_start_element($xw, 'arg1');
            xmlwriter_start_attribute($xw, 'type');
            xmlwriter_text($xw, 'var');
            xmlwriter_end_attribute($xw);
            xmlwriter_text($xw, $splitline[1]);
            xmlwriter_end_element($xw);
            xmlwriter_start_element($xw, 'arg2');
            xmlwriter_start_attribute($xw, 'type');
            if (strcasecmp($symb[0],"GF") == 0 || strcasecmp($symb[0],"LF") == 0 || strcasecmp($symb[0],"TF") == 0){
                xmlwriter_text($xw, 'var');
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $splitline[2]);
            } else {
                xmlwriter_text($xw,$symb[0]);
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $symb[1]);
            }
            xmlwriter_end_element($xw);
            xmlwriter_end_element($xw);
            break;
        
        
        case "CREATEFRAME":
        case "PUSHFRAME":   
        case "POPFRAME":        
            $temp = REGEXES::CheckARGS($stats,$numberOfWords,$splitline,2);
            if ($temp != 0){
                exit(ReturnValue::PARSE_ERR);
            }
            xmlwriter_start_element($xw, 'instruction');
            xmlwriter_start_attribute($xw, 'order');
            xmlwriter_text($xw, $counter++);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_attribute($xw, 'opcode');
            xmlwriter_text($xw,$splitline[0]);
            xmlwriter_end_attribute($xw);
            xmlwriter_end_element($xw);
            break;
        
        
        case "DEFVAR":
            $temp =REGEXES::CheckARGS($stats,$numberOfWords,$splitline,3);
            if ($temp != 0){
                exit(ReturnValue::PARSE_ERR);
            }

            if (!preg_match('~'.REGEXES::VAR.'~ui',$splitline[1])){
                fwrite(STDERR,"Chybny pocet operandov alebo lexika, alebo lexika, pouzite DEFVAR <var> \n".PHP_EOL);
                exit(ReturnValue::PARSE_ERR);
            }
            xmlwriter_start_element($xw, 'instruction');
            xmlwriter_start_attribute($xw, 'order');
            xmlwriter_text($xw, $counter++);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_attribute($xw, 'opcode');
            xmlwriter_text($xw,'DEFVAR');
            xmlwriter_end_attribute($xw);
            xmlwriter_start_element($xw, 'arg1');
            xmlwriter_start_attribute($xw, 'type');
            xmlwriter_text($xw, 'var');
            xmlwriter_end_attribute($xw);
            xmlwriter_text($xw, $splitline[1]);
            xmlwriter_end_element($xw);
            xmlwriter_end_element($xw);
            break;
        
        
        case "CALL":
            $stats->jumps++;
            $temp = REGEXES::CheckARGS($stats,$numberOfWords,$splitline,3);
            if ($temp != 0){
                exit(ReturnValue::PARSE_ERR);
            }

            if (!preg_match('~'.REGEXES::LABEL.'~ui',$splitline[1])){
                fwrite(STDERR,"Chybny pocet operandov alebo lexika, pouzite CALL <label> \n".PHP_EOL);
                exit(ReturnValue::PARSE_ERR);
            }
            xmlwriter_start_element($xw, 'instruction');
            xmlwriter_start_attribute($xw, 'order');
            xmlwriter_text($xw, $counter++);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_attribute($xw, 'opcode');
            xmlwriter_text($xw,'CALL');
            xmlwriter_end_attribute($xw);
            xmlwriter_start_element($xw, 'arg1');
            xmlwriter_start_attribute($xw, 'type');
            xmlwriter_text($xw, 'label');
            xmlwriter_end_attribute($xw);
            xmlwriter_text($xw, $splitline[1]);
            xmlwriter_end_element($xw);
            xmlwriter_end_element($xw);   
            break;
        
        
        case "RETURN":
            $stats->jumps++;
            
            $temp = REGEXES::CheckARGS($stats,$numberOfWords,$splitline,2);
            if ($temp != 0){
                exit(ReturnValue::PARSE_ERR);
            }

            xmlwriter_start_element($xw, 'instruction');
            xmlwriter_start_attribute($xw, 'order');
            xmlwriter_text($xw, $counter++);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_attribute($xw, 'opcode');
            xmlwriter_text($xw,$splitline[0]);
            xmlwriter_end_attribute($xw);
            xmlwriter_end_element($xw);
            break;
        
        
        case "PUSHS":
        case "WRITE":
        case "EXIT":
        case "DPRINT":

            $temp = REGEXES::CheckARGS($stats,$numberOfWords,$splitline,3);
            if ($temp != 0){
                exit(ReturnValue::PARSE_ERR);
            }

            if (!preg_match('~'.REGEXES::SYMB.'~ui',$splitline[1])){
                 fwrite(STDERR,"Chybny pocet operandov alebo lexika, pouzite PUSHs <symb> \n".PHP_EOL);
                 exit(ReturnValue::PARSE_ERR);
            }
            $symb = preg_split("~@~u",$splitline[1]);
            xmlwriter_start_element($xw, 'instruction');
            xmlwriter_start_attribute($xw, 'order');
            xmlwriter_text($xw, $counter++);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_attribute($xw, 'opcode');
            xmlwriter_text($xw,$splitline[0]);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_element($xw, 'arg1');
            xmlwriter_start_attribute($xw, 'type');
            if (strcasecmp($symb[0],"GF") == 0 || strcasecmp($symb[0],"LF") == 0 || strcasecmp($symb[0],"TF") == 0){
                xmlwriter_text($xw, 'var');
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $splitline[1]);
            } else {
                xmlwriter_text($xw,$symb[0]);
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $symb[1]);
            }
            xmlwriter_end_element($xw);
            xmlwriter_end_element($xw); 
            break;
        case "POPS":
            
            $temp = REGEXES::CheckARGS($stats,$numberOfWords,$splitline,3);
            if ($temp != 0){
                exit(ReturnValue::PARSE_ERR);
            }

            if (!preg_match('~'.REGEXES::VAR.'~ui',$splitline[1])){
                fwrite(STDERR,"Chybny pocet operandov alebo lexika, pouzite POPs >var> \n".PHP_EOL);
                exit(ReturnValue::PARSE_ERR);
            } 
            xmlwriter_start_element($xw, 'instruction');
            xmlwriter_start_attribute($xw, 'order');
            xmlwriter_text($xw, $counter++);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_attribute($xw, 'opcode');
            xmlwriter_text($xw,'POPS');
            xmlwriter_end_attribute($xw);
            xmlwriter_start_element($xw, 'arg1');
            xmlwriter_start_attribute($xw, 'type');
            xmlwriter_text($xw, 'var');
            xmlwriter_end_attribute($xw);
            xmlwriter_text($xw, $splitline[1]);
            xmlwriter_end_element($xw);
            xmlwriter_end_element($xw); 
            break;
        
        
        case "ADD":
        case "SUB":
        case "MUL":
        case "IDIV":
        case "LT":
        case "GT":
        case "EQ":
        case "AND":
        case "OR":
        case "STR2INT":
        case "CONCAT":
        case "GETCHAR":
        case "SETCHAR":
        
            $temp = REGEXES::CheckARGS($stats,$numberOfWords,$splitline,5);
            if ($temp != 0){
                exit(ReturnValue::PARSE_ERR);
            }

            if (!preg_match('~'.REGEXES::VAR.'~ui',$splitline[1]) && !preg_match('~'.REGEXES::SYMB.'~ui',$splitline[2]) && !preg_match('~'.REGEXES::SYMB.'~ui',$splitline[3])){
                fwrite(STDERR,"Chybny pocet operandov alebo lexika, pouzite INSTRUCTION <var> <symb1> <symb2> \n".PHP_EOL);
                exit(ReturnValue::PARSE_ERR);
            } 
            $symb = preg_split("~@~u",$splitline[2]);
            $symb2 = preg_split("~@~u",$splitline[3]);
            xmlwriter_start_element($xw, 'instruction');
            xmlwriter_start_attribute($xw, 'order');
            xmlwriter_text($xw, $counter++);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_attribute($xw, 'opcode');
            xmlwriter_text($xw,$splitline[0]);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_element($xw, 'arg1');
            xmlwriter_start_attribute($xw, 'type');
            xmlwriter_text($xw,'var');
            xmlwriter_end_attribute($xw);
            xmlwriter_text($xw, $splitline[1]);
            xmlwriter_end_element($xw);
            xmlwriter_start_element($xw, 'arg2');
            xmlwriter_start_attribute($xw, 'type');
            if (strcasecmp($symb[0],"GF") == 0 || strcasecmp($symb[0],"LF") == 0 || strcasecmp($symb[0],"TF") == 0){
                xmlwriter_text($xw, 'var');
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $splitline[1]);
            } else {
                xmlwriter_text($xw,$symb[0]);
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $symb[1]);
            }
            xmlwriter_end_element($xw);
            xmlwriter_start_element($xw, 'arg3');
            xmlwriter_start_attribute($xw, 'type');
            if (strcasecmp($symb2[0],"GF") == 0 || strcasecmp($symb2[0],"LF") == 0 || strcasecmp($symb2[0],"TF") == 0){
                xmlwriter_text($xw, 'var');
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $splitline[1]);
            } else {
                xmlwriter_text($xw,$symb2[0]);
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $symb2[1]);
            }
            xmlwriter_end_element($xw);
            xmlwriter_end_element($xw);
            break;
        
        
        case "NOT":
        case "INT2CHAR":
        case "TYPE":
        case "STRLEN":
        
            $temp = REGEXES::CheckARGS($stats,$numberOfWords,$splitline,4);
            if ($temp != 0){
                exit(ReturnValue::PARSE_ERR);
            }

            if (!preg_match('~'.REGEXES::VAR.'~ui',$splitline[1]) && !preg_match('~'.REGEXES::SYMB.'~ui',$splitline[2])){
                fwrite(STDERR,"Chybny pocet operandov alebo lexika, pouzite NOT <var> <symb1> ".PHP_EOL);
                exit(ReturnValue::PARSE_ERR);
            }
            $symb = preg_split("~@~u",$splitline[2]);
            xmlwriter_start_element($xw, 'instruction');
            xmlwriter_start_attribute($xw, 'order');
            xmlwriter_text($xw, $counter++);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_attribute($xw, 'opcode');
            xmlwriter_text($xw,'PUSHS');
            xmlwriter_end_attribute($xw);
            xmlwriter_start_element($xw, 'arg1');
            xmlwriter_start_attribute($xw, 'type');
            xmlwriter_text($xw,'var');
            xmlwriter_end_attribute($xw);
            xmlwriter_text($xw, $splitline[1]);
            xmlwriter_end_element($xw);
            xmlwriter_start_element($xw, 'arg2');
            xmlwriter_start_attribute($xw, 'type');
            if (strcasecmp($symb[0],"GF") == 0 || strcasecmp($symb[0],"LF") == 0 || strcasecmp($symb[0],"TF") == 0){
                xmlwriter_text($xw, 'var');
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $splitline[1]);
            } else {
                xmlwriter_text($xw,$symb[0]);
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $symb[1]);
            }
            xmlwriter_end_element($xw);
            xmlwriter_end_element($xw);
            break;
        
        
        case "READ":
            
            $temp = REGEXES::CheckARGS($stats,$numberOfWords,$splitline,4);
            if ($temp != 0){
                exit(ReturnValue::PARSE_ERR);
            }

            if (!preg_match('~'.REGEXES::VAR.'~ui',$splitline[1]) && !preg_match('~'.REGEXES::TYPE.'~ui',$splitline[2])){
                fwrite(STDERR,"Chybny pocet operandov alebo lexika, pouzite NOT <var> <type> ".PHP_EOL);
                exit(ReturnValue::PARSE_ERR);
            }
            xmlwriter_start_element($xw, 'instruction');
            xmlwriter_start_attribute($xw, 'order');
            xmlwriter_text($xw, $counter++);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_attribute($xw, 'opcode');
            xmlwriter_text($xw,'READ');
            xmlwriter_end_attribute($xw);
            xmlwriter_start_element($xw, 'arg1');
            xmlwriter_start_attribute($xw, 'type');
            xmlwriter_text($xw, 'var');
            xmlwriter_end_attribute($xw);
            xmlwriter_text($xw, $splitline[1]);
            xmlwriter_end_element($xw);
            xmlwriter_start_element($xw, 'arg2');
            xmlwriter_start_attribute($xw, 'type');
            xmlwriter_text($xw, 'type');
            xmlwriter_end_attribute($xw);
            xmlwriter_text($xw, $splitline[2]);
            xmlwriter_end_element($xw);
            xmlwriter_end_element($xw); 
            break;           

        
        
        case "LABEL":
        case "JUMP":
            
            $temp = REGEXES::CheckARGS($stats,$numberOfWords,$splitline,3);
            if ($temp != 0){
                exit(ReturnValue::PARSE_ERR);
            }

            if (!preg_match('~'.REGEXES::LABEL.'~ui',$splitline[1])){
                fwrite(STDERR,"Chybny pocet operandov alebo lexika, pouzite LABEL/JUMP <label>".PHP_EOL);
                exit(ReturnValue::PARSE_ERR);
            }
            if (preg_match('~JUMP~u',$splitline[1])){
                $stats->jumps++;
            }else{
                $stats->labels++;
            }
            xmlwriter_start_element($xw, 'instruction');
            xmlwriter_start_attribute($xw, 'order');
            xmlwriter_text($xw, $counter++);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_attribute($xw, 'opcode');
            xmlwriter_text($xw,$splitline[0]);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_element($xw, 'arg1');
            xmlwriter_start_attribute($xw, 'type');
            xmlwriter_text($xw, 'label');
            xmlwriter_end_attribute($xw);
            xmlwriter_text($xw, $splitline[1]);
            xmlwriter_end_element($xw);
            xmlwriter_end_element($xw); 
            break;
        
        
        case "JUMPIFEQ":
        case "JUMPIFNEQ":
            $stats->jumps++;

            $temp = REGEXES::CheckARGS($stats,$numberOfWords,$splitline,5);
            if ($temp != 0){
                exit(ReturnValue::PARSE_ERR);
            }

            if (!preg_match('~'.REGEXES::LABEL.'~ui',$splitline[1]) && !preg_match('~'.REGEXES::SYMB.'~ui',$splitline[2]) && !preg_match('~'.REGEXES::SYMB.'~ui',$splitline[3])){
                fwrite(STDERR,"Chybny pocet operandov alebo lexika, pouzite JUMPIFEQ/NE <label> <symb1> <symb2> \n".PHP_EOL);
                exit(ReturnValue::PARSE_ERR);
            }
            $symb = preg_split("~@~u",$splitline[2]);
            $symb2 = preg_split("~@~u",$splitline[3]);
            xmlwriter_start_element($xw, 'instruction');
            xmlwriter_start_attribute($xw, 'order');
            xmlwriter_text($xw, $counter++);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_attribute($xw, 'opcode');
            xmlwriter_text($xw,$splitline[0]);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_element($xw, 'arg1');
            xmlwriter_start_attribute($xw, 'type');
            xmlwriter_text($xw,'label');
            xmlwriter_end_attribute($xw);
            xmlwriter_text($xw, $splitline[1]);
            xmlwriter_end_element($xw);
            xmlwriter_start_element($xw, 'arg2');
            xmlwriter_start_attribute($xw, 'type');
            if (strcasecmp($symb[0],"GF") == 0 || strcasecmp($symb[0],"LF") == 0 || strcasecmp($symb[0],"TF") == 0){
                xmlwriter_text($xw, 'var');
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $splitline[2]);
            } else {
                xmlwriter_text($xw,$symb[0]);
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $symb[1]);
            }
            xmlwriter_end_element($xw);
            xmlwriter_start_element($xw, 'arg3');
            xmlwriter_start_attribute($xw, 'type');
            if (strcasecmp($symb2[0],"GF") == 0 || strcasecmp($symb2[0],"LF") == 0 || strcasecmp($symb2[0],"TF") == 0){
                xmlwriter_text($xw, 'var');
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $splitline[1]);
            } else {
                xmlwriter_text($xw,$symb2[0]);
                xmlwriter_end_attribute($xw);
                xmlwriter_text($xw, $symb2[1]);
            }
            xmlwriter_end_element($xw);
            xmlwriter_end_element($xw);
            break;
 
        
        
        case "BREAK":
            
            $temp = REGEXES::CheckARGS($stats,$numberOfWords,$splitline,2);
            if ($temp != 0){
                exit(ReturnValue::PARSE_ERR);
            }

            xmlwriter_start_element($xw, 'instruction');
            xmlwriter_start_attribute($xw, 'order');
            xmlwriter_text($xw, $counter++);
            xmlwriter_end_attribute($xw);
            xmlwriter_start_attribute($xw, 'opcode');
            xmlwriter_text($xw,'BREAK');
            xmlwriter_end_attribute($xw);
            xmlwriter_end_element($xw); 
            break;
        
        
        default:
               fwrite(STDERR, "Neexistujuci kod \n");
               exit(ReturnValue::BAD_OPCODE);
    }   
}
#dopise koniec XML suboru a vytlaci to na STDOUT
xmlwriter_end_element($xw); 
xmlwriter_end_document($xw);
echo xmlwriter_output_memory($xw);

#zapis rozsirenia do zadaneho suboru
if ($statsEnable){

    $myfile = fopen($stats->fileName[1], "w");
    $vypis = preg_split('~ ~u',$stats->statsToPrint);
    foreach ($vypis as $ToPrint){
        if (strcmp("comments",$ToPrint) == 0){
            fwrite($myfile,$stats->comments.PHP_EOL);
        }elseif (strcmp("loc",$ToPrint) ==0){
            fwrite($myfile,$stats->loc.PHP_EOL);
        }elseif (strcmp("labels",$ToPrint) == 0){
            fwrite($myfile,$stats->labels.PHP_EOL);
        }elseif (strcmp("jumps",$ToPrint) == 0){
            fwrite($myfile,$stats->jumps.PHP_EOL);
        }
    
}
fclose($myfile);    
}
?>