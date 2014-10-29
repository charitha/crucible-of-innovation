#!/usr/bin/env python

import cgi
import datetime
import webapp2
import urllib
import json
import operator

NUMTEAM = 25
CAT1 = "Best Service Produced"
CAT2 = "Best use of Intuit Services"
CAT3 = "Innovate for India"
FORMAT_MSG = "Please Re-vote with the format @gw &lt;team#&gt; &lt;c1/c2/c3&gt; &lt;your_corp_id&gt;"
FORMAT_MSG2= "Please Re-vote with the format @gw.check &lt;team#&gt;"

CATEGORIES = ['c1','c2', 'c3']
TEXTAPPKEY = 'e1fcf9b5-41aa-4529-94b5-9cd38cb1e4f5'
#TEXTAPPKEY = '71aeadce-5ad5-4528-ad46-806bb0be3892'
#TEXTAPPKEY2 = '83f4873c-0703-47fe-95e0-798ae1006941'

from google.appengine.ext import ndb

class trackerdb(ndb.Model):
	txtHash = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)
	category = ndb.StringProperty()
	tnumber = ndb.IntegerProperty()
	
	@classmethod
	def query_votes(cls,cat,tn):
		tn = str(tn)
		queryString = "Select * from trackerdb where category = '"+ cat + "'and tnumber =" + tn
		return ndb.gql(queryString).count()
		
	@classmethod
	def validate_unique_vote(cls,cat,th):
		queryString = "Select * from trackerdb where category = '"+ cat + "'and txtHash ='" + th +"'"
		if ndb.gql(queryString).count() !=0:
			return False
		else:
			return True
	
	
	
class VoteFeedBack(webapp2.RequestHandler):
	def get(self):
		categorys = ['c1','c2', 'c3']
		dictvote = {}
	 
		for cat in categorys:
			dictvote[cat] = {}
			for i in range(1,NUMTEAM+1):
				dictvote[cat][i] = trackerdb.query_votes(cat,i)
			dictvote[cat] = sorted(dictvote[cat].iteritems(), key=operator.itemgetter(1),reverse=True)[0:5]
			
			#dictvote[cat].sort(reverse=True)
			#dictvote[cat] = dictvote[cat][0:5]
		jsonobj = json.dumps(dictvote,ensure_ascii=False)
		self.response.out.write(str( jsonobj))

				
class GetIndividualVotes(webapp2.RequestHandler):
	def get(self):
		outputText = '<html> <head> <meta name="txtweb-appkey" content="'+TEXTAPPKEY+'"/></head><body>'
		tn = self.request.get('txtweb-message')
		if tn != '':
			try:
				tn = int(tn)
				categorys = ['c1','c2', 'c3']
				dictvote ={}
				
				if tn>0 and tn <= NUMTEAM :
					for cat in categorys:
						dictvote[cat] = trackerdb.query_votes(cat,tn)
					votingText = CAT1 + ": "+str(dictvote['c1']) +"<br/>"+CAT2 + ": "+str(dictvote['c2'])+"<br/>"+CAT3 + ": "+str(dictvote['c3'])
					outputText = outputText + 'Your votes: <br/> '+votingText
				else:
					outputText = outputText + FORMAT_MSG2 +' where team# is 1 to' +str(NUMTEAM)
			except ValueError:
				outputText = outputText + FORMAT_MSG2
		else:
			outputText = outputText + FORMAT_MSG2
		outputText = outputText + '</body></html>'
		self.response.out.write(outputText)

	
class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('<html><body>Its Working!!</body></html>')

class Polltracker(webapp2.RequestHandler):
	def get(self):
		outputText = '<html> <head> <meta name="txtweb-appkey" content="'+TEXTAPPKEY+'"/></head><body>'
		
		try:
			textMsg = self.request.get('txtweb-message')
			textHash = self.request.get('txtweb-mobile')
			textMsgParts = textMsg.split()
			if(len(textMsgParts) == 3):
				teamnumber = int(textMsgParts[0])
				teamcategory = textMsgParts[1]
				if teamnumber>0 and teamnumber<= NUMTEAM :
					if teamcategory in CATEGORIES :
						
						if(trackerdb.validate_unique_vote(teamcategory,textHash)):
							entryTrackerDB = trackerdb(txtHash = textHash  , category = teamcategory , tnumber = teamnumber)
							entryTrackerDB.put()
							outputText = outputText + 'Thank you. Your vote has been recorded!'						
						else:
							outputText = outputText + 'Sorry, your vote has already been registered once for this category'
					else:
						outputText = outputText + FORMAT_MSG + ' where team# is 1 to' + NUMTEAM
				else:
					outputText = outputText + FORMAT_MSG 
			else:
				outputText = outputText + FORMAT_MSG
		except:
			outputText = outputText + FORMAT_MSG
		outputText = outputText + '</body></html>'
		self.response.out.write(outputText)
			

			

		

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/message',Polltracker ),
  ('/getvotes',VoteFeedBack),
  ('/getmyvote',GetIndividualVotes)
], debug=True)