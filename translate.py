#! /usr/bin/env python3
import sys

translators = { ("alaw", "ulaw") : 1,
                ("ulaw", "alaw") : 1,
                ("alaw", "slin") : 2,
                ("slin", "alaw") : 2,
                ("ulaw", "slin") : 2,
                ("slin", "ulaw") : 2,
                ("g722", "slin16") : 3,
                ("slin16", "g722") : 4,
                ("slin16", "slin") : 2,
                ("slin", "slin16") : 2,
                ("g729", "slin") : 5,
                ("slin", "g729") : 5,
                ("g7222", "slin16") : 6,
                ("slin16", "g7222") : 6,
                ("g723", "slin") : 7,
                ("slin", "g723") : 7,
                ("clearmode", "alaw") : 1,
                ("alaw", "clearmode") : 1,
                ("lpc10", "ulaw") : 10,
                ("ulaw", "lpc10") : 10,
                ("ilbc", "slin") : 11,
                ("slin", "ilbc") : 11,
                ("speex", "slin") : 12,
                ("slin", "speex") : 12,
                ("speex", "speex16") : 13,
                ("speex16", "speex") : 13,
                ("speex16", "slin16") : 14,
                ("slin16", "speex16") : 14,
                ("g726", "g722") : 5,
                ("g722", "g726") : 5,
                ("gsm", "slin") : 6,
                ("slin", "gsm") : 6
               }

def translation_path(in_codec, out_codec):
    if in_codec == out_codec:
        return [], 0
    graph = edges_to_graph(translators)
    print(graph)
    path, cost = dijstras_shortest_path(graph, in_codec, out_codec)
    return path, cost

def edges_to_graph(edges_dict):
    graph = {} 
    for source_dest,cost in edges_dict.items():
        source,dest = source_dest
        if source not in graph:
            graph[source] = {}
        graph[source][dest] = cost
    # print([x for x in graph.keys()])
    # for k,v in graph.items():
    #     print(k,v)
    return graph

def dijstras_shortest_path(graph, start, end):
    min_cost = {}
    for node in graph.keys():
        min_cost[node] = float('inf')
    min_cost[start] = 0
    visited = set()
    MST = {}
    prev = None
    while min_cost[end] == float('inf'):
        print("\n",min_cost)
        node = chooseNode(min_cost, visited)
        MST[node] = prev
        prev = node
        visited.add(node)
        for neighbor, cost in graph[node].items():
            min_cost[neighbor] = min(min_cost[node] + cost, min_cost[neighbor])
    MST[node] = prev   
    path = get_path(MST, start, end)
    return path, min_cost[end]

def get_path(MST, start, end):
    print(MST)
    path = []
    node = end
    while node != start:
        path.append(node)
        node = MST[node]
    path.append(start)
    path.reverse()
    return path

def chooseNode(min_cost, visited):
    min_cost_node = None
    min_cost_value = float('inf')
    for node, cost in min_cost.items():
        if node not in visited and cost < min_cost_value:
            min_cost_node = node
            min_cost_value = cost
    return min_cost_node

def test():
    langs= ['alaw', 'ulaw', 'slin', 'g722', 'slin16', 'g729', 'g7222', 'g723', 'clearmode', 'lpc10', 'ilbc', 'speex', 'speex16', 'g726', 'gsm']
    for lang1 in langs:
        for lang2 in langs:
            if lang1 != lang2:
                path, cost = translation_path(lang1, lang2)
                if cost == float('inf'):
                    continue
                    print("No translation path was found from {} to {}.".format(lang1, lang2))
                else:
                    print("From {} to {}\t, Path:{},  \tMin Cost {}.".format(lang1, lang2, path, cost))

if __name__ == "__main__":
    test()
    sys.exit(0)
    if len(sys.argv) < 3:
        print("Not enough arguments. Give input and output codec.")
        sys.exit(1)
    try:
        path, cost = translation_path(sys.argv[1], sys.argv[2])
        print("The translation path from {} to {} goes starts at {}, passes through the intermediate codecs {} and ends up at {}, all with a cost of {}.".format(sys.argv[1], sys.argv[2], sys.argv[1], path, sys.argv[2], cost))
    except:
        print("No translation path was found for a {} to {} conversion.".format(sys.argv[1], sys.argv[2]))
        sys.exit(1)
    sys.exit(0)