from py2neo import Graph, Relationship, Node
from datetime import datetime
import os
import uuid
from passlib.hash import bcrypt 
import uuid 
from utils import get_timestamp



# Change later!
url = 'localhost:7474'

'''
url = os.environ.get('GRAPHENEDB_URL', 'localhost:7474')
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

graph = Graph(url, username=username, password=password)
'''

graph = Graph(url)

############################## USER ####################################################

class User:
    self._user = None
    # Stores the neo4j nodeID
    self._id = None 

    def __init__(self, firstname, lastname, gender, dob, email, username, password):
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender 
        self.dob = dob 
        self.email = email
        self.username = username 
        self.password = password
        self.id = uuid.uuid4()
        self.created = get_timestamp()
    
    def register(self):
        try:
            if not self.find():
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
        except Exception as e:
            return e 
    
    @staticmethod
    def find_user(username):
        return graph.nodes.match('User', username=username).first()
    
    def find(self):
        if self._user:
            return self._user
        self._user = graph.nodes.match('User', username=self.username).first()
        return self._user
    
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
    
    def like_post(self, post_id):
        try:
            user = self.find()
            post = Post.find_by_id(post_id)
            rel = Relationship(user, 'LIKED', post)
            graph.create(rel)
        except Exception as e:
            return e
    

    def comment_on_post(self, post_id, text):
        try:
            comment = Comment(post_id=post_id, text=text, user_id=self.id)
            comment.create()
            user = self.find()
            post = Post.find_by_id(post_id)

            rel1 = Relationship(user, 'COMMENTED', comment)
            rel2 = Relationship(comment, 'ON', post)
            # Figure out if you can do this with one function.
            graph.create(rel1)
            graph.create(rel2)

        except Exception as e:
            return e
    
    def request_friendship(self, user_id):
        pass


###################################### POST ##############################################

class Post:
    self._post = None 
    self._id = None 

    def __init__(self):
        # think of a better solution, doofus
        self.id = uuid.uuid4()
        self.created = get_timestamp()
        pass 
    
    def create(self):
        post = Node(
            'Post',

        )
    
    @staticmethod 
    def find_by_id(post_id):
        # return graph.nodes.get(post_id)
        return graph.nodes.match('Post', id=post_id).first()
    
    def find(self):
        if self._post:
            return self._post 
        self._post = graph.nodes.match('Post', id=self.id).first()
        return self._post
    
    # Should this be a @staticmethod????????!!!!!!
    def get_post_likers(self):
        query = '''
        match (u:User)-[:LIKES]->(p:Post)
        where p.id={}
        return u
        '''.format(self.id)

        result = graph.run(query)
        return ['{} {}'.format(i['firstname'], i['lastname']) for i in result()]
    
    @staticmethod
    def get_likes(post_id):
        query = '''
        match (u:User)-[:LIKES]-(p:Post) 
        where p.id={}
        return count(u)
        '''.format(post_id)

        result = graph.run(query)
        return result.data()[0]['count(u)']
    

############################################### COMMENT #######################################

class Comment:
    self._comment = None 
    self._id = None 
    self._post = None 
    self._user = None

    def __init__(self, user_id, post_id, text):
        self.id = uuid.uuid4()
        self.created = get_timestamp() 
        self.post_id = post_id
        self.user_id = user_id
        self.text = text
        pass
    
    def create(self):
        comment = Node(
            'Comment',
            id=self.id, 
            created=self.created, 
            post_id=self.post_id,
            user_id=self.user_id
        )
        graph.create(comment)
        
    
    



