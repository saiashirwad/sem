from py2neo import Graph, Relationship, Node
from datetime import datetime
import os
import uuid
from passlib.hash import bcrypt 



# Change later!
url = 'localhost:7474'

'''
url = os.environ.get('GRAPHENEDB_URL', 'localhost:7474')
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

graph = Graph(url, username=username, password=password)
'''

graph = Graph(url)

class User:
    def __init__(self, firstname, lastname, gender, dob, email, username, password):
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender 
        self.dob = dob 
        self.email = email
        self.username = username 
        self.password = password
    
    def register(self):
        if not find_user(self.username):
            user = Node(
                'User',
                username=self.username,
                lastname=self.lastname, 
                gender=self.gender, 
                dob=self.dob,
                email=self.email,
                username=self.username, 
                password=self.password 
            )
            graph.create(user)
            return True 
        else:
            return False

    
def find_user(username):
    user = graph.nodes.match('User', 'username', username).first()
    
