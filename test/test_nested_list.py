from delimited import NestedDict as ndict
from delimited.container import ListIndex as index
import pprint

data = {("k1", "k2", index(0), "name"): "Chris Antonellis"}
pprint.pprint(data)

expanded = ndict._expand(data)
pprint.pprint(expanded)

collapsed = ndict._collapse(expanded)
pprint.pprint(collapsed)