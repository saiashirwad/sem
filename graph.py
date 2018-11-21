from py2neo import Graph

url = 'localhost:7474'

graph = Graph(url, username='neo4j', password='1234')

print(graph)