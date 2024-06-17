from collections import defaultdict

def read_graph(file_path):
    graph = defaultdict(list)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            source, target = line.strip().split(' -> ')
            graph[source].append(target)
    return graph

def has_cycle(graph):
    visited = set()
    stack = set()
    cycle_path = []

    def visit(node):
        if node in stack:
            cycle_path.append(node)
            return True
        if node in visited:
            return False
        stack.add(node)
        visited.add(node)
        cycle_path.append(node)
        for neighbor in graph[node]:
            if visit(neighbor):
                return True
        stack.remove(node)
        cycle_path.pop()
        return False

    for node in graph:
        if visit(node):
            cycle_start = cycle_path[-1]
            cycle = []
            while cycle_path:
                cycle_node = cycle_path.pop()
                cycle.append(cycle_node)
                if cycle_node == cycle_start and len(cycle) > 1:
                    break
            cycle.reverse()
            print("图中存在环:", " -> ".join(cycle))
            return True
    return False

def main():
    file_path = 'config_dependencies.txt'  # 替换为实际的文件路径
    graph = read_graph(file_path)
    if not has_cycle(graph):
        print("图中不存在环")

if __name__ == '__main__':
    main()
