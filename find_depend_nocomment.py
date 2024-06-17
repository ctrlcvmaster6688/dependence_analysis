def read_config_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config_options = file.readlines()
    return {config.strip() for config in config_options}

def find_common_configs(file1, file2, output_file):
    # 读取第一个文件中的 config 选项
    isolated_configs = read_config_file(file1)
    # 读取第二个文件中的 config 选项
    undescribed_configs = read_config_file(file2)
    
    # 找到两个集合的交集，即共同的 config 选项
    common_configs = isolated_configs.difference(undescribed_configs)
    
    # 将共同的 config 选项写入新的文件
    with open(output_file, 'w', encoding='utf-8') as file:
        for config in common_configs:
            file.write(config + '\n')

def main():
    file1 = 'no_special_configs.txt'
    file2 = 'isolated_configs.txt'
    output_file = 'depend_but_nocomment.txt'
    
    find_common_configs(file1, file2, output_file)
    print(f"共同的 config 选项已写入到 {output_file}")

if __name__ == '__main__':
    main()
