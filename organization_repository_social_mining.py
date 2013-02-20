#
# Basic analysis of an Organization repository in GitHub
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

graph = nx.MultiDiGraph()
issue = {}

def analyse_repo(repository):    
    print "-----"
    print "DESCRIPTION:",repository.description
    print "-----"
    print "OWNER:",repository.owner.login
    graph.add_node(str(unicode(repository.owner.login)),owner="Yes")
    print "-----"
    print "WATCHERS:",repository.watchers
    for i in repository.get_stargazers():
        if i != None:
            print "-",i.login
            if i.login not in graph:
                graph.add_node(str(unicode(i.login)),watcher="Yes")
            else:
                graph.node[i.login]["watcher"]="Yes"
    print "-----"
    print "COLLABORATORS"
    for i in repository.get_collaborators():
        if i != None:
            print "-",i.login
            if i.login not in graph:
                graph.add_node(str(unicode(i.login)),collaborator="Yes")
            else:
                graph.node[i.login]["collaborator"]="Yes"
    print "-----"
    print "HAS ISSUES=",repository.has_issues
    if repository.has_issues == True:
        print "-----"
        print "ISSUES: Open ones"
        for i in repository.get_issues(state="open"):
            if i.user != None:
                print "- Created by", i.user.login
                #issue[i.number]["author"] = i.user.login
                #print issue[i.number]["author"]
                print i.number
            print "--",i.title
            if i.assignee != None:
                print "-- Assigned to",i.assignee.login
            print "--",i.comments,"comments"
            for f in i.get_comments():
                if f.user != None:
                    print "--- With a comment by",f.user.login
            print ""      

        print "ISSUES: Closed ones"
        for i in repository.get_issues(state="closed"):
            if i.user != None:
                print "- Created by", i.user.login
                #issue[i.number]["author"] = i.user.login
                #print issue[i.number]["author"]
                print i.number
            print "--",i.title
            if i.assignee != None:
                print "-- Assigned to",i.assignee.login
            print "--",i.comments,"comments"
            for f in i.get_comments():
                if f.user != None:
                    print "--- With a comment by",f.user.login
            print ""      

              
    print "-----"
    print "CONTRIBUTORS"
    for i in repository.get_contributors():
        print "-", i.login
        if i.login not in graph:
                graph.add_node(str(unicode(i.login)),contributor="Yes")
        else:
            graph.node[i.login]["contributor"]="Yes"
    print "-----"
    print "COMMITS"
    for i in  repository.get_commits():
        print "-",i.sha
        if i.committer != None:
            print "-- by",i.committer.login
   
    print "-----"
    
    #print "FORKS"
    #for i in repository.get_forks():
    #    print i.name
    #    print "ANALYSING A FORK"
    #    print ""
    #    analyse_repo(i)
    #    print ""
    #print "-----"
    
    # Check the attributes of every node, and add a "No" when it is not present, in order to let Gephi use the attribute for graph partitioning
    for i in graph.nodes():
        if "owner" not in graph.node[i]:
            graph.node[i]["owner"] = "No"
        if "contributor" not in graph.node[i]:
            graph.node[i]["contributor"] = "No"               
        if "collaborator" not in graph.node[i]:
            graph.node[i]["collaborator"] = "No"
        if "watcher" not in graph.node[i]:
            graph.node[i]["watcher"] = "No"

    return


if __name__ == "__main__":
    print "Social Network Analisys of your GitHub Organization"
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
    
    print org.login,"has",org.public_repos, "repositories."
    
    print ""
    
    for repo in org.get_repos():
        print "-",repo.name
    
    print ""
    
    repo_to_mine = raw_input("Enter the name of the repository you want to mine: ")
    b = org.get_repo(repo_to_mine)
    analyse_repo(b)
    
    print graph.nodes()
    print graph.edges()
    
    print "Saving the network..."
    nx.write_gexf(graph, username+"_"+repo_to_mine+"_social_interactions_analysis.gexf")
    print "Done. Saved as "+username+"_"+repo_to_mine+"_social_interactions_analysis.gexf"