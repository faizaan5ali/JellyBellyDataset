import csv
import ast
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
def load_beans(bean_csv):
    """Load beans.csv into a dict: {flavorName: backgroundColor}"""
    bean_dict = {}
    with open(bean_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            flavor = row.get("flavorName")
            color = row.get("backgroundColor", "#CCCCCC")  # fallback color
            if flavor:
                bean_dict[flavor.lower()] = color
    return bean_dict

def build_graph(csv_file, bean_dict):
    """Build a flavor combination graph with colors from bean_dict."""
    G = nx.Graph()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            combo_id = row['combinationId']
            combo_name = row['name']
            tag_str = row['tag']

            try:
                # Parse stringified list safely
                flavors = [fl.lower() for fl in ast.literal_eval(tag_str) if fl != '+']
            except Exception:
                print(f"Could not parse tags for combo {combo_id}: {tag_str}")
                continue

            # Add nodes with colors, and edges for pairs
            for i in range(len(flavors)):
                for j in range(i + 1, len(flavors)):
                    # Only add edge if BOTH flavors exist in bean_dict
                    if flavors[i] in bean_dict and flavors[j] in bean_dict:
                        for flavor in (flavors[i], flavors[j]):
                            if not G.has_node(flavor):
                                color = bean_dict.get(flavor)
                                G.add_node(flavor, color=color)
                        if flavors[i] != flavors[j]:
                            G.add_edge(flavors[i], flavors[j], combo=combo_name)

    return G

def plot_graph(G, title="Flavor Combination Network"):
    plt.figure(figsize=(16, 12))
    pos = nx.spring_layout(G, k=0.8, iterations=200, seed=42)
    pos = nx.kamada_kawai_layout(G)

    # Extract node colors from attributes
    node_colors = [G.nodes[n].get("color", "#CCCCCC") for n in G.nodes]

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2000, edgecolors="black")
    nx.draw_networkx_edges(G, pos, edge_color="gray")
    nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif")

    plt.title(title)
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    beans = load_beans("output/beans.csv")
    for bean in beans:
        print(bean)
    graph = build_graph("output/combinations.csv", beans)
    print(f"Graph built with {graph.number_of_nodes()} flavors and {graph.number_of_edges()} edges.")
    plot_graph(graph)
