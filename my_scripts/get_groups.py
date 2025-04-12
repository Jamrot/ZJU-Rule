"""example:
proxy-groups:
- name: "proxy"
  type: select
  proxies:
  - DIRECT
  - ss
  use:
  - provider1
  - provider1

  url: 'https://www.gstatic.com/generate_204'
  interval: 300
  lazy: true
  timeout: 5000
  max-failed-times: 5

  disable-udp: true
  interface-name: en0
  routing-mark: 11451
  include-all: false
  include-all-proxies: false
  include-all-providers: false
  filter: "(?i)港|hk|hongkong|hong kong"
  exclude-filter: "美|日"
  exclude-type: "Shadowsocks|Http"
  expected-status: 204
  hidden: true
  icon: xxx
"""

BASIC_SETTING = """  url: 'https://www.gstatic.com/generate_204'
  interval: 300
  lazy: true
  max-failed-times: 5
  timeout: 3000
"""


def get_groups(filepath):
    groups = {}

    with open(filepath) as f:
        lines = f.readlines()
    
    for line in lines:
        if "custom_proxy_group=" in line:
            if "[]" in line:
                group = line.split("=")[-1].strip()
                group_name = group.split("`")[0]
                group_type = group.split("`")[1]
                group_groups = group.split("`")[2:]
                group_groups = [item.strip("[]") for item in group_groups if item]

                groups[group_name] = {
                    "name": group_name,
                    "type": group_type,
                    "groups": group_groups
                }
            elif ".*" in line:
                group = line.split("=")[-1].strip()
                group_name = group.split("`")[0]
                group_type = group.split("`")[1]
                groups[group_name] = {
                    "name": group_name,
                    "type": group_type
                }

            else:
                group = line.split("=")[-1].strip()
                group_name = group.split("`")[0]
                group_type = group.split("`")[1]
                group_filter = group.split("`")[2]
                # group_filter = group_filter.replace("(", "/").replace(")", "/")

                groups[group_name] = {
                    "name": group_name,
                    "type": group_type,
                    "filter": group_filter
                }

    return groups

def write_groups(groups):
    output_filepath = "groups.yaml"
    content = "proxy-groups:\n"

    for name, item in groups.items():
        content += f"- name: \"{item['name']}\"\n"
        content += f"  type: {item['type']}\n"
        content += BASIC_SETTING
        if "filter" in item:
            content += f"  include-all-proxies: true\n"
            content += f"  filter: \"{item['filter']}\"\n"
            content += f"  exclude-filter: \"倍|DIRECT|自动选择|节点选择|剩余流量|套餐到期\"\n"
        elif "groups" in item:
            content += f"  proxies:\n"
            for group in item["groups"]:
                content += f"  - {group}\n"
        else:
            content += f"  include-all-proxies: true\n"
            content += f"  exclude-filter: \"倍|DIRECT|自动选择|节点选择|剩余流量|套餐到期\"\n"
        content += "\n"

    with open(output_filepath, "w") as f:
        f.write(content)
    
    print(f"Groups have been written to {output_filepath}")

if __name__ == "__main__":
    filepath = "Clash/config/ZJU.ini"
    groups = get_groups(filepath)
    write_groups(groups)
