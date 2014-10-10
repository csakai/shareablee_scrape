import requests, bs4, html5lib, networkx as nx, matplotlib.pyplot as plt

base_url = 'http://en.wikipedia.org'
list_url = base_url +'/wiki/List_of_sovereign_states'

def create_node_set(response):
  links = bs4.BeautifulSoup(response.text, "html5lib").select('table.wikitable.sortable tr > td > b > a[href^=/wiki/]')
  nodes = {}
  for link in links:
    node = get_country(link)
    nodes[node[0]] = node[1]
  return nodes

def get_country(link):
  return (link.attrs.get('href'), link.attrs.get('title'))

def soup_adjacency(country_slug, nodes):
  try:
    page = requests.get(base_url + country_slug)
    links = bs4.BeautifulSoup(page.text, "html5lib").select('a[href^=/wiki/]')
    edges = [nodes[a.attrs.get('href')] for a in links if a.attrs.get('href') and a.attrs.get('href') in nodes.keys()]
  except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
    edges = list(soup_adjacency(country_slug, nodes))
  finally:
    if not edges:
      edges = []
  return set(edges)

def edge_list(country, node_set):
  return [(country, node) for node in node_set]

def list_single_ended(country, matrix):
  return set([dest for dest in matrix[country] if country not in matrix[dest]])

def list_double_ended(country, matrix):
  return set([dest for dest in matrix[country] if country in matrix[dest]])

response = requests.get(list_url)

nodes = create_node_set(response)

del response

print len(nodes)
if u'Transnistria' in nodes.values():
  print 'Transnistria in. It works.'

adjacency_matrix = {}

n=0
for country in nodes:
  adjacency_matrix[nodes[country]] = soup_adjacency(country, nodes)
  print repr(nodes[country]), ":", len(adjacency_matrix[nodes[country]])
  if n>=5:
    break
  n+=1
del nodes
print "\n"
#print "All scraped at ", len(adjacency_matrix.keys()), "nodes."
print "Limited to 5"

G = nx.DiGraph()
G.add_nodes_from(adjacency_matrix.keys())
for country in adjacency_matrix:
  G.add_edges_from(edge_list(country, adjacency_matrix[country]))

nx.draw_circular(G, with_labels=True)
plt.show()
