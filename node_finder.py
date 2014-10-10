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

response = requests.get(list_url)

nodes = create_node_set(response)

del response

print len(nodes)
if len(nodes) == 206:
  print 'List scrape complete'

G = nx.DiGraph()

# n=0
for country in nodes:
  G.add_edges_from(edge_list(nodes[country], soup_adjacency(country,nodes)))
  print repr(nodes[country]), "added."
#   if n>=100:
#     break
#   n+=1
# print "Limited to", n
del nodes

nx.draw_circular(G, ax=None, node_size=20, node_color="k", width=0.01, edge_color="#3300cc", font_family="monospace", font_weight="bold", font_color="#33cc00", with_labels=True)
plt.axis('off')
plt.show()
