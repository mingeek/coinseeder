import csv
import re

tags = {}
with open('seed.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter ='\t')
	rank = 0
	for row in reader:
		tag = row[0].split(',')[0]
		tag = re.sub("[\(\[].*?[\)\]]", "", tag.replace(" ", ""))
		tags[tag.lower()] = rank
		rank += 1

with open('players.txt') as f:
    attendees = [re.sub("[\(\[].*?[\)\]] ", "", x.strip('\n')) for x in f.readlines()]

final = []
for attendee in attendees:
	if attendee.lower().replace(" ", "") not in tags:
		tags[attendee.lower().replace(" ", "")] = len(tags)
	final.append((tags[attendee.lower().replace(" ", "")], attendee))
final = sorted(final)


f = open('seeded.txt', 'w')
for player in final:
	f.write(player[1] + '\n')  # python will convert \n to os.linesep
f.close()