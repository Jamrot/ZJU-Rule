import os

def process_ini_file(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    
    ruleset_dict = {}

    for line in lines:
        if "ruleset=" in line:
            ruleset = line.split("=")[-1].strip()
            rule_label = ruleset.split(",")[0]
            rule_url = ruleset.split(",")[1]
            rule_name = rule_url.split("/")[-1].split(".")[0]

            ruleset_dict.setdefault(rule_label, []).append(rule_name)
    
    return ruleset_dict

def write2tmp(ruleset_list):
    for label, rules in ruleset_list.items():
        with open(f"tmp.txt", "a") as f:
            f.write(f"{label}:\n")
            for rule in rules:
                f.write(f"  - {rule}\n")

def write2yaml(ruleset_list, output_dir):
    """example:
    rule-providers:
        google:
            type: http
            path: ./rule1.yaml
            url: "https://raw.githubusercontent.com/../Google.yaml"
            interval: 600
            proxy: DIRECT
            behavior: classical
            format: yaml
            size-limit: 0"""
    os.makedirs(output_dir, exist_ok=True)
    output_filepath = "rule_providers_ini.yaml"
    content = "rule-providers:\n"
    for label, rule_names in ruleset_list.items():
        for rule_name in rule_names:
            rule_path = os.path.join(output_dir, f"{rule_name}.yaml")
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
    filepath = "Clash/config/ZJU.ini"
    ruleset_list = process_ini_file(filepath)
    print(ruleset_list.keys())
    write2tmp(ruleset_list)
    write2yaml(ruleset_list, "output")