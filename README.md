# MTGRank
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue)  
---  
A Magic: The Gathering format archetype ranking tool based on TOP 8 tournaments results. Ranking is based on summing points obtained of TOP 8 archetypes in tournaments. Points are determined by position in TOP 8 and number of players of the event.

## Features

* Support of [MTGTOP8](https://mtgtop8.com), [MTGDECKS](https://mtgdecks.net) and [MTGGOLDFISH](https://www.mtggoldfish.com) as tournament data sources.
* Support of 3 formats: Modern, Legacy and Pioneer.
* Support of 2 ranking algorithms:
    * Linear: each TOP8 member gets ( (9-n) * nb_players / 8 ) pts, where n is the rank;
    * Exponential: TOP1 gets (8 * nb_players / 8) pts, TOP2 gets (4 * nb_players / 8) pts, TOP3-4 get (2 * nb_players / 8) pts, TOP5-8 get (1 * nb_players / 8) pts
* Support of 4 possible time ranges options for analysis: last 2 weeks, last 2 months, since beginning of the year or since specific date.
* Support of selection of paper only events or online only events or both.
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
usage: mtgrank.py [-h] [--source SOURCE] [--format FORMAT] [--algorithm ALGORITHM] [--top TOP] [--date] [--paper | --online]

options:
  -h, --help            show this help message and exit
  --source SOURCE, -s SOURCE
                        Data source to use (mtgtop8, mtgdecks, mtggoldfish ; default: mtgtop8)
  --format FORMAT, -f FORMAT
                        Format (modern, legacy, pioneer ; default: modern)
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
$ python3 mtgrank.py 

TOP 20 Modern archetypes over the last 2 weeks based on MTGTOP8 for both paper and online events and using exponential ranking algorithm

1 - Rakdos - 904 pts - 67 times TOP8
2 - Amulet Titan - 769 pts - 17 times TOP8
3 - Yawgmoth Evolution - 468 pts - 21 times TOP8
4 - Tron - 433 pts - 27 times TOP8
5 - 4cc - 391 pts - 44 times TOP8
6 - UR Murktide - 250 pts - 29 times TOP8
7 - Living End - 230 pts - 30 times TOP8
8 - Burn - 192 pts - 17 times TOP8
9 - Hammer Time - 183 pts - 23 times TOP8
10 - Creativity - 177 pts - 24 times TOP8
11 - Mono Black Control - 158 pts - 12 times TOP8
12 - RDW - 106 pts - 7 times TOP8
13 - Grixis Death's Shadow - 83 pts - 18 times TOP8
14 - Breach - 73 pts - 12 times TOP8
15 - The Underworld Cookbook - 56 pts - 7 times TOP8
16 - Hardened Scales - 49 pts - 5 times TOP8
17 - Cascade Crash - 45 pts - 17 times TOP8
18 - Urza - 42 pts - 2 times TOP8
19 - 5c Domain - 40 pts - 1 times TOP8
20 - Trash for Treasure - 33 pts - 5 times TOP8
```
```
$ python3 mtgrank.py -s mtggoldfish -d
Select time range:
        1 Last 2 weeks
        2 Last 2 months
        3 Since beginning of the year
        4 Since specific date
 [1/2/3/4]: 2

TOP 20 Modern archetypes over the last 2 months based on MTGGOLDFISH for both paper and online events and using exponential ranking algorithm

1 - 4cc - 1304 pts - 86 times TOP8
2 - Rakdos - 1294 pts - 115 times TOP8
3 - Creativity - 1215 pts - 101 times TOP8
4 - UR Murktide - 1021 pts - 95 times TOP8
5 - Living End - 871 pts - 71 times TOP8
6 - Amulet Titan - 868 pts - 30 times TOP8
7 - Tron - 790 pts - 52 times TOP8
8 - Yawgmoth Evolution - 552 pts - 48 times TOP8
9 - Hammer Time - 541 pts - 53 times TOP8
10 - Burn - 442 pts - 49 times TOP8
11 - Grixis Death's Shadow - 306 pts - 29 times TOP8
12 - Crashing Footfalls - 250 pts - 45 times TOP8
13 - Temur Cascade - 223 pts - 9 times TOP8
14 - Jund - 186 pts - 9 times TOP8
15 - Generic Ragavan - 184 pts - 28 times TOP8
16 - Four-color Midrange - 172 pts - 4 times TOP8
17 - All Other Decklists - 170 pts - 5 times TOP8
18 - Lantern - 150 pts - 7 times TOP8
19 - Domain Zoo - 138 pts - 21 times TOP8
20 - Mill - 132 pts - 11 times TOP8
```
```
$ python3 mtgrank.py -f legacy -a linear -t 10

TOP 10 Legacy archetypes over the last 2 weeks based on MTGTOP8 for both paper and online events and using linear ranking algorithm

1 - Grixis Death's Shadow - 764 pts - 36 times TOP8
2 - Reanimator - 502 pts - 16 times TOP8
3 - Grixis Delver - 368 pts - 28 times TOP8
4 - Painter - 312 pts - 20 times TOP8
5 - 4cc - 247 pts - 8 times TOP8
6 - 8-Cast - 228 pts - 4 times TOP8
7 - Lands - 221 pts - 13 times TOP8
8 - Initiative Stompy - 204 pts - 10 times TOP8
9 - Sneak Show - 161 pts - 4 times TOP8
10 - Cradle Control - 159 pts - 5 times TOP8
```
```
$ python3 mtgrank.py -f pioneer -s mtgdecks

TOP 20 Pioneer archetypes over the last 2 weeks based on MTGDECKS for both paper and online events and using exponential ranking algorithm

1 - Rakdos - 511 pts - 73 times TOP8
2 - Green Devotion - 411 pts - 54 times TOP8
3 - Azorius Spirits - 261 pts - 16 times TOP8
4 - Mono White Humans - 190 pts - 20 times TOP8
5 - Creativity - 169 pts - 26 times TOP8
6 - Azorius Control - 134 pts - 23 times TOP8
7 - Mono-White Humans - 129 pts - 5 times TOP8
8 - Boros Convoke - 108 pts - 11 times TOP8
9 - Atarka Red - 106 pts - 3 times TOP8
10 - Enigmatic Incarnatio... - 94 pts - 8 times TOP8
11 - BR Aggro - 93 pts - 11 times TOP8
12 - WU Control - 75 pts - 8 times TOP8
13 - Red Deck Wins - 69 pts - 6 times TOP8
14 - Gruul Vehicles - 69 pts - 6 times TOP8
15 - Gruul Aggro - 65 pts - 5 times TOP8
16 - Boros Prowess - 48 pts - 15 times TOP8
17 - Uw Lotus Field Contr... - 48 pts - 1 times TOP8
18 - Mono green  - 48 pts - 1 times TOP8
19 - Five-color Niv-Mizze... - 48 pts - 1 times TOP8
20 - Abzan Greasefang - 47 pts - 11 times TOP8
```
```
$ python3 mtgrank.py -d 
Select time range:
        1 Last 2 weeks
        2 Last 2 months
        3 Since beginning of the year
        4 Since specific date
 [1/2/3/4]: 4
Enter date (dd-mm-yyyy):
: 23-06-2023

TOP 20 Modern archetypes since 23-06-2023 based on MTGTOP8 for both paper and online events and using exponential ranking algorithm

1 - 4cc - 1489 pts - 102 times TOP8
2 - Rakdos - 1350 pts - 109 times TOP8
3 - Amulet Titan - 902 pts - 38 times TOP8
4 - Living End - 889 pts - 72 times TOP8
5 - Creativity - 765 pts - 60 times TOP8
6 - Yawgmoth Evolution - 750 pts - 39 times TOP8
7 - UR Murktide - 637 pts - 69 times TOP8
8 - Tron - 622 pts - 55 times TOP8
9 - Hammer Time - 596 pts - 52 times TOP8
10 - Burn - 293 pts - 35 times TOP8
11 - Cascade Crash - 235 pts - 32 times TOP8
12 - Grixis Death's Shadow - 207 pts - 33 times TOP8
13 - Temur Cascade - 196 pts - 9 times TOP8
14 - Mono Black Control - 174 pts - 16 times TOP8
15 - Breach - 138 pts - 29 times TOP8
16 - RDW - 108 pts - 8 times TOP8
17 - UW Control - 94 pts - 17 times TOP8
18 - UR Aggro - 78 pts - 5 times TOP8
19 - 4/5c Aggro - 77 pts - 10 times TOP8
20 - Merfolk - 76 pts - 17 times TOP8

```
```
$ python3 mtgrank.py -p 

TOP 20 Modern archetypes over the last 2 weeks based on MTGTOP8 for paper only events and using exponential ranking algorithm

1 - Rakdos - 825 pts - 35 times TOP8
2 - Amulet Titan - 746 pts - 10 times TOP8
3 - Yawgmoth Evolution - 425 pts - 9 times TOP8
4 - Tron - 401 pts - 17 times TOP8
5 - 4cc - 352 pts - 26 times TOP8
6 - Living End - 216 pts - 24 times TOP8
7 - UR Murktide - 212 pts - 15 times TOP8
8 - Hammer Time - 175 pts - 19 times TOP8
9 - Burn - 169 pts - 9 times TOP8
10 - Creativity - 153 pts - 14 times TOP8
11 - Mono Black Control - 146 pts - 5 times TOP8
12 - RDW - 90 pts - 2 times TOP8
13 - Grixis Death's Shadow - 69 pts - 7 times TOP8
14 - The Underworld Cookbook - 52 pts - 5 times TOP8
15 - Breach - 50 pts - 2 times TOP8
16 - 5c Domain - 40 pts - 1 times TOP8
17 - Urza - 34 pts - 1 times TOP8
18 - Hardened Scales - 32 pts - 2 times TOP8
19 - Trash for Treasure - 32 pts - 4 times TOP8
20 - Dredge - 30 pts - 2 times TOP8
```
```
$ python3 mtgrank.py -s mtgdecks -o

TOP 20 Modern archetypes over the last 2 weeks based on MTGDECKS for online only events and using exponential ranking algorithm

1 - Rakdos - 83 pts - 28 times TOP8
2 - Dimir Bowmasters - 43 pts - 13 times TOP8
3 - Yawgmoth Evolution - 40 pts - 10 times TOP8
4 - 4cc - 33 pts - 15 times TOP8
5 - Burn - 32 pts - 13 times TOP8
6 - Tron - 30 pts - 10 times TOP8
7 - UR Murktide - 23 pts - 11 times TOP8
8 - Temur Cascade - 21 pts - 6 times TOP8
9 - Creativity - 17 pts - 6 times TOP8
10 - Mono Black Coffers - 16 pts - 6 times TOP8
11 - Amulet Titan - 14 pts - 5 times TOP8
12 - Mill - 12 pts - 4 times TOP8
13 - Jund Saga - 10 pts - 3 times TOP8
14 - Living End - 10 pts - 6 times TOP8
15 - 4 Color Cascade - 10 pts - 5 times TOP8
16 - Grixis Death's Shadow - 9 pts - 8 times TOP8
17 - Bant Control - 8 pts - 1 times TOP8
18 - Orzhov Blink - 8 pts - 1 times TOP8
19 - Jeskai Breach - 8 pts - 5 times TOP8
20 - Hammer Time - 7 pts - 3 times TOP8
```