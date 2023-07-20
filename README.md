# MTGRank
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue)  
---  
A Magic: The Gathering format archetype ranking tool based on TOP 8 tournaments results.

## Features

* Support of [MTGTOP8](https://mtgtop8.com), [MTGDECKS](https://mtgdecks.net) and [MTGGOLDFISH](https://www.mtggoldfish.com) as tournaments data sources.
* Support of 3 formats: Modern, Legacy and Pioneer.
* Support of 2 ranking algorithms:
    * Linear: each TOP8 member gets 9-n pts where n is the rank ;
    * Exponential: TOP1 gets 8 pts, TOP2 gets 4 pts, TOP3-4 get 2 pts, TOP5-8 get 1 pt 
* Support of 3 possible time ranges for analysis: last 2 weeks, last 2 months and since beginning of the year.

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
usage: mtgrank.py [-h] [--source SOURCE] [--format FORMAT] [--algorithm ALGORITHM] [--top TOP] [--date]

options:
  -h, --help            show this help message and exit
  --source SOURCE, -s SOURCE
                        Data source to use (mtgtop8, mtgdecks, mtggoldfish ; default: mtgtop8)
  --format FORMAT, -f FORMAT
                        Format (modern, legacy, pioneer ; default: modern)
  --algorithm ALGORITHM, -a ALGORITHM
                        Ranking algorithm (default: exponential):
                            Linear: each TOP8 member gets 9-n pts, where n is the rank; or
                            Exponential: TOP1 gets 8 pts, TOP2 gets 4 pts, TOP3-4 get 2 pts, TOP5-8 get 1 pt
  --top TOP, -t TOP     TOP ranking size (default: 20)
  --date, -d            Time range to be specified through a selection menu (default: last 2 weeks)
```

## Examples
```
$ python3 mtgrank.py 

TOP 20 Modern archetypes over the last 2 weeks based on MTGTOP8 and using exponential ranking algorithm

1 - Rakdos - 159 pts - 59 times TOP8
2 - 4cc - 105 pts - 46 times TOP8
3 - Living End - 96 pts - 31 times TOP8
4 - Creativity - 81 pts - 25 times TOP8
5 - UR Murktide - 66 pts - 29 times TOP8
6 - Tron - 65 pts - 26 times TOP8
7 - Burn - 55 pts - 18 times TOP8
8 - Yawgmoth Evolution - 54 pts - 17 times TOP8
9 - Amulet Titan - 53 pts - 17 times TOP8
10 - Hammer Time - 52 pts - 22 times TOP8
11 - Mono Black Control - 33 pts - 12 times TOP8
12 - Trash for Treasure - 33 pts - 5 times TOP8
13 - Death's Shadow - 31 pts - 16 times TOP8
14 - Cascade Crash - 29 pts - 15 times TOP8
15 - Breach - 26 pts - 12 times TOP8
16 - RDW - 26 pts - 7 times TOP8
17 - Jund - 24 pts - 7 times TOP8
18 - Hardened Scales - 22 pts - 5 times TOP8
19 - Merfolk - 21 pts - 8 times TOP8
20 - The Underworld Cookbook - 18 pts - 7 times TOP8 
```
```
$ python3 mtgrank.py -s mtggoldfish -d
Select time range:
        1 Last 2 weeks
        2 Last 2 months
        3 Since beginning of the year
 [1/2/3]: 2

TOP 20 Modern archetypes over the last 2 months based on MTGGOLDFISH and using exponential ranking algorithm

1 - Rakdos - 261 pts - 110 times TOP8
2 - Creativity - 258 pts - 102 times TOP8
3 - UR Murktide - 258 pts - 93 times TOP8
4 - 4cc - 210 pts - 77 times TOP8
5 - Living End - 201 pts - 71 times TOP8
6 - Tron - 139 pts - 53 times TOP8
7 - Yawgmoth Evolution - 135 pts - 45 times TOP8
8 - Hammer Time - 120 pts - 53 times TOP8
9 - Burn - 116 pts - 49 times TOP8
10 - Crashing Footfalls - 115 pts - 43 times TOP8
11 - Generic Ragavan - 91 pts - 28 times TOP8
12 - Amulet Titan - 87 pts - 30 times TOP8
13 - Dimir Control - 44 pts - 14 times TOP8
14 - Domain Zoo - 44 pts - 21 times TOP8
15 - Simic Hardened Scales - 39 pts - 9 times TOP8
16 - Jund - 38 pts - 9 times TOP8
17 - Mill - 34 pts - 11 times TOP8
18 - Grinding Station - 33 pts - 10 times TOP8
19 - Temur Cascade - 32 pts - 9 times TOP8
20 - Grixis Death's Shadow - 30 pts - 15 times TOP8
```
```
$ python3 mtgrank.py -f legacy -a linear -t 10

TOP 10 Legacy archetypes over the last 2 weeks based on MTGTOP8 and using linear ranking algorithm

1 - Grixis Delver - 131 pts - 30 times TOP8
2 - Death's Shadow - 111 pts - 18 times TOP8
3 - Painter - 98 pts - 22 times TOP8
4 - Lands - 82 pts - 14 times TOP8
5 - Death & Taxes - 80 pts - 13 times TOP8
6 - Dragon Stompy - 77 pts - 13 times TOP8
7 - Reanimator - 76 pts - 16 times TOP8
8 - 4cc - 70 pts - 10 times TOP8
9 - Grixis Aggro - 44 pts - 7 times TOP8
10 - Initiative Stompy - 43 pts - 10 times TOP8
```
```
$ python3 mtgrank.py -f pioneer -s mtgdecks

TOP 20 Pioneer archetypes over the last 2 weeks based on MTGDECKS and using exponential ranking algorithm

1 - Rakdos - 174 pts - 74 times TOP8
2 - Green Devotion - 160 pts - 57 times TOP8
3 - Azorius Control - 70 pts - 23 times TOP8
4 - Creativity - 67 pts - 29 times TOP8
5 - Mono White Humans - 66 pts - 22 times TOP8
6 - Boros Prowess - 41 pts - 17 times TOP8
7 - Abzan Greasefang - 38 pts - 13 times TOP8
8 - Lotus Field Combo - 36 pts - 15 times TOP8
9 - Azorius Spirits - 31 pts - 16 times TOP8
10 - WU Control - 27 pts - 9 times TOP8
11 - Boros Convoke - 25 pts - 11 times TOP8
12 - BR Aggro - 25 pts - 11 times TOP8
13 - Parhelion Shoot - 24 pts - 9 times TOP8
14 - Enigmatic Incarnatio... - 22 pts - 9 times TOP8
15 - Goblins - 21 pts - 4 times TOP8
16 - Izzet Phoenix - 16 pts - 7 times TOP8
17 - RG Aggro - 16 pts - 5 times TOP8
18 - Red Deck Wins - 16 pts - 6 times TOP8
19 - Mardu Sacrifice - 15 pts - 6 times TOP8
20 - Jund Transmogrify - 14 pts - 3 times TOP8
```