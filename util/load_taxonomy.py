#!/usr/bin/python

"""
Kind of a mess.  Load the taxonomy into the database.  Will clean up.
"""

import sys
import MySQLdb
import pprint

if not len(sys.argv) == 4:
	print "load taxonomy into db script!: usage: %s db-name db-username db-password"
	sys.exit(1)

try:
	conn = MySQLdb.connect (host="localhost",
			db=sys.argv[1],
			user=sys.argv[2],
			passwd=sys.argv[3])
except Exception, msg:
	print "Couldn't connect to database!", msg
	sys.exit(1)

name_to_node_dict = dict()
names_in_db = set()

class node(object):
	def __init__(self, string):
		if string in names_in_db:
			return
		names_in_db.add(string)

		self.string = string
		self.id = None

		if '/' in self.string:
			parent_string = '/'.join(string.split('/')[:-1])
			if not parent_string in name_to_node_dict:
				self.parent = node('/'.join(string.split('/')[:-1]))
				name_to_node_dict[self.parent.string] = self.parent
			else:
				self.parent = name_to_node_dict[parent_string]
		else:
			self.parent = None

		self.insert()

	def insert(self):
		global name_to_node_dict	
		global conn

		cursor = conn.cursor()
		insert_query = """INSERT INTO web_category VALUES ('NULL', '%s', '%s', %s);"""
		name = self.string.split("/")[-1].strip()
		slug = ''.join(filter(lambda x: x.isalnum(), name))

		if self.parent:
			this_query = insert_query % (name, slug, self.parent.id)
		else:
			this_query = insert_query % (name, slug, 'NULL')
		cursor.execute(this_query)
		self.id = conn.insert_id()
		print "got this id", self.id

categories = [line.replace(",","/") for line in open("taxonomy.csv")]

for category in categories:
	node(category)
