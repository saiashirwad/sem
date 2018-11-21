import datetime 

def get_timestamp():
    return datetime.datetime.now().timestamp()

def parse_posts(posts):
    parsed_posts = []
    for post in posts:
        postvar = post['p']
        parsed_posts.append