import argparse
import csv


class Node(object):
    def __init__(self, label, cost=0, parent=None):
        self.label = label
        self.cost = int(cost)
        self.parent = parent

    def __eq__(self, other):
        if not other:
            return False
        return self.label == other.label

    def __repr__(self):
        return "{}.{}".format(self.label, self.cost)


class Uniform(object):
    def __init__(self, file_name, start_node, end_node):
        self.graph = self.load_graph(file_name)
        self.start_node = Node(start_node)
        self.end_node = Node(end_node)

        self.expanded_list = []
        self.priority_list = []

    def load_graph(self, file_name):
        graph = {}
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                if line[0] not in graph:
                    graph[line[0]] = []
                if line[1] not in graph:
                    graph[line[1]] = []
                graph[line[0]].append(dict(label=line[1], cost=int(line[2])))
                graph[line[1]].append(dict(label=line[0], cost=int(line[2])))
        return graph

    def valid_to_expand(self, node):
        if node in self.expanded_list:
            return False
        return True

    def find_path(self, node):
        path = [node]
        while(True):
            node = node.parent
            if node is None:
                break
            path.append(node)
        path.reverse()
        return path

    def run(self):
        self.priority_list.append(self.start_node)

        count = 0
        while(len(self.priority_list) > 0):
            count += 1

            self.priority_list = sorted(self.priority_list, key=lambda x: x.cost)
            expanding_node = self.priority_list.pop(0)

            if not self.valid_to_expand(expanding_node):
                continue

            self.expanded_list.append(expanding_node)

            if self.end_node in self.expanded_list:
                break

            children_node = self.graph.get(expanding_node.label, [])
            for child in children_node:
                child_node = Node(child['label'], expanding_node.cost + child['cost'], expanding_node)

                if not expanding_node.parent or expanding_node.parent != child_node:
                    self.priority_list.append(child_node)

        last_expended_node = self.expanded_list[-1]
        if last_expended_node == self.end_node:
            path = self.find_path(last_expended_node)
            return path
        else:
            return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find shortest route.')
    parser.add_argument('--file', type=str, help='file name')
    args = parser.parse_args()

    start_node = input("What is start node?: ")
    end_node = input("What is goal node?: ")

    path = Uniform(args.file, start_node, end_node).run()
    print()
    if path:
        # print("Result: Your Trip from {} to {} include {} stops, and will take {} minutes".format(
        #     start_node, end_node, len(path) - 2, path[-1].cost
        # ))
        path_labels = "->".join([n.label for n in path])
        print("Path from {} to {} is {}, and have cost {}.".format(start_node, end_node, path_labels, path[-1].cost))
    else:
        print("Result: No Routes from {} to {}".format(start_node, end_node))
