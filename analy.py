import re

# 定义正则表达式模式
config_pattern = re.compile(r'^(config|menuconfig) (\w+)')
help_pattern = re.compile(r'^\s*help')
comment_pattern = re.compile(r'^\s*#')
depends_pattern = re.compile(r'^\s*(depends on|select) (.+)')

# 统计 Kconfig 文件中的配置项数量和特性
def count_config_features(file_path, output_file):
    total_configs = 0  # 总的 config 数量
    with_help = 0  # 带有帮助文本的 config 数量
    with_comment = 0  # 带有注释的 config 数量
    with_depends_on = 0  # 带有依赖关系的 config 数量
    nothing_special = 0  # 既没有帮助文本和注释，也没有依赖关系的 config 数量
    nothing_special_configs = []  # 记录 nothing_special 的 config 项

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_config = None  # 当前处理的配置项名称
    has_help = False
    has_comment = False
    has_depends_on = False

    for line in lines:
        line = line.strip()
        config_match = config_pattern.match(line)
        if config_match:
            # 处理上一个配置项
            if current_config:
                total_configs += 1
                if has_help:
                    with_help += 1
                if has_comment:
                    with_comment += 1
                if has_depends_on:
                    with_depends_on += 1
                if not (has_help or has_comment or has_depends_on):
                    nothing_special += 1
                    nothing_special_configs.append(current_config)
            
            # 初始化新配置项
            current_config = config_match.group(2)
            has_help = False
            has_comment = False
            has_depends_on = False
        else:
            if help_pattern.match(line):
                has_help = True
            elif comment_pattern.match(line):
                has_comment = True
            elif depends_pattern.match(line):
                has_depends_on = True
    
    # 处理最后一个配置项
    if current_config:
        total_configs += 1
        if has_help:
            with_help += 1
        if has_comment:
            with_comment += 1
        if has_depends_on:
            with_depends_on += 1
        if not (has_help or has_comment or has_depends_on):
            nothing_special += 1
            nothing_special_configs.append(current_config)
    
    # 将 nothing_special 的 config 项写入文件
    with open(output_file, 'w', encoding='utf-8') as file:
        for config in nothing_special_configs:
            file.write(config + '\n')
    
    return total_configs, with_help, with_comment, with_depends_on, nothing_special

# 主程序
if __name__ == '__main__':
    kconfig_file = 'all.txt'  # 替换为实际的 Kconfig 文件路径
    output_file = 'nothing_special_configs.txt'  # 输出文件路径
    total_configs, with_help, with_comment, with_depends_on, nothing_special = count_config_features(kconfig_file, output_file)
    
    # 输出统计信息
    print(f"总的 config 数量: {total_configs}")
    print(f"带有帮助文本的 config 数量: {with_help}")
    print(f"带有注释的 config 数量: {with_comment}")
    print(f"带有依赖关系的 config 数量: {with_depends_on}")
    print(f"既没有帮助文本和注释，也没有依赖关系的 config 数量: {nothing_special}")
    print(f"nothing_special 的 config 项已写入到 {output_file}")
