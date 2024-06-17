import requests
import re

# 读取包含config项的文档
config_file = 'depend_but_nocomment.txt'
write_file = 'config_with_1stversion'
# 读取文档中的config项
with open(config_file, 'r', encoding='utf-8') as f:
    config_items = f.read().splitlines()

# 目标网址的模板
base_url = 'https://cateee.net/lkddb/web-lkddb/{}.html'

# 正则表达式模式
pattern = r'found in Linux kernels: ([\d\.\–\s]+?-rc\+HEAD|[\d\.\–\s]+)'

# 遍历每个config项，访问网址并获取信息
for config in config_items:
    # 构建完整的URL
    url = base_url.format(config)
    
    # 发起GET请求
    response = requests.get(url)
    
    if response.status_code == 200:
        # 使用正则表达式查找版本信息
        match = re.search(pattern, response.text)
        
        if match:
            # 提取版本信息
            found_in_kernels = match.group(1).strip()
            
            # 打印信息
            print(f"{config}: {found_in_kernels}")
            
            # 如果需要将信息写入文件，可以在这里实现
            # 例如，将信息追加写入到原始文档中
            with open(write_file, 'a', encoding='utf-8') as f:
                f.write(f"{config}: {found_in_kernels}\n")
        
        else:
            print(f"Cannot find 'found in Linux kernels' for {config}")

    else:
        print(f"Failed to fetch {config}. Status code: {response.status_code}")
