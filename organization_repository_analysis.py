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

def analyse_repo(repository):
    
    print "-----"
    print "DESCRIPTION:",repository.description
    print "-----"
    print "OWNER:",repository.owner.login
    print "-----"
    print "WATCHERS:",repository.watchers
    for i in repository.get_stargazers():
        if i != None:
            print "-",i.login
    print "-----"
    print "COLLABORATORS"
    for i in repository.get_collaborators():
        if i != None:
            print "-",i.login
    print "-----"
    print "HAS ISSUES=",repository.has_issues
    if repository.has_issues == True:
        print "-----"
        print "ISSUES: Open ones"
        for i in repository.get_issues(state="open"):
            if i.user != None:
                print "- Created by", i.user.login
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
    print "-----"
    print "COMMITS"
    for i in  repository.get_commits():
        print "-",i.sha
        if i.committer != None:
            print "-- by",i.committer.login
    print "-----"
    print "FORKS"
    for i in repository.get_forks():
        print i.name
        print "ANALYSING A FORK"
        print ""
        analyse_repo(i)
        print ""
    print "-----"

    return


if __name__ == "__main__":
    print "Basic Analisys of your GitHub Organization"
    print ""
    userlogin = raw_input("Login: Enter your username: ")
    password = getpass.getpass("Login: Enter yor password: ")
    username = raw_input("Enter the username you want to analyse: ")
    print ""
    g = Github( userlogin, password )
    
    
    graph = nx.DiGraph()
    
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
    