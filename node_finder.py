import requests, bs4, wikipedia, re, html5lib, random

base_url = 'http://en.wikipedia.org'
list_url = base_url +'/wiki/List_of_sovereign_states'

# def chunk_to_string(url):
#   r = requests.get(url, stream=True)
#   s = ""
#   checking=""
#   for chunk in r.iter_content(chunk_size=1024):
#     if chunk:
#       if not checking and not s:
#         checking = chunk
#       elif checking and not s:
#         checking, s = init_table(checking, chunk)
#       else:
#         s += checking
#         if ends_table(checking, chunk):
#           # print checking, chunk
#           s += chunk
#           break
#         else:
#           checking = chunk
#   return isolate_table(s)

# def init_table(chunk1, chunk2):
#   if '<table class="sortable wikitable' in chunk1+chunk2:
#     return chunk2, chunk1+chunk2
#   else:
#     return chunk2, ""

# def ends_table(chunk1, chunk2):
#   return '</table>' in chunk1+chunk2

# def isolate_table(bulk):
#   pattern = re.compile("<table.*>")
#   return "<html><head></head><body><table>"+re.split(pattern, bulk)[2]+"</body></html>"

# def download_file(url):
#   local_filename = url.split('/')[-1]
#   # NOTE the stream=True parameter
#   r = requests.get(url, stream=True)
#   with open(local_filename, 'wb') as f:
#     for chunk in r.iter_content(chunk_size=1024):
#       if chunk: # filter out keep-alive new chunks
#         f.write(chunk)
#         f.flush()
#   return local_filename

def create_node_set(table):
  nodes = {}
  for row in table.findAll('tr'):
    first_cell = row.find('td')
    if first_cell and has_flag(first_cell):
      chref = get_country(first_cell)
      nodes[chref[0]] = chref[1]
  return nodes

def has_flag(cell):
  return True if cell.find('span', { 'class' : 'flagicon' }) else False

def get_country(cell):
  result = cell.find('a')
  return (result.attrs.get('title'), result.attrs.get('href'))

# def find_adjacency(country, nodes):
#   out = set(wikipedia.page(country).links)
#   return out & nodes

def soup_adjacency(country, node_set):
  page = requests.get(base_url + country)
  links = bs4.BeautifulSoup(page.text, "html5lib").find_all("a")
  return set([a.attrs.get('title') for a in links if a.attrs.get('title') and a.attrs.get('title') in node_set])

def list_double_ended(country, matrix):
  return set([dest for dest in matrix[country] if country in matrix[dest]])
# bulk = chunk_to_string(list_url)

bulk = requests.get(list_url).text

table = bs4.BeautifulSoup(bulk, "html5lib").find("table", {"class" : "sortable wikitable" })

nodes = create_node_set(table)

node_set = set(nodes.keys())

# def test_country(country, nodes=nodes):
#   print country
#   print find_adjacency(country, nodes), "\n"

# def weird_happens(country, nodes=nodes):
#   return not find_adjacency(country, nodes)

# title attribute of a tags may save some time.

if u'Transnistria' in nodes:
  print 'Transnistria in. It works.'

def test_soup(country, node_set=node_set):
  print country[6:]
  test = soup_adjacency(country, node_set)
  print sorted(test)

adjacency_matrix = {}

for country in nodes:
  adjacency_matrix[country] = soup_adjacency(nodes[country], node_set)
  print repr(country), ":", repr(adjacency_matrix[country])
print "\n"
print "All scraped at ", len(adjacency_matrix.keys()), "nodes."

# weirdos = []
# for country in nodes:
#   print repr(country),
#   if weird_happens(country):
#     print "!!",
#     weirdos += [country]
#   print "\n"

# print weirdos
