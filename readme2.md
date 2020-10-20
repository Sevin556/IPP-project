 # <p style="text-align:center"> Implementační dokumentace k 2. úloze do IPP 2019/2020 </p>
##  <p style="text-align:center"> Jméno a příjmení: Ivan Halomi </p>
##  <p style="text-align:center"> Login: xHalom00 </p>

# <p style="text-align:center"> Interpret </p>
## Návrh a rozdelenie
Interpret je rozdelený na dva súbory, *interpret.py*, kde prebehne spracovanie argumentov a zavolanie adekvátnej triedovej funkcie z druhého súboru *parsing.py* alebo vypísanie pri parametri **--help**.Súbor *parsing.py* implementuje triedy **ReturnValue**, kde sú návratové hodnoty pre chybpvé kódy, triedu **notDefined** a triedu **interprets**. 

### Trieda notDefined:
slúži na inicializáciu premennej v inštrukcii *DEFVAR*, pri pokuse o čítanie takejto premennej nastane chyba 56(výnimka pri inštrukcii *TYPE*, kde sa vráti typ ako "")
### Trieda interprets:
Sú v nej uložené lable a ich čísla riadkov, rámce s premennými(implementované ako zásobník slovníkov), returnStack pre návrat po volaní funkcií, aktuálny riadok( jedna inštrukcia = 1 riadok)  
#### Funkcie triedy interprets : 
+ **BOTHGiven,INPUTGiven,XMLGiven:**sú volané z *interpret.py* a načítajú vstupné súbory(alebo STDIN), rozparsujú XML na inštrukcie pomocou funkcie *getroot/fromstring* z knižnice **xml.etree.ElementTree**, vyhladajú sa *lable* pomocou **FindLabels** a inštrukcie sú v nekonečnom cykle posielané do **OrderArgs**  
+ **FindLabel:** prejde všetky inštrukcie a nájde v nich *lable*, ktorých číslo riadku uloží do slovníka *labels*  
+ **OrderArgs:** zoradí argumenty do správneho poradia a pošle ich do **DoInstruction**  
+ **DoInstruction:** kontroluje či daný OPCode je nejaká inštrukcia a postará sa o následné vykonanie danej inštrukcie  
+ **CheckVar:** skontroluje či sa daná premenná nachádza v zadanom rámci a vráti jej hodnotu a typ  
+ **CheckType:** zistí či nejde o premennú (zavolá **CheckVar**) alebo vráti hodnotu a typ zadanej hodnoty  
+ **SaveToVar:** skontroluje existenciu premennej v danom rámci a uloží do nej zadanú hodnotu  
+ **DoOperation:** načíta hodnoty, skontroluje a vykoná zadanú matematickú/logickú operáciu a vráti výsledok  
+ **FunctionCycle:** je volaná inštrukciou *CALL* a vytvorí cyklus od zadaného *labelu* až do konca inštrukcií alebo inštrukcie *RETURN*, ktorá sa vráti na riadok uložený na vrchnej pozícii v *returnStack*  


# <p style="text-align:center"> TEST </p>

## Návrh 
Využíva dve triedy **Params**, do ktorej sa načítajú spracované argumenty  a **ReturnValue**, kde sú uložené návratové hodnoty chýb. Po spracovaní argumentov sa dostaneme k samotnému riešeniu prechádzania súborov či priečinkov. Funkcia **CheckDirectory** prechádza zadaný priečinok a hľadá priečinky, do ktorých vstupuje (ak je zadané --recursive) rekurzívnym volaním samej seba, ďalej hľadá súbory s koncovkou ".src" z ktorých zistí meno a nájde, poprípadne dogeneruje ostatné súbory (.in;.out;.rc). S nájdeným *src* súborom pokračuje k samotnému testovaniu, ktoré je založené na niekoľkých podmienkach (prišlo mi to lepšie riešenie ako vytvárať funkciu pre --interpret/parse-only či obe zvlášť), testovací skript vytvorí premennú s cestou k parse/interpret, .src a .in súboru , presmerovaním výstupu do súboru s rovnakým menom ako testovaný súbor no predponou 'My'(pre parse) alebo 'MyFinal'(pre interpret). Návratový kód je získaný pomocom ";echo $?" na konci premennej, ktorá je následne pomocou funkcie **shell_exec** vykonaná.
*Ukážka vytvorenia a spustenia premennej:*
```php
$temp ="php7.4 $params->parseFile <$directoryName/$file >$directoryName/My$nameOfFile.out; echo $?";
$ReturnCode = shell_exec("$temp");
```
Testovanie konkrétneho súboru končí chybným návratovým kódom alebo po porovnaní .out súborov ak bol návratový kód 0.
## HTML výstup
Výsledky testovania sú "tlačené" na STDOUT hneď po dokončení každého testu. Formát tabuľky som zvolil, pretože mi to príde prehľadné a na prvý pohľad je vidno, ktorý test neuspel v ktorom bode. Tabuľka pozostáva z 5tich stĺpcov(meno testu,úspech/neúspech,správny kód, vrátený kód a či sa output zhoduje),stĺpce boli zvolené takto pretože som sám pri testovaní zistil, že je vhodné hneď vidieť, kde nastala chyba a nie len či test prešiel alebo nie.Neúspech testu vidieť na prvý pohľad farebnou zmenou pozadia stĺpca *úspech/neúspech* a stĺpca, kde chyba nastala ( zlá navratová hodnota alebo rozdielne outputy).
