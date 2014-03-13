# -*- coding: utf-8 -*-
#
# Ego-network analysis of followers in GitHub, Degree 2 
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

print "Social Network Analisys of your GitHub network"
print ""
username = raw_input("Enter your username: ")
password = getpass.getpass("Enter yor password: ") 
user = raw_input("Enter the username to mine: ")
print ""
g = Github( username, password )

graph = nx.DiGraph()

graph.add_node(user,label=g.get_user(user).name)

print "Looking for the followers of",user,"..."
for f in g.get_user(user).get_followers():
    print " -", f.login, " / ", f.name
    if f.name == None:
        graph.add_node(f.login,label=f.login)
        graph.add_edge(f.login,user)
    else:
        graph.add_node(f.login,label=f.name)
        graph.add_edge(f.login,user)
    print " And his/her followers:"
    for i in f.get_followers():
        print " --", i.login, " / ", i.name
        if i.name == None:
            graph.add_node(i.login,label=i.login)
            graph.add_edge(i.login,f.login)
        else:
            graph.add_node(i.login,label=i.name)
            graph.add_edge(i.login,f.login)
    print " And the users she/he's following:"
    for i in f.get_following():
        print " --", i.login, " / ", i.name
        if i.name == None:
            graph.add_node(i.login,label=i.login)
            graph.add_edge(f.login,i.login)
        else:
            graph.add_node(i.login,label=i.name)
            graph.add_edge(f.login,i.login)
        
print "-----"

print "Looking for the users",user,"is following..."
for f in g.get_user(user).get_following():
    print " -", f.login, " / ", f.name
    if f.name == None:
        graph.add_node(f.login,label=f.login)
        graph.add_edge(user,f.login)
    else:
        graph.add_node(f.login,label=f.name)
        graph.add_edge(user,f.login)
    print " And his/her followers:"
    for i in f.get_followers():
        print " --", i.login, " / ", i.name
        if i.name == None:
            graph.add_node(i.login,label=i.login)
            graph.add_edge(i.login,f.login)
        else:
            graph.add_node(i.login,label=i.name)
            graph.add_edge(i.login,f.login)
    print " And the users she/he's following:"
    for i in f.get_following():
        print " --", i.login, " / ", i.name
        if i.name == None:
            graph.add_node(i.login,label=i.login)
            graph.add_edge(f.login,i.login)
        else:
            graph.add_node(i.login,label=i.name)
            graph.add_edge(f.login,i.login)
    
print "-----"

print "Saving the network..."
nx.write_gexf(graph, user+"_ego-network_2_levels.gexf")
print "Done."