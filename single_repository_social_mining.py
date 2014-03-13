# -*- coding: utf-8 -*-
#
# Social analysis of a single repository in GitHub
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
import os

# Clear screen
os.system('cls' if os.name=='nt' else 'clear')

from repoanalysis import analyse_repo

# Variables for the whole program

graph = nx.MultiDiGraph()
issue = {}
issue = {0:{"author":"none", "comments":{}}}
commits = {0:{"commit","sha"}}
repos = {}



if __name__ == "__main__":
    print "Social Network Analisys of a GitHub repository"
    print ""
    userlogin = raw_input("Login: Enter your username: ")
    password = getpass.getpass("Login: Enter yor password: ")
    username = raw_input("Enter the username you want to analyse: ")
    print ""
    g = Github( userlogin, password )
    
    
    print username,"has",g.get_user(username).public_repos, "repositories."
    
    print ""
    
    for repo in g.get_user(username).get_repos():
        print "-",repo.name
    
    print ""
    
    repo_to_mine = raw_input("Enter the name of the repository you want to mine: ")
    b = g.get_user(username).get_repo(repo_to_mine)
    analyse_repo(b,graph)
    
    # Getting rid of the node "None", it was used to catch the errors of users that are NoneType
    graph.remove_node('None')
    
    print ""
    print "NODES..."
    print graph.nodes()
    print ""
    print "EDGES..."
    print graph.edges()
    print ""
    
    print "Saving the network..."
    nx.write_gexf(graph, username+"_"+repo_to_mine+"_social_interactions_analysis.gexf")
    print "Done. Saved as "+username+"_"+repo_to_mine+"_social_interactions_analysis.gexf"