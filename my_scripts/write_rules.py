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

def set_rules_from_ini(ruleset_list, output_filepath):
    """example:
    const newRules = [
        "RULE-SET,OneDrive,国际媒体",
        ];
    """

    content = "const newRules = [\n"
    for label, rule_names in ruleset_list.items():
        for rule_name in rule_names:
            if rule_name=="[]FINAL":
                content += f"    \"MATCH,{label}\",\n"
            elif rule_name=="[]GEOIP":
                content += f"    \"GEOIP,CN,DIRECT\",\n"
            else:
                content += f"    \"RULE-SET,{rule_name},{label}\",\n"
    content += "];"

    with open(output_filepath, "w") as f:
        f.write(content)

    print(f"Rules have been written to {output_filepath}")

if __name__ == "__main__":
    output_filepath = "rules.js"
    ini_filepath = "Clash/config/ZJU.ini"
    ruleset_dict = process_ini_file(ini_filepath)
    set_rules_from_ini(ruleset_dict, output_filepath)