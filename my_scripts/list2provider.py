import os

def get_lists(dirpath):
    lists_dict = {}
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.endswith('.list'):
                name = file.split('.')[0]
                with open(os.path.join(root, file)) as f:
                    file_list = f.readlines()
                lists_dict[name] = process_single_file(file_list)

    return lists_dict

def process_single_file(file_list):
    # process the file content
    processed_list = []
    for item in file_list:
        # process the item
        if "#" not in item.strip() and item.strip():
            processed_list.append(item.strip())
    return processed_list

def write2yaml(lists_dict, root_dir):
    os.makedirs(root_dir, exist_ok=True)
    for name, items in lists_dict.items():
        with open(os.path.join(root_dir, name + ".yaml"), "w") as f:
            f.write("payload:\n")
            for item in items:
                f.write(f"  - {item}\n")

def write2provider(list_dict, root_dir, output_filepath):
    os.makedirs(root_dir, exist_ok=True)
    content = "rule-providers:\n"
    for rule_name, items in lists_dict.items():
        rule_path = os.path.join(root_dir, f"{rule_name}.yaml")
        if not os.path.exists(rule_path):
            print(f"Rule file {rule_path} does not exist.")
            continue
        content += f"  {rule_name}:\n"
        content += f"    type: file\n"
        content += f"    path: ./{rule_path}\n"
        # content += f"    url: \"https://raw.githubusercontent.com/ConnersHua/Profiles/master/Clash/RuleSet/{rule_name}.yaml\"\n"
        # content += f"    interval: 600\n"
        # content += f"    proxy: DIRECT\n"
        content += f"    behavior: classical\n"
        content += f"    format: yaml\n"
        # content += f"    size-limit: 0\n"
    
    with open(output_filepath, "w") as f:
        f.write(content)
    
    print(f"Rule providers have been written to {output_filepath}")

if __name__ == "__main__":
    dirpath = "Clash"
    lists_dict = get_lists(dirpath)
    write2yaml(lists_dict, "output")
    write2provider(lists_dict, "output", "rule_providers.yaml")
    