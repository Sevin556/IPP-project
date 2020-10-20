 #  Implementační dokumentace k 1. úloze do IPP 2019/2020 
##  Jméno a příjmení: Ivan Halomi 
##  Login: xHalom00 

## Návrh 
Parser spracuje argumenty, poprípadne vypíše *help* alebo chybu *č. 10*. Začne načítavať vstup zo **STDIN** po riadkoch a tie sa následne spracujú (prázdny riadok, komentár, hlavička) alebo rozparsujú na slová a posunú do *swtichu*, kde sa hľadá či prvé slovo v riadku vyhovuje niektorej z inštrukcií **IPPCODE20**, inštrukcie sú rozdelené do skupín s rovnakými vlastnosťami, kvôli prehladnosti kódu. Následne sa skontroluje správny počet argumentov a ich lexikálnu správnosť. Na výpis do XML formátu som zvolil XMLwriter, ktorý zapisuje do pamäte a v prípade, že nepríde k žiadnej chybe tak pred koncom *parse.php* sa vypíše na **STDOUT**.

### Triedy
V programe mám tri triedy *ReturnValues*, kde sú uložené chybové kódy, *REGEXES*, ktoré majú uložené jednotlivé regulárne výrazy pre argumenty inštrukcií a bola vytvorená pre zúhľadnenie kódu, takisto obsahuje funkciu na kontrolu správneho počtu argumentov a tretia trieda *Stats* pre rozšírenie.


### Rozšírenia 
Rozšírenie **STATS** je implementované a funguje nasledovne:
Argumenty sa ukladajú do stringu a počas behu programu sa zbierajú štatistky o všetkom. Na konci programu sa vypíšu len požadované štatistiky v poradí v akom sú uložené v stringu( konvertovanom na pole).

### Nedostatky 
Program nedokáže rozpoznať komentár, ktorý začína priamo za argumentom inštrukcie( var#komentár ukončí program s chybou 23).