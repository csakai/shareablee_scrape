import requests, bs4, re, html5lib

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

for country in nodes:
  adjacency_matrix[nodes[country]] = soup_adjacency(country, nodes)
  print repr(nodes[country]), ":", repr(adjacency_matrix[nodes[country]])
print "\n"
print "All scraped at ", len(adjacency_matrix.keys()), "nodes."
