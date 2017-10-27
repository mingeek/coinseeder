import csv
import re
import datetime as dt
from xml.dom import minidom

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

#Scans the log of matches to find all matches played within the past two weeks
def findPrevMatches(num_days):
	xmldoc = minidom.parse('backlog.bcn')
	itemlist = xmldoc.getElementsByTagName('Match')

	matches = [x for x in itemlist]
	played_matches = []

	for i in matches:
		last_week = dt.datetime.today() - dt.timedelta(days=num_days)
		date1 = dt.datetime.strptime(i.attributes['Timestamp'].value.split()[0], "%m/%d/%Y")

		if date1 > last_week:
			p1_tag = re.sub("[\(\[].*?[\)\]]", "", str(i.attributes['Player1'].value).replace(" ", ""))
			p2_tag = re.sub("[\(\[].*?[\)\]]", "", str(i.attributes['Player2'].value).replace(" ", ""))
			played_matches.append((p1_tag, p2_tag))
	return played_matches

#Takes a list of ordered seeds and returns a string list of conflicts
def findConflicts(seeds, num_days):
	num_entrants = len(seeds)
	number = 2

	while num_entrants > number:
		number *= 2

	opponents = {}

	#First loop to add in first round matches
	for x in range(1, num_entrants + 1):
		if (number - x < num_entrants):
			opponents[x] = number - x + 1

	#Loop for second round opponents where both players have a bye
	newNum = number / 2 + 1
	for x in range(num_entrants - len(opponents),0,-1):
		if (newNum - x not in opponents):
			opponents[x] = newNum - x

	conflicts = []

	#Number of days to check for previous matches
	matches = findPrevMatches(num_days)
	for index in opponents:
		player1 = seeds[index-1][1]
		player2 = seeds[opponents[index] - 1][1]
		p1_tag = re.sub("[\(\[].*?[\)\]]", "", str(player1).replace(" ", ""))
		p2_tag = re.sub("[\(\[].*?[\)\]]", "", str(player2).replace(" ", ""))
		region1 = seeds[index-1][2]
		region2 = seeds[opponents[index] - 1][2]

		#Check if players have played
		if (p1_tag, p2_tag) in matches or (p2_tag, p1_tag) in matches:
			if(player1, player2) in conflicts or (player2, player1) in conflicts:
				continue
			conflict = (player1, player2)
			conflicts.append(conflict)
	return conflicts

def writeSeeds(seeds):
	f = open('seeded.txt', 'w')
	for player in seeds:
		f.write(player[1] + '\n')
	f.close()

def writeConflicts(conflicts):
	f = open('conflicts.txt', 'w')
	for conflict in conflicts:
		f.write(str(conflict) + '\n')
	f.close()

def main():
	tags = setTags('seed.csv')
	seeded_list = setOrder(tags)
	conflicts = findConflicts(seeded_list, 14)
	writeSeeds(seeded_list)
	writeConflicts(conflicts)

if __name__ == "__main__":
    main()
