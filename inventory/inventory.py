#!/usr/bin/python3
import json
import os

import yaml


class Instance:
    def __init__(self, instance_name: str, hostvars: dict, groups: list):
        self.instance_name = instance_name
        self.hostvars = hostvars
        self.groups = groups

    def get_hostvar(self):
        return {self.instance_name: self.hostvars}

    def get_instance_name(self):
        return self.instance_name

    def get_groups(self):
        return self.groups


def parse_custom_inventory(file_path):
    instances = []

    with open(file_path, "r") as file:
        custom_inventory = yaml.safe_load(file)

        for instance_name in custom_inventory:
            instances.append(Instance(instance_name, custom_inventory[instance_name]["hostvars"],
                                      custom_inventory[instance_name]["groups"]))

    return instances


def fill_inventory(inventory: dict, instances: list[Instance]):
    for instance in instances:
        instance_name = instance.get_instance_name()
        hostvars = instance.get_hostvar()
        groups = instance.get_groups()

        inventory["_meta"]["hostvars"][instance_name] = hostvars[instance_name]
        inventory["all"].append(instance_name)

        for group in groups:
            if group not in inventory:
                inventory[group] = []
            inventory[group].append(instance_name)

    inventory["all"] = list(set(inventory["all"]))


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = f"{script_dir}/hosts.yaml"
    inventory = {"_meta": {"hostvars": {}}, "all": []}

    instances = parse_custom_inventory(file_path)
    fill_inventory(inventory, instances)
    print(json.dumps(inventory))


if __name__ == "__main__":
    main()
