
import csv
import re

tags = {}
with open('seed.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter ='\t')
	rank = 0
	for row in reader:
		if row[0].split(',')[0] == "Name":
			continue
		tag = row[0].split(',')[0]
		region = row[0].split(',')[3]
		tag = re.sub("[\(\[].*?[\)\]]", "", tag.replace(" ", ""))
		tags[tag.lower()] = (rank,region)
		rank += 1

with open('players.txt') as f:
    attendees = [re.sub("[\(\[].*?[\)\]] ", "", x.strip('\n')) for x in f.readlines()]

final = []
for attendee in attendees:
	if attendee.lower().replace(" ", "") not in tags:
		tags[attendee.lower().replace(" ", "")] = (len(tags),"")
	final.append((tags[attendee.lower().replace(" ", "")][0], attendee,tags[attendee.lower().replace(" ", "")][1]))
final = sorted(final)

entrants = len(final)

number = 2
while entrants > number:
	number *= 2

opponents = {}

#first loop to add in first round matches
for x in range(1, entrants + 1):
	if (number - x < entrants):
		opponents[x] = number - x + 1

#loop for second round opponents where both players have a bye
newNum = number / 2 + 1
for x in range(entrants - len(opponents),0,-1):
	if (newNum - x not in opponents):
		opponents[x] = newNum - x

#check for regional conflicts between opponents
conflicts = []
for index in opponents:
	player1 = final[index-1][1]
	player2 = final[opponents[index] - 1][1]
	region1 = final[index-1][2]
	region2 = final[opponents[index] - 1][2]
	#ignore conflicts if both players have no listed region or are both out of region
	if region2 == "" or region1 == "" or region2 == "<< Out of region >>" or region1 == "<< Out of region >>":
		continue
	if region2 == region1:
		tempString = str(player2) + " vs " + str(player1)
		conflicts.append(tempString)



f = open('seeded.txt', 'w')
for player in final:
	f.write(player[1] + '\n')  # python will convert \n to os.linesep
f.close()

#write conflicts
f = open('conflicts.txt', 'w')
for conflict in conflicts:
	f.write(conflict + '\n')
f.close()

