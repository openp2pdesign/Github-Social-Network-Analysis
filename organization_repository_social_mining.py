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

# Variables for the whole program

graph = nx.MultiDiGraph()
issue = {}
issue = {0:{"author":"none", "comments":{}}}
commits = {0:{"commit","sha"}}
repos = {}

def analyse_repo(repository,loop): 
    print ""
    print "LOOP:",loop
    print ""   
    print "-----"
    print "DESCRIPTION:",repository.description
    print "-----"
    print "OWNER:",repository.owner.login
    graph.add_node(str(unicode(repository.owner.login)),owner="Yes")
    print "-----"
    print "WATCHERS:",repository.watchers
    print ""
    for i in repository.get_stargazers():
        if i != None:
            print "-",i.login
            if i.login not in graph:
                graph.add_node(str(unicode(i.login)),watcher="Yes")
            else:
                graph.node[i.login]["watcher"]="Yes"
        else:
            graph.node["None"]["watcher"]="Yes"
    print "-----"
    print "COLLABORATORS"
    print ""
    for i in repository.get_collaborators():
        if i != None:
            print "-",i.login
            if i.login not in graph:
                graph.add_node(str(unicode(i.login)),collaborator="Yes")
            else:
                graph.node[i.login]["collaborator"]="Yes"
        else:
            graph.node["None"]["collaborator"]="Yes"
    print "-----"
    print "HAS ISSUES=",repository.has_issues
    if repository.has_issues == True:
        print "-----"
        print "ISSUES: Open ones"
        print ""
        for i in repository.get_issues(state="open"):
            print "Issue number:",i.number
            if i.user != None:
                print "- Created by", i.user.login
                issue[i.number]= {}
                issue[i.number]["comments"]= {}
                issue[i.number]["author"] = i.user.login
            else:
                print "- Created by None"
                issue[i.number]= {}
                issue[i.number]["comments"]= {}
                issue[i.number]["author"] = "None"
            print "--",i.title
            if i.assignee != None:
                print "-- Assigned to",i.assignee.login
                graph.add_edge(str(i.user.login),str(i.assignee.login))
            else:
                print "-- Assigned to None"
                graph.add_edge(str(i.user.login),"None")
            print "--",i.comments,"comments"
            for j,f in enumerate(i.get_comments()):
                if f.user != None:
                    print "--- With a comment by",f.user.login
                    issue[i.number]["comments"][j] = f.user.login
                else:
                    print "--- With a comment by None"
                    issue[i.number]["comments"][j] = "None"
            print ""      

        print "ISSUES: Closed ones"
        print ""
        for i in repository.get_issues(state="closed"):
            print "Issue number:",i.number
            if i.user != None:
                print "- Created by", i.user.login
                issue[i.number]= {}
                issue[i.number]["comments"]= {}
                issue[i.number]["author"] = i.user.login
            else:
                print "- Created by None"
                issue[i.number]= {}
                issue[i.number]["comments"]= {}
                issue[i.number]["author"] = "None"
            print "--",i.title
            if i.assignee != None:
                print "-- Assigned to",i.assignee.login
                graph.add_edge(str(i.user.login),str(i.assignee.login))
            else:
                print "-- Assigned to None"
                graph.add_edge(str(i.user.login),"None")
            print "--",i.comments,"comments"
            for j,f in enumerate(i.get_comments()):
                if f.user != None:
                    print "--- With a comment by",f.user.login
                    issue[i.number]["comments"][j] = f.user.login
                else:
                    print "--- With a comment by None"
                    issue[i.number]["comments"][j] = "None"
            print ""      
              
    print "-----"
    print "CONTRIBUTORS"
    print ""
    for i in repository.get_contributors():
        if i.login != None:
            print "-", i.login
            if i.login not in graph:
                    graph.add_node(str(unicode(i.login)),contributor="Yes")
            else:
                graph.node[i.login]["contributor"]="Yes"
        else:
            graph.node["None"]["contributor"]="Yes"
    print "-----"
    print "COMMITS"
    print ""
    
    repos[loop]={0:""}
    for k,i in enumerate(repository.get_commits()):
        print "-",i.sha
        if i.committer != None:
            print "-- by",i.committer.login
            repos[loop][k]=i.committer.login
        else:
            print "-- by None"
            repos[loop][k]="None"
        
   
    print "-----"
       
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
            
            
    # Add an edge from a commiter to a previous one,
    # i.e. if you are committing after somebody has commited,
    # you are interacting with him/her
    print "ADDING EDGES FROM COMMITS"
    print ""
    for h in repos[loop]:
        if h < len(repos[loop])-1:
            print "-"
            print "Committer:",repos[loop][h]
            print "Adding an edge from:",repos[loop][h],"to previous committer:",repos[loop][h+1]
            #graph.add_edge(str(i.user.login),str(i.assignee.login))
            
    # Creating the edges from the issues and their comments.
    # Each comment interacts with the previous ones,
    # so each user interacts with the previous ones that have been creating the issue or commented it
    print ""
    print "-----"
    print "ADDING EDGES FROM ISSUES COMMENTING"
    print ""
    
    for a,b in enumerate(issue):
        print "-----"
        print "Issue author:",issue[a]["author"]
        print ""
        for k,j in enumerate(issue[a]["comments"]):
            print "Comment author:",issue[a]["comments"][k]
            print "Adding an edge from",issue[a]["comments"][k],"to",issue[a]["author"]
            graph.add_edge(str(issue[a]["comments"][k]),str(issue[a]["author"]))

            for l in range(k):
                print "Adding an edge from",issue[a]["comments"][k],"to",issue[a]["comments"][l]
                graph.add_edge(str(issue[a]["comments"][l]),str(issue[a]["comments"][l]))
    print ""
    
    
    #print "FORKS"
    #print ""
    #for f,i in enumerate(repository.get_forks()):
    #    print i.name
    #    print "ANALYSING A FORK, number",f
    #    print ""
    #    analyse_repo(i,f+1)
    #    print ""
    #print "-----"
    
    print "-----"
    print "PULL REQUESTS"
    print ""
    
    for i in repository.get_pulls():
        print i.id
        if i.assignee != None:
            print "Assignee:",i.assignee.login
        if i.user != None:
            print "User:",i.user.login
        print "Adding an edge from",i.user.login,"to",i.assignee.login
        graph.add_edge(str(i.user.login),str(i.assignee.login))
        
        # We should look at the comments on the pull request, but it seems not to be working now
        #for k,jj in enumerate(i.get_comments()):
        #    print "k=",k
        #    print "a",jj
        #    print "User comment a:",jj.user.login
        #    print jj.body
   
    print "-----"
  
 

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
    analyse_repo(b,0)
    
    # Getting rid of the node None, it was used to catch the errors of users that are NoneType
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