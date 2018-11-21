from py2neo import Graph, Relationship, Node
from datetime import datetime
import os
import uuid
from passlib.hash import bcrypt 
import uuid 
from utils import get_timestamp
import random 

from graph import graph 
from user import User


class Post:
  
    def __init__(self, text, user_id, title, tags, post_obj=None):

        if post_obj is not None:

            self.id = post_obj['id']
            self.created = post_obj['created']
            self.text = post_obj['text']
            self.creator_id = post_obj['user_id']
            self.tags = post_obj['tags']
            self.title = post_obj['title']

        else:

            self.id = random.randint(1000, 1000000)
            self.created = get_timestamp()
            self.text = text
            self.creator_id = user_id
            self.tags = tags 
            self.title = title


    
    def create(self):

        post = Node(
            'Post',
            name = self.text,
            text = self.text,
            created = self.created,
            creator_id = self.creator_id,
            id = self.id,
            tags = self.tags,
            title = self.title
        )

        graph.create(post)

        user = User.find_user_by_id(self.creator_id)

        print('here')
        rel = Relationship(user, 'POSTED', post)
        graph.create(rel)
        return post

    

    @staticmethod
    def find_by_id(post_id):

        query = '''
        match (p:Post)
        where p.id={}
        return p
        '''.format(post_id)

        result = graph.run(query)

        return result.data()[0]['p']
    


    def find(self):

        if self._post:

            return self._post 

        self._post = graph.nodes.match('Post', id=self.id).first()

        return self._post
    


    def get_post_likers(self):

        query = '''
        match (u:User)-[:LIKES]->(p:Post)
        where p.id='{}'
        return u
        '''.format(self.id)

        result = graph.run(query)

        return ['{} {}'.format(i['firstname'], i['lastname']) for i in result()]
    


    @staticmethod
    def get_likes(post_id):

        query = '''
        match (u:User)-[:LIKES]-(p:Post) 
        where p.id='{}'
        return count(u)
        '''.format(post_id)

        result = graph.run(query)

        return result.data()[0]['count(u)']
    


    # Has issues
    @staticmethod
    def delete_post(post_id):

        try:

            query = '''
            match (p:Post)
            where p.id={}
            del p
            '''.format(post_id)

            graph.run(query)

            return True

        except Exception as e:

            print(e)
    


    @staticmethod
    def neo4j_to_post(neo4j_post):

        return Post(neo4j_post=neo4j_post)
    


    def update_post(self, text):    

        try:

            query = '''
            match (p:Post)
            where p.id='{}'
            set p.text='{}'
            return p
            '''.format(self.id, text)

            result = graph.run(query)

            return Post.neo4j_to_post(result.data())
        
        except Exception as e:
            return False
    

    
    @staticmethod
    def get_post_comments(post_id):

        try:
            query = '''
            match (u:User)-[c:COMMENTED_ON]->(p:Post)
            where p.id={}
            return u.username as creator, c.text as text
            '''.format(post_id)

            print(query)

            result = graph.run(query)

            return result.data()
        
        except Exception as e:
            print(e)

            return None



