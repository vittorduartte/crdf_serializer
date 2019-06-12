from rdflib import URIRef, BNode, Literal
from rdflib import Graph
from rdflib import Namespace

def get_class_vars(cl):
    return {key:value for key, value in cl.__dict__.items() if not key.startswith('__') and not callable(key)}

class ObjectDecorator():

    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2


    def link_nodes (self, object):
        class_vars = get_class_vars(type(object))
        for k,v in object.__dict__.items():
            if (k != "_uri" and (isinstance(v, Literal) or isinstance(v, URIRef))) :
                object.g.add( (object._uri, class_vars[k], v) )

    def __call__(self, fun, *args, **kwargs):
        def inner_func(*args, **kwargs):
            args[0].g = Graph()
            obj = fun(*args, **kwargs)
            args[0]._uri = URIRef(self.arg1+args[0].id)
            args[0].g.add( (args[0]._uri, RDF.type, self.arg2) )
            self.link_nodes(args[0])
            return obj

        return inner_func

class BindDecorator ():

    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2


    def __call__(self, fun, *args, **kwargs):
        def inner_func(*args, **kwargs):
            args[0].g.bind(self.arg1, self.arg2)
            return fun(*args, **kwargs)
        return inner_func


def serialize_all (l):
    gtotal = Graph()
    for o in l:
        gtotal = gtotal + o.g
    return gtotal.serialize ().decode()