# Author: Massimo Menichinelli
# Homepage: http://www.openp2pdesign.org
# License: GPL v.3
#
# Instructions: install pyGithub with pip install PyGithub
#


from github import Github
import networkx as nx

print "Social Network Analisys of your GitHub network"
print ""
username = raw_input("Enter your username: ")
password = raw_input("Enter your password: ")
print ""
g = Github( username, password )

graph = nx.DiGraph()

print "Looking for your followers..."
for f in g.get_user().get_followers():
    print " -", f.name
    graph.add_edge(f.name,username)
    
print "-----"

print "Looking for the ones you are following..."
for f in g.get_user().get_following():
    print " -", f.name
    graph.add_edge(username,f.name)
    
print "-----"

print "Saving the network..."
nx.write_gexf(graph, username+"_ego-network.gexf")
print "Done."