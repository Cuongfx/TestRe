import json
import networkx as nx

# #############################################################
# 1) Load workpiece graph and feature graph data from json file
# #############################################################
def load_graph_from_json(json_path):
    """
    Loads a JSON file containing 'nodes' and 'edges' and returns a NetworkX Graph.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    G = nx.Graph()
    # Add nodes
    for node_info in data["nodes"]:
        node_id = node_info[0]
        node_attrs = node_info[1]
        G.add_node(node_id, **node_attrs)

    # Add edges
    for edge_info in data["edges"]:
        n1, n2, edge_attrs = edge_info
        G.add_edge(n1, n2, **edge_attrs)

    return G

# #################################
# 2) Create graphs from loaded data
# #################################

def node_match(n1_attrs, n2_attrs):
    """
    Example: match on 'type' exactly, ignoring other attributes.
    """
    return n1_attrs.get('type') == n2_attrs.get('type')

def edge_match(e1_attrs, e2_attrs):
    """
    Example: require 'angular_type' to match exactly.
    """
    return e1_attrs.get('angular_type') == e2_attrs.get('angular_type')


if __name__ == "__main__":

    workpiece_graph_path = "workpiece_graph.json"
    feature_graph_path   = "feature_graph.json"
    workpiece_graph = load_graph_from_json(workpiece_graph_path)
    feature_graph   = load_graph_from_json(feature_graph_path)

    print("Workpiece graph has:")
    print("  - {} nodes".format(workpiece_graph.number_of_nodes()))
    print("  - {} edges".format(workpiece_graph.number_of_edges()))

    print("Feature graph has:")
    print("  - {} nodes".format(feature_graph.number_of_nodes()))
    print("  - {} edges".format(feature_graph.number_of_edges()))

    # ############################################################
    # 3) Check if the feature graph is a subgraph of the workpiece
    #    and find any other matching subgraphs
    # ############################################################

    GM = nx.algorithms.isomorphism.GraphMatcher(
        workpiece_graph,
        feature_graph,
        node_match=node_match,
        edge_match=edge_match
    )

    matches = list(GM.subgraph_isomorphisms_iter())

    # ##########
    # 4) Results
    # ##########
    if len(matches) == 0:
        print("No subgraph match was found for the feature.")
    else:
        print("Number of matches found:", len(matches))
        for i, match_dict in enumerate(matches, 1):
            print(f"Match #{i}:")
            for feat_node, work_node in match_dict.items():
                print(f"  Feature node {feat_node} => Workpiece node {work_node}")
        print("\n(Shown above are all node mappings in each matched subgraph.)")