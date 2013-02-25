#
# Ego-network analysis of followers in a GitHub organization, Degree 1
# Fast version (only account name)
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

print "Organization Ego-network analysis"
print ""
userlogin = raw_input("Login: Enter your username: ")
password = getpass.getpass("Login: Enter yor password: ")
username = raw_input("Enter the username you want to analyse: ")
print ""
g = Github( userlogin, password )

print "ORGANIZATIONS:"
for i in g.get_user(username).get_orgs():
    print "-", i.login
print ""

org_to_mine = raw_input("Enter the name of the Organization you want to analyse: ")
print ""
org = g.get_organization(org_to_mine)

graph = nx.DiGraph()

for i in org.get_members():
    print "Member:",i.login
    graph.add_node(i.login,label=i.login,member="Yes")


for j in org.get_members():
    print ""
    print "-----"
    print "Looking for the followers of", j.login,"..."
    for f in g.get_user(j.login).get_followers():
        print " -", f.login
        graph.add_node(f.login,label=f.login, member="No")
        graph.add_edge(f.login,j.login)
                 
    print "-----"
    
    print "Looking for the users that",j.login,"is following ..."
    for f in g.get_user(j.login).get_following():
        print " -", f.login
        graph.add_node(f.login,label=f.login,member="No")
        graph.add_edge(j.login,f.login)

    print "-----"

for i in org.get_members():
    graph.node[i.login]["member"]="Yes"

print "Saving the network..."
nx.write_gexf(graph,username+"_"+org_to_mine+"_ego-network_1_level.gexf")
print "Done."