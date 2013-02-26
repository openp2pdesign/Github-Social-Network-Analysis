GitHub Social Network Analysis scripts
======================================

<img src="http://www.openp2pdesign.org/wordpress/wp-content/uploads/2013/02/opendesigndefinition-ego.png" alt="Social Network Analysis on GitHub"/>

Social Network Analisys of GitHub:
a collection of python scripts for mining GitHub social networks

License
-------
[GPL V.3](http://www.gnu.org/licenses/gpl-3.0.txt)


Description
-----------

1. **ego-network.py**: Ego-network search for followers and following users of a single user, Depth = 1
2. **ego-network-2levels.py**: Ego-network search for followers and following users of a single user, Depth = 2 (full name of the user is requested, very slow)
3. **ego-network-2levels-fast.py**: Ego-network search for followers and following users of a single user, Depth = 2 (only username of the user is requested, faster)
4. **organization_repository_analysis.py**: Analysis of an Organization repository, starting from a user. No graph is built
5. **organization_repository_social_mining.py**: Analysis of an Organization repository, starting from a user. A .gexf graph with multiple edges is built and saved
6. **organization_repository_social_mining_weighted.py**: Analysis of an Organization repository, starting from a user. A .gexf graph is built with weighted singular edges and saved
7. **organization_ego-network.py**: Ego-network search for followers and following users of all the members of an Organization, Depth = 1
8. **organization_ego-network-2levels.py**: Ego-network search for followers and following users of all the members of an Organization, Depth = 2
9. **single_repository_social_mining.py**: Analysis of a user repository, starting from a user. A .gexf graph with multiple edges is built and saved
10. **single_repository_social_mining_weighted.py**: Analysis of a user repository, starting from a user. A .gexf graph with weighted singular edges is built and saved


Requisites
----------
Install pyGithub with: 
*pip install PyGithub*

Install NetworkX with: 
*pip install networkx*