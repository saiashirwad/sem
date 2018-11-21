from graph import graph

from py2neo import Graph, Relationship, Node
from datetime import datetime
import os
import uuid
from passlib.hash import bcrypt 
import uuid 
from utils import get_timestamp
import random 



class User:

    def __init__(self, firstname="", lastname="", gender="", dob="", email="", username="", password="", user_obj=None):
        if user_obj is not None:
            self.firstname = user_obj['firstname']
            self.lastname = user_obj['lastname']
            self.gender = user_obj['gender']
            self.email = user_obj['email']
            self.password = user_obj['password']
            self.id = user_obj['id']
            self.created = user_obj['created']
            self.username = user_obj['username']

            # self.is_authenticated = False
            # self.is_active = False 
            # self.is_anonymous = False
        else:
            self.firstname = firstname
            self.lastname = lastname
            self.gender = gender 
            self.email = email
            self.username = username 
            self.password = password
            self.id = random.randint(1000, 1000000)
            self.created = get_timestamp()

            # self.is_anonymous = False
            # self.is_active = False
            # self.is_authenticated = False


    
    def register(self):

        try:
            if self.find() is None:
                user = Node(
                    'User',
                    name = self.username,
                    firstname=self.firstname,
                    username=self.username,
                    lastname=self.lastname, 
                    gender=self.gender, 
                    email=self.email,
                    password=self.password,
                    created=self.created,
                    id=self.id
                )

                graph.create(user)

                return User.get_user(self.username)
            else:
                return False
        except Exception as e:
            print(e)
    


    @staticmethod
    def find_user(username):

        return graph.nodes.match('User', username=username).first()
    


    @staticmethod
    def get_user(username):

        temp_user = User.find_user(username=username)

        return User(user_obj = temp_user)
    


    @staticmethod
    def neo4j_to_user(neo4j_user):

        return User(user_obj=neo4j_user)
    


    def find(self):
        return graph.nodes.match('User', username=self.username).first()

    


    def friends_with(self, username):
        query = '''
        match (u1:User)-[rel]-(u2:User) 
        where u1.username='{}'and u2.username='{}' 
        return type(rel) as type
        '''.format(self.username, username)

        result = graph.run(query)

        if result.data()[0]['type'] == 'FRIENDS_WITH':
            return True 

        return False



    def get_friends(self):

        query = '''
        match (u1:User)-[:FRIENDS_WITH]-(u2:User)
        where u1.username='{}'
        return u2
        '''.format(self.username)

        result = graph.run(query)

        return [User.neo4j_to_user(nuser) for nuser in result.data()]

    

    def like_post(self, post_id):
        try:

            user = self.find()
            post = Post.find_by_id(post_id)

            rel = Relationship(user, 'LIKED', post)

            graph.create(rel)

            return True
        except Exception as e:
            return False
    


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

            return True

        except Exception as e:
            return False
        


    @staticmethod
    def get_posts_by_user(username):

        query = '''
        match (u:User)-[:POSTED]->(p:Post)
        where u.name='{}'
        return p
        '''.format(username)

        result = graph.run(query)

        return result.data()



    @staticmethod 
    def find_user_by_id(id):

        return graph.nodes.match('User', id=id).first()



    def request_friendship(self, user_id):
        try:
            user = self.find()
            other_user = User.find_user_by_id(user_id)

            rel = Relationship(user, 'SENT_FRIEND_REQUEST_TO', other_user)

            graph.create(rel)

            return True 

        except Exception as e:
            return False
    


    def shortest_path(self, name):
        pass



    def delete_friendship(self, user_id):
        pass 
    