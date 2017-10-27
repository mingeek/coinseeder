CoinSeederV0.2

Instructions:

1) Make sure "seed.csv" is in the same folder as seeding.exe
- The first row in the csv MUST be the tag

2) Make sure "players.txt" is in the same folder as seeding.exe
- The format should be one player per line 

3) Make sure that "backlog.bcn" is in the same folder as seeding.exe
- You must get this from Coin, you cannot reproduce your own

Ex:
Kuyashi
Joka
Mars
...
...
Etc

3) Click seeding.exe (or python seeding.py if you are on Linux/Mac OS)

4) "seeded.txt" will be the seeded playerlist according to the version of the CSV (which is just a downloaded version of the full Coin Rank)

5) "conflicts.txt" will show matches played in WR1 and WR2 that have been played in the past two weeks

------ NOTES -----

Names of the files must be "seed.csv", "players.txt", and "backlog.bcn".

New players or altered tags will automatically be pushed to the bottom of the list.

The generator does NOT account for "|" tags, such as "GW | Lain".

Tags that only differ by the following characters ' []().*?' or by case will be viewed as the same tag.

Some tags may be incorrectly seeded due to either duplicate names in Coin Rank or typos in entry.


