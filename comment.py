from graph import graph

from py2neo import Graph, Relationship, Node
from datetime import datetime
import os
import uuid
from passlib.hash import bcrypt 
import uuid 
from utils import get_timestamp
import random

class Comment:

    def __init__(self, user_id, post_id, text):
        self.id = random.randint(100000, 10000000)
        self.created = get_timestamp() 
        self.post_id = post_id
        self.user_id = user_id
        self.text = text
        pass


    def create(self):
       
        query = '''
        match (u:User), (p:Post)
        where u.id={} and p.id={}
        create (u)-[c:COMMENTED_ON {{text: '{}', id: {} }}]->(p)
        return c
        '''.format(self.user_id, self.post_id, self.text, self.id)

        return graph.run(query)



    @staticmethod
    def delete_comment(comment_id):
        try:
            query = '''
            match (u:User)-[c:COMMENTED_ON]-(p:Post)
            where c.id = {}
            delete c
            '''
            graph.run(query)
            return True
        except Exception as e:
            return False


        
    
    



