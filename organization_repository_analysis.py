#
# Social network analysis of an Organization repository in GitHub
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


a = org.get_repo(repo_to_mine)
print "-----"
print "DESCRIPTION:",a.description
print "-----"
print "COLLABORATORS"
for i in a.get_collaborators():
    print "-",i.login
print "-----"
print "HAS ISSUES=",a.has_issues
if a.has_issues == True:
    print "-----"
    print "ISSUES"
    for i in a.get_issues():
        print "- Created by", i.user.login
        print "--",i.title
        print "--",i.comments,"comments"
        for f in i.get_comments():
            print "--- With a comment by",f.user.login
        print ""        
print "-----"
print "CONTRIBUTORS"
for i in a.get_contributors():
    print "-", i.login
print "-----"
print "FORKS"
for i in a.get_forks():
    print i.name
print "-----"

