#    Copyright 2020 D-Wave Systems Inc.

# Imports both in modules and JN for users skipping sections
import matplotlib.pyplot as plt
import networkx as nx
import dimod 
import minorminer
import pandas as pd

def generate_ran1(variables, interactions, draw=True):
    "Generate a RAN1 problem on a random graph."
    
    G = nx.random_regular_graph(n=variables, d=interactions)
    bqm = dimod.generators.random.ran_r(1, G)
    
    if draw:
        if  variables*interactions > 2000: 
            figsize = (7, 7)  
        else:
            figsize = (4, 4)         
        plt.figure(figsize=figsize)
        nx.draw_networkx(G, pos=nx.spring_layout(G), with_labels=False, node_size=25) 
        plt.show()
            
    return bqm


def try_embedding(bqm, target_graphs, timeout=60, tries=2):
    "Attempt to embed a given binary quadratic model "
    
    max_len = {}
    for topology in target_graphs:
        
        embedding = minorminer.find_embedding(bqm.quadratic, 
                                          topology[1].edges, 
                                          timeout=timeout, 
                                          tries=tries)
        if not embedding:
            print("{}: failed to embed.".format(topology[0]))
            max_len[topology[0]] = 0
        else:
            max_len[topology[0]] = max([len(embedding[n]) for n in embedding])
            print("{}: found embedding with longest chain of {} qubits.".format(topology[0], max_len[topology[0]]))
            
    return max_len

def embedding_loop(nodes, edges, target_graphs, **params):
    "Loop over problem generation and embedding attempts."
    
    # Set configuration defaults
    problems = params.get('problems', 2)
    draw_problem = params.get('draw_problem', True)
    embedding_timeout = params.get('embedding_timeout', 60)
    embedding_tries = params.get('embedding_tries', 2)

    row = []
        
    for problem in range(problems):
        
        print("\nProblem {} of {} for {} nodes and {} edges:".format(
               problem + 1, problems, nodes, edges))
        
        bqm = generate_ran1(nodes, edges, draw_problem)
        row.append([nodes,
                    edges,
                    problem, 
                    try_embedding(bqm, target_graphs, embedding_timeout, embedding_tries)])

    return row 



