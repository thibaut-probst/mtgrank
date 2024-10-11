# MTGRank
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)  
---  
A Magic: The Gathering format archetype ranking tool based on TOP 8 tournaments results. Ranking is based on summing points obtained of TOP 8 archetypes in tournaments. Points are determined by position in TOP 8 and number of players of the event.

## Features

* Support of [MTGTOP8](https://mtgtop8.com).
* Possibility to pass the format as an option or to discover it and select it via interactive mode.
* Support of 2 ranking algorithms:
    * Linear: each TOP8 member gets ( (9-n) * nb_players / 8 ) pts, where n is the rank;
    * Exponential: TOP1 gets (8 * nb_players / 8) pts, TOP2 gets (4 * nb_players / 8) pts, TOP3-4 get (2 * nb_players / 8) pts, TOP5-8 get (1 * nb_players / 8) pts
* Support of 4 possible time ranges options for analysis: last 2 weeks, last 2 months, since beginning of the year or since specific date.
* Possibility to select paper only events or online only events or both.
* Progress bar during tool execution.

## Requirements

Make sure you have [Python 3.10 or higher](https://www.python.org/downloads/) and [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) installed.  

## Installation 

#### Clone the repository to your working directory 
```
$ git clone https://github.com/thibaut-probst/mtgrank.git
$ cd mtgrank/
```
#### Install the dependencies
```
$ pip install -r requirements.txt
```

## Usage 

You can display ***MTGRank*** startup parameters information by using the --help argument: 

```
$ python3 mtgrank.py -h
usage: mtgrank.py [-h] [--format FORMAT] [--algorithm ALGORITHM] [--top TOP] [--date] [--paper | --online]

options:
  -h, --help            show this help message and exit
  --format FORMAT, -f FORMAT
                        The format to analyze (default: interactive mode)
  --algorithm ALGORITHM, -a ALGORITHM
                        Ranking algorithm (default: exponential):
                            Linear: each TOP8 member gets ( (9-n) * nb_players / 8 ) pts, where n is the rank; or
                            Exponential: TOP1 gets (8 * nb_players / 8) pts, TOP2 gets (4 * nb_players / 8) pts, TOP3-4 get (2 * nb_players / 8) pts, TOP5-8 get (1 * nb_players / 8) pts
  --top TOP, -t TOP     TOP ranking size (default: 20)
  --date, -d            Time range to be specified through a selection menu (default: last 2 weeks)
  --paper, -p           Only analyze paper events
  --online, -o          Only analyze online events
```

## Examples
```
$ python mtgrank.py -f LE 

TOP 20 Le archetypes over the last 2 weeks based on MTGTOP8 for both paper and online events and using exponential ranking algorithm

1 - Reanimator - 794 pts - 82 times TOP8
2 - Dragon Stompy - 484 pts - 26 times TOP8
3 - Dimir Tempo - 374 pts - 36 times TOP8
4 - Eldrazi Aggro - 337 pts - 37 times TOP8
5 - Painter - 265 pts - 23 times TOP8
6 - Other - Combo - 188 pts - 4 times TOP8
7 - Cradle Control - 166 pts - 14 times TOP8
8 - UWx Control - 152 pts - 17 times TOP8
9 - Cephalid Breakfast - 150 pts - 19 times TOP8
10 - Doomsday - 131 pts - 15 times TOP8
11 - Nadu - 124 pts - 11 times TOP8
12 - Grixis Aggro - 116 pts - 15 times TOP8
13 - Mystic Forge - 73 pts - 9 times TOP8
14 - BUG Control - 66 pts - 9 times TOP8
15 - 4/5c Control - 66 pts - 7 times TOP8
16 - Stiflenought - 60 pts - 9 times TOP8
17 - Patriot Aggro - 52 pts - 6 times TOP8
18 - Storm - 51 pts - 6 times TOP8
19 - Mono Red Combo - 50 pts - 4 times TOP8
20 - Cloudpost Ramp - 47 pts - 10 times TOP8
```
```
$ python mtgrank.py -f DC -t 30

TOP 30 EDH archetypes over the last 2 weeks based on MTGTOP8 for both paper and online events and using exponential ranking algorithm

1 - Aragorn, King Of Gondor - 187 pts - 21 times TOP8
2 - Phelia, Exuberant Shepherd - 165 pts - 15 times TOP8
3 - Slimefoot And Squee - 160 pts - 23 times TOP8
4 - Partner WR - 147 pts - 16 times TOP8
5 - Ertai Resurrected - 142 pts - 7 times TOP8
6 - Tamiyo, Inquisitive Student - 127 pts - 14 times TOP8
7 - Tivit, Seller Of Secrets - 104 pts - 8 times TOP8
8 - Atraxa, Grand Unifier - 102 pts - 10 times TOP8
9 - Phlage, Titan Of Fire's Fury - 85 pts - 8 times TOP8
10 - Satya, Aetherflux Genius - 69 pts - 8 times TOP8
11 - Light-Paws, Emperor's Voice - 67 pts - 8 times TOP8
12 - Partner WUBR - 64 pts - 3 times TOP8
13 - Aminatou, the Fateshifter - 51 pts - 8 times TOP8
14 - Amalia Benavides Aguirre - 41 pts - 8 times TOP8
15 - Norin, Swift Survivalist - 39 pts - 7 times TOP8
16 - Elminster - 32 pts - 2 times TOP8
17 - Grist, The Hunger Tide - 30 pts - 6 times TOP8
18 - Partner WRG - 30 pts - 3 times TOP8
19 - Flamewar, Brash Veteran - 28 pts - 2 times TOP8
20 - Esika, God Of The Tree - 24 pts - 2 times TOP8
21 - Feldon, Ronom Excavator - 21 pts - 5 times TOP8
22 - Ezio Auditore da Firenze - 20 pts - 3 times TOP8
23 - Old Rutstein - 20 pts - 3 times TOP8
24 - Glarb, Calamity's Augur - 18 pts - 2 times TOP8
25 - Marchesa, Dealer of Death - 16 pts - 2 times TOP8
26 - Juri, Master Of The Revue - 16 pts - 2 times TOP8
27 - Niv-Mizzet Reborn - 16 pts - 3 times TOP8
28 - Kasla, the Broken Halo - 16 pts - 1 times TOP8
29 - Sheoldred, the Apocalypse - 14 pts - 3 times TOP8
30 - Azusa, Lost But Seeking - 13 pts - 3 times TOP8
```
```
$ python mtgrank.py -f DC -d -t 30
Select time range:
        1 Last 2 weeks
        2 Last 2 months
        3 Since the beginning of the year
        4 Since a specific date
 [1/2/3/4]: 4
Enter date (dd-mm-yyyy):
: 14-06-2024

TOP 30 EDH archetypes since 14-06-2024 based on MTGTOP8 for both paper and online events and using exponential ranking algorithm

1 - Tamiyo, Inquisitive Student - 2748 pts - 181 times TOP8
2 - Slimefoot And Squee - 2274 pts - 178 times TOP8
3 - Aragorn, King Of Gondor - 1190 pts - 121 times TOP8
4 - Partner WR - 1169 pts - 124 times TOP8
5 - Phelia, Exuberant Shepherd - 954 pts - 101 times TOP8
6 - Feldon, Ronom Excavator - 908 pts - 103 times TOP8
7 - Satya, Aetherflux Genius - 826 pts - 95 times TOP8
8 - Phlage, Titan Of Fire's Fury - 715 pts - 60 times TOP8
9 - Atraxa, Grand Unifier - 698 pts - 71 times TOP8
10 - Nadu, Winged Wisdom - 673 pts - 33 times TOP8
11 - Azusa, Lost But Seeking - 464 pts - 49 times TOP8
12 - Ertai Resurrected - 448 pts - 42 times TOP8
13 - Tivit, Seller Of Secrets - 424 pts - 30 times TOP8
14 - Marchesa, Dealer of Death - 422 pts - 38 times TOP8
15 - Grist, The Hunger Tide - 414 pts - 39 times TOP8
16 - Flamewar, Brash Veteran - 371 pts - 23 times TOP8
17 - Light-Paws, Emperor's Voice - 348 pts - 34 times TOP8
18 - Amalia Benavides Aguirre - 306 pts - 27 times TOP8
19 - Sheoldred, the Apocalypse - 267 pts - 25 times TOP8
20 - Aminatou, the Fateshifter - 257 pts - 37 times TOP8
21 - The Gitrog Monster - 225 pts - 9 times TOP8
22 - Niv-Mizzet Reborn - 206 pts - 19 times TOP8
23 - Hidetsugu And Kairi - 205 pts - 12 times TOP8
24 - Dennick, Pious Apprentice - 191 pts - 22 times TOP8
25 - Ghyrson Starn, Kelermorph - 185 pts - 35 times TOP8
26 - Juri, Master Of The Revue - 183 pts - 20 times TOP8
27 - Old Stickfingers - 179 pts - 10 times TOP8
28 - Partner WRG - 171 pts - 20 times TOP8
29 - Partner WUBG - 171 pts - 17 times TOP8
30 - Leovold, Emissary of Trest - 168 pts - 12 times TOP8
```