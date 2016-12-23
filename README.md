#VU CHF Poblikacijų Rinkimo Programa

> Programa skirta Vilniaus Universiteto Chemijos fakultetui.
> Ši programa yra skirta statistikos rinkimui apie VU Chemijos fakultete
> dirbančių dėstytojų ir mokslininkų publikuotus mokslinius darbus.

##Programos veikimas

**Programa atlieka sekančius veiksmus:**
- Nuskaito XML failą su jame pateiktais:
    - Eilės numeriu;
    - Publikacijos aprašymu.
- Pagal nuskaitytus duomenis programa suranda ir suskaičiuoja 
    mokslinės publikacijos IF* ir AIF** rodiklius.
- Programa surinktus duomenis atspausdina į Excel failą, kurį išsaugo
    Jūsų kompiuterio darbalaukyje.
    
    
**IF** (*angl.* Impact Factor) - TODO
  
**AIF** (*angl.* Average Impact Factor) - TODO

**Korektiškam programos veikimui reikalingas interneto ryšys.**

##Programos įrašymas
   
- Išskelidus .zip ar kitokio tipo archyvą papildomų veiksmų atlikti nereikia.
- Išskleistoje direktorijoje reikia rasti dokumentą extractor.exe ir jį paspausti du kartus.

>_Norint, programą iškviesti iš jūsų darbalaukio tam reikėtų susikurti "shortcut" nuorodą.
>Ją kuriame paspaudę dešinį pelytės klavišą savo darbalaukyje:_

- New;
- Schrotcut;

##Duomenų programai apipavidalinimas

**Programos korektiškam veikimui būtina paduoti reikiamai formatuotą XML dokumentą žemiau pateikta forma:**

```sh
<root>
    <row count="1" text="[publikacijos anotacija]"></row>
    <row count="2" text="[publikacijos anotacija]"></row>
    ...
</root>
```

`Excel`
**Norint sukurti šį dokumentą reikia atlikti sekančius žingsnius:**

>1. `Word` dokumentą kuriame yra visos publikacijos reikia išsaugoti `Plain Text` formatu
>    - Išsaugojimo dialoge reikia pasirinkti šiuos parametrus
>        - "Other encoding" -> `Western European (Windows)`
>        - "End lines with" -> `CR / LF`
>        - "Allow character substitution" -> `True`  
>2. Iš `Plain Text` formato dokumento viską nukopijuojame į `Excel` programą
>3. `Excel` programoje atliekame teksto formatavimo žingsnius
>    - Paliekame tik tuos langelius kuriuose yra publikacija arba/ir jos numeris - kitus šaliname
>    - Kai kuriais atvejais publikacijos aprašas gali būti "išmėtytas" per du langelius, tokiu atveju publikacijos aprašą reiktų "sujungti" ir patalpinti į vieną langelį
>4. Sutvarkius formatavimą pažymimę visą stulpelį ir jį filtruojame `Data -> Filter` filtre nurodome filtravimo tvarką `Sort Largest to smallest`
>5. Altikus filtravimą tekstinę dalį kopijuojame į naują `Sheet'ą` į langelį `B2`
>6. Pradedant langelyje `A2` sunumeruojame visas publikacijas, galutinis variantas turi atrodyti taip:
>       ```sh
>           1 [publikacijos anotacija]
>           2 [publikacijos anotacija]
>           ...
>7. [...]

        


##Programos '*stand-alone*' versijos kompiliavimas

```sh
$ pyinstaller --hidden-import lxml --hidden-import html5lib main.py
```
