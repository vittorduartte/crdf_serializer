from rdflib import Namespace, Literal, URIRef
from crdf_serializer import ObjectDecorator, BindDecorator, graph
from rdflib.namespace import DC, FOAF

vcard = Namespace('https://www.w3.org/2006/vcard/ns#') #Trazendo uma nova ontologia
n = Namespace("http://linkedscience.org/teach/ns#")

class Curso ():

    # os nomes dessas variaveis de classe, precisam ser os mesmos das de instancia
    title = n.courseTitle
    image = vcard.hasPhoto

    @ObjectDecorator(n.Course, "http://lud.ufma.br/course/")
    @BindDecorator("teach", n)
    @BindDecorator("vcard", vcard)
    def __init__(self, id, title):
        self.id = id
        self.title = Literal(title)
        self.image = URIRef('urlimg')
 

c1 = Curso("1","Computação")
c2 = Curso("2", "Mecanica")
print( graph([c1,c2]).serialize(format='n3') ) # serializando todos
print( graph(c1).serialize(format='n3') ) # serializando um apenas


# exemplo do rdflib
'''
g = Graph()

# Create an identifier to use as the subject for Donna.
donna = BNode()

# Add triples using store's add method.
g.add( (donna, RDF.type, FOAF.Person) )
g.add( (donna, FOAF.nick, Literal("donna", lang="foo")) )
g.add( (donna, FOAF.name, Literal("Donna Fales")) )
g.add( (donna, FOAF.mbox, URIRef("mailto:donna@example.org")) )

# Bind a few prefix, namespace pairs for more readable output
g.bind("dc", DC)
g.bind("foaf", FOAF)

print( g.serialize(format='n3') )
'''

class Person:
    nick = FOAF.nick
    name = FOAF.name
    email = FOAF.mbox

    @ObjectDecorator(FOAF.Person, None) # blank node
    @BindDecorator("dc", DC)
    @BindDecorator("foaf", FOAF)
    def __init__ (self, name, nick, email):
        self.nick = Literal(nick, lang="foo")
        self.name = Literal (name)
        self.email = URIRef(email) 

p = Person ("Donna Fales","donna", "mailto:donna@example.org")
print( graph(p).serialize(format='n3') )

