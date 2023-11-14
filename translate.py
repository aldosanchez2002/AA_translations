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

def translationPath(in_codec, out_codec, graph):
    if in_codec == out_codec:
        return [], 0
    path, cost = dijkstraMST(graph, in_codec, out_codec)
    #print(graph)
    return path, cost

def edgesToGraph(edges_dict):
    graph = {}
    for source_dest, cost in edges_dict.items():
        source, dest = source_dest
        if source not in graph:
            graph[source] = {}
        graph[source][dest] = (cost, [source, dest])
    return graph

def dijkstraMST(graph, start, end):
    min_cost = dict()
    for node in graph.keys():
        min_cost[node] = float('inf')
        
    min_cost[start] = 0
    visited = set()
    prev, node = None, start
    MST = {}
    while end not in visited:
        visited.add(node)
        MST[node] = prev
        path = get_path(MST, start, end)
        if graph[start] == None:
          graph[start][end] = (min_cost[end], path)
        elif end not in graph[start]:
          graph[start][end] = (min_cost[end], path)
        elif graph[start][end][0] >min_cost[end]:
          graph[start][end] = (min_cost[end], path)


        prev = node
        for neighbor, cost_path in graph[node].items():
            cost, path = cost_path
            min_cost[neighbor] = min(min_cost[node] + cost, min_cost[neighbor])
        node = choose_node(min_cost, visited)
        if not node:
            break
    MST[node] = prev
    # print(MST)
    # print(min_cost)
    # print(MST[start],MST[end])
    # print(min_cost[start],min_cost[end])

    path = get_path(MST, start, end)
    graph[start][end] = (min_cost[end], path)
    return path, min_cost[end]

def get_path(MST, start, end):
    if end not in MST:
        return []
    path = []
    node = end
    visited = set()
    while node != start:
        if node in visited:
            return []  # Node already in path, return empty path
        path.append(node)
        visited.add(node)
        node = MST[node]
    path.append(start)
    path.reverse()
    return path


def choose_node(min_cost, visited):
    min_cost_node = None
    min_cost_value = float('inf')
    for node, cost in min_cost.items():
        if node not in visited and cost < min_cost_value:
            min_cost_node = node
            min_cost_value = cost
    return min_cost_node

def test0():
    langs = ['alaw', 'ulaw', 'slin', 'g722', 'slin16', 'g729', 'g7222', 'g723', 'clearmode', 'lpc10', 'ilbc', 'speex', 'speex16', 'g726', 'gsm']
    ans0 = []
    for lang1 in langs:
        for lang2 in langs:
            if lang1 != lang2:
                graph = edgesToGraph(translators)
                path, cost = translationPath(lang1, lang2, graph)
                if cost == float('inf'):
                    print("No translation path was found from {} to {}.".format(lang1, lang2))
                    ans0.append("NO")
                else:
                    print("From {} to {}, \n\tPath: {} \n\tMinCost {}.".format(lang1, lang2, "->".join(path), cost))
                    ans0.append(cost)
    return ans0

if __name__ == '__main__':
    ans0 = test0()
    # if len(sys.argv) < 3:
    #     print("Not enough arguments. Give input and output codec.")
    #     sys.exit(1)
    # try:
    #     path, cost = translation_path(sys.argv[1], sys.argv[2])
    #     print("The translation path from {} to {} goes starts at {}, passes through the intermediate codecs {} and ends up at {}, all with a cost of {}.".format(sys.argv[1], sys.argv[2], sys.argv[1], path, sys.argv[2], cost))
    # except:
    #     print("No translation path was found for a {} to {} conversion.".format(sys.argv[1], sys.argv[2]))
    #     sys.exit(1)
