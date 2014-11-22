import math
import random
import os
import wsgiref.handlers
from google.appengine.ext import webapp
#from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from util.sessions import Session
import json
from random import randint;

class TeacherDB(db.Model):
    teacher_name = db.StringProperty
    teacher_id=db.StringProperty
    teacher_class_id=db.StringProperty
    

class tExistingHandler(webapp.RequestHandler):
    
    def post(self):
    
	self.session = Session()
	
	id_lookup= self.request.get("tidlookup")
	#tid_lookup=TeacherDB.gql("WHERE teacher_id=" + id_lookup)
	#tName = tid_lookup.teacher_name
    
	tName=id_lookup
	    
	existMsg=""
	if (tName):
	    self.session['username'] = tName

	    existMsg="Welcome back, " + tName
	else:
	    existMsg="Sorry you are not registered yet"
	
	    
	temp=os.path.join(os.path.dirname(__file__), 'templates/existingmem.html')
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{"emsg":existMsg})))	
    
class tNewHandler(webapp.RequestHandler):
  
  def post(self):
	
    que = db.Query(TeacherDB)
    db.delete(que)
	      
    tname=self.request.get("tname")
	    
    if (self.request.get("teacherid")):
	tid=tname+str(randint(1,100))
    tclassid=self.request.get('tclassid')
	    
    #Create new db for teacher
    newDB = TeacherDB(teacher_name=tname, teacher_id=tid, teacher_class_id=tclassid)
    newDB.put()
	     
    temp=os.path.join(os.path.dirname(__file__), 'templates/logint.html')
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(str(template.render(temp,{"tid":tid, "tid_msg":"Your userID is:  ", "tclassid_msg":"Your class id is:  ", "tclassid":tclassid})))	
	    
class LogoutHandler(webapp.RequestHandler):
    
    def get(self):
	
	    
	self.session=Session()
	self.session.delete_item('username')
	
	
	logoutmsg="You are not logged out"
	
	temp = os.path.join(os.path.dirname(__file__), 'templates/logout.html')
	
      	self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(str(template.render(temp,{"logoutmsg":logoutmsg})))
	
	
class LoginHandler(webapp.RequestHandler):
  
  def get (self):
	#self.response.out.write(self.request.get('out'))
	existing = self.request.get("exist")
    
	if existing == '1':
	    temp=os.path.join(os.path.dirname(__file__), 'templates/existingmem.html')
	else:
	    temp=os.path.join(os.path.dirname(__file__), 'templates/newmem.html')

		
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{})))
     
    
  def post(self):
    
    #self.session = Session()
    role=self.request.get("role")
    #self.response.out.write(test)
    
    if (role=='TEACHER'):
	temp=os.path.join(os.path.dirname(__file__), 'templates/logint.html')
    else:
	temp=temp=os.path.join(os.path.dirname(__file__), 'templates/logins.html')
	
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(str(template.render(temp,{})))
	
    '''
    self.session['username'] = acct
    temp = os.path.join(os.path.dirname(__file__), 'setting/game_control.html')
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(str(template.render(temp, {'username':acct})))
    
    
    temp = os.path.join(os.path.dirname(__file__), 'login/login.html')
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(str(template.render(temp, {'error':"Error! Please type a correct ID and a password!"})))
    '''
class MainHandler(webapp.RequestHandler):
    def get (self):

	    
      filepath = self.request.path
      self.session = Session()
      
      loggedUser=""
      greeting=""
      if (self.session.get('username')):
	greeting="Welcome, "
	loggedUser = self.session.get('username')
      	
      
      try:
        temp = os.path.join(os.path.dirname(__file__), 'templates' + filepath)
	
      	self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(str(template.render(temp,{"loggedUser":loggedUser,"greeting":greeting})))
        #self.response.out.write(filepath)
      except:
      	 temp = os.path.join(os.path.dirname(__file__), 'templates/main.html')
	 #self.response.out.write(temp)
	 self.response.headers['Content-Type'] = 'text/html'
	 self.response.out.write(str(template.render(temp,{'loggedUser':loggedUser, "greeting":greeting})))
      
def main ():
  application = webapp.WSGIApplication ([('/logout', LogoutHandler),
					('/texisting', tExistingHandler),
					('/tnew', tNewHandler),
					('/login', LoginHandler),
					('/.*', MainHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main ()