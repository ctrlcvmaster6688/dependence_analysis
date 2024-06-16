import re
import networkx as nx
import matplotlib.pyplot as plt

# 定义正则表达式模式
config_pattern = re.compile(r'^config (\w+)')
depends_pattern = re.compile(r'^\s*(depends on|select) (.+)')

def parse_kconfig(file_path):
    dependencies = {}
    configs = set()

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_config = None

    for line in lines:
        line = line.strip()
        config_match = config_pattern.match(line)
        if config_match:
            current_config = config_match.group(1)
            configs.add(current_config)
            dependencies[current_config] = []
        elif current_config:
            depends_match = depends_pattern.match(line)
            if depends_match:
                depends_type = depends_match.group(1).strip()
                depends_on = depends_match.group(2).split()
                if depends_type == 'depends on' or depends_type == 'select':
                    for dep in depends_on:
                        if dep in ['&&', '||', '!']:
                            continue
                        dependencies[current_config].append(dep.strip('()'))
    
    return configs, dependencies

def build_dependency_graph(configs, dependencies):
    G = nx.DiGraph()
    G.add_nodes_from(configs)
    
    for config, deps in dependencies.items():
        for dep in deps:
            if dep in configs: 
                G.add_edge(dep, config)
    
    return G

def find_isolated_configs(G):
    # 找到没有任何依赖和被依赖的config
    isolated_configs = [node for node in G.nodes if G.in_degree(node) == 0 and G.out_degree(node) == 0]
    return isolated_configs

def output_dependencies(file_path, dependencies):
    with open(file_path, 'w', encoding='utf-8') as file:
        for config, deps in dependencies.items():
            for dep in deps:
                file.write(f"{dep} -> {config}\n")

def main():
    kconfig_file = 'all.txt'
    configs, dependencies = parse_kconfig(kconfig_file)
    
    G = build_dependency_graph(configs, dependencies)
    
    isolated_configs = find_isolated_configs(G)
    
    # 输出孤立的 config 项到文件
    with open('isolated_configs.txt', 'w', encoding='utf-8') as output_file:
        for config in isolated_configs:
            output_file.write(config + '\n')
    
    # 输出依赖关系到文件
    output_dependencies('config_dependencies.txt', dependencies)
    
    # 打印并输出统计信息
    total_configs = len(configs)
    isolated_configs_count = len(isolated_configs)
    with_depends_on = sum(1 for deps in dependencies.values() if deps)
    
    print(f"总的 config 数量: {total_configs}")
    print(f"带有依赖关系的 config 数量: {with_depends_on}")
    print(f"孤立的 config 数量: {isolated_configs_count}")
    
    with open('config_statistics.txt', 'w', encoding='utf-8') as stats_file:
        stats_file.write(f"总的 config 数量: {total_configs}\n")
        stats_file.write(f"带有依赖关系的 config 数量: {with_depends_on}\n")
        stats_file.write(f"孤立的 config 数量: {isolated_configs_count}\n")

    # 绘制有向图
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)  # 用 spring layout 布局图
    nx.draw(G, pos, with_labels=True, node_size=50, font_size=8, arrows=True)
    plt.title('Linux Kernel Config Dependencies')
    plt.show()

if __name__ == '__main__':
    main()
