import csv
import re

#Takes the name of a CSV file and returns a dictionary of tags	
def setTags(stats_sheet):
	tags_list = {}
	with open(stats_sheet, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter ='\t')
		rank = 0
		for row in reader:
			if row[0].split(',')[0] == "Name":
				continue
			tag = row[0].split(',')[0]
			region = row[0].split(',')[3]
			tag = re.sub("[\(\[].*?[\)\]]", "", tag.replace(" ", ""))
			tags_list[tag.lower()] = (rank,region)
			rank += 1
	return tags_list

#Takes a dictionary of tags and returns a seeded list of players
def setOrder(tags_list):
	with open('players.txt') as f:
	    attendees = [re.sub("[\(\[].*?[\)\]] ", "", x.strip('\n')) for x in f.readlines()]

	seeds = []
	for attendee in attendees:
		if attendee.lower().replace(" ", "") not in tags_list:
			tags_list[attendee.lower().replace(" ", "")] = (len(tags_list),"")
		seeds.append((tags_list[attendee.lower().replace(" ", "")][0], attendee,tags_list[attendee.lower().replace(" ", "")][1]))
	return sorted(seeds)

#Takes a list of ordered seeds and returns a string list of conflicts
def findConflicts(seeds):
	num_entrants = len(seeds)
	number = 2
	while num_entrants > number:
		number *= 2

	opponents = {}

	#first loop to add in first round matches
	for x in range(1, num_entrants + 1):
		if (number - x < num_entrants):
			opponents[x] = number - x + 1

	#loop for second round opponents where both players have a bye
	newNum = number / 2 + 1
	for x in range(num_entrants - len(opponents),0,-1):
		if (newNum - x not in opponents):
			opponents[x] = newNum - x

	#check for regional conflicts between opponents
	conflicts = []
	for index in opponents:
		player1 = seeds[index-1][1]
		player2 = seeds[opponents[index] - 1][1]
		region1 = seeds[index-1][2]
		region2 = seeds[opponents[index] - 1][2]
		#ignore conflicts if both players have no listed region or are both out of region
		if region2 == "" or region1 == "" or region2 == "<< Out of region >>" or region1 == "<< Out of region >>":
			continue
		if region2 == region1:
			conflict = (player2, player1)
			conflicts.append(conflict)
	return conflicts

def writeSeeds(seeds):
	f = open('seeded.txt', 'w')
	for player in seeds:
		f.write(player[1] + '\n')  # python will convert \n to os.linesep
	f.close()

def writeConflicts(conflicts):
	f = open('conflicts.txt', 'w')
	for conflict in conflicts:
		f.write(str(conflict) + '\n')
	f.close()

def main():
	tags = setTags('seed.csv')
	seeded_list = setOrder(tags)
	conflicts = findConflicts(seeded_list)
	writeSeeds(seeded_list)
	writeConflicts(conflicts)

if __name__ == "__main__":
    main()
