import click 
import parser
import kgcl_2_sparql
import graph_transformer 
import rdflib

import sys
sys.path.append("../")
import python.kgcl 

class Config(object):
    def __init__(self):
        self.verbose = False

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.command() 
@click.argument('kgcl', type=click.File('r'), required=True)
@click.argument('graph', type=click.Path(), required=True)
@click.argument('output', type=click.Path(), required=True)
@pass_config
def cli(config, kgcl, graph, output):
    
    #read kgcl commands from file
    kgcl_statements = kgcl.read()

    #parser kgcl commands
    parsed_statements = parser.parse(kgcl_statements)

    #apply kgcl commands as SPARQL UPDATE queries to graph
    g = rdflib.Graph()
    g.load(graph, format="nt") 
    graph_transformer.transform_graph(parsed_statements, g)
    #TODO: make this two steps?
    #first compute the SPARQL queries and
    #then apply them to the graph (both steps are currently done by the graph transformer)

    #save updated graph
    g.serialize(destination=output, format='nt') 

if __name__ == '__main__':
    cli()


