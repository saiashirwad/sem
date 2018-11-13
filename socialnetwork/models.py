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
    
    def friends_with(self, username):
        query = '''
        match (u1:User)-[rel]-(u2:User) 
        where u1.name='{}'and u2.name='{}' 
        return type(rel) as type
        '''.format(self.username, username)

        result = graph.run(query)
        if result.data()[0]['type'] == 'FRIENDS_WITH':
            return True 
        return False

def find_user(username):
    return graph.nodes.match('User', 'username', username).first()
    
