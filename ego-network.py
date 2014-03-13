#
# Ego-network analysis of followers in GitHub, Degree 1 
# Slow version (even real name)
#
# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: GPL v.3
#
# Requisite: 
# install pyGithub with pip install PyGithub
# install NetworkX with pip install networkx
#
# PyGitHub documentation can be found here: 
# https://github.com/jacquev6/PyGithub
#
from github import Github
import networkx as nx
import getpass

print "Social Network Analisys of a user GitHub network"
print ""
username = raw_input("Enter your username: ")
password = getpass.getpass("Enter yor password: ") 
user = raw_input("Enter the username to mine: ")
print ""
g = Github( username, password )

graph = nx.DiGraph()

graph.add_node(username,label=g.get_user(user).name)

print "Looking for the followers of",user,"..."
for f in g.get_user(user).get_followers():
    print " -", f.login, " / ", f.name
    if f.name == None:
        graph.add_node(f.login,label=f.login)
        graph.add_edge(f.login,username)
    else:
        graph.add_node(f.login,label=f.name)
        graph.add_edge(f.login,username)
        
print "-----"

print "Looking for the users",user", is following..."
for f in g.get_user(user).get_following():
    print " -", f.login, " / ", f.name
    if f.name == None:
        graph.add_node(f.login,label=f.login)
        graph.add_edge(username,f.login)
    else:
        graph.add_node(f.login,label=f.name)
        graph.add_edge(username,f.login)
    
print "-----"

print "Saving the network..."
nx.write_gexf(graph, user+"_ego-network.gexf")
print "Done."