import yaml
from collections import OrderedDict


def convert_policies(acl_policies):
    new_acl_policies = []
    for policy in acl_policies:
        new_policy = {}
        # Set the description element
        new_policy['description'] = policy['description']

        # Set the context element to new format
        new_policy['context'] = {}
        new_policy['context'][policy['context']['type']] = policy['context']['rule']

        # Build the group element from groups
        new_policy['by'] = []
        ug_policy = {}
        ug_policy['group'] = []
        for group in policy['by']['groups']:
            ug_policy['group'].append(group)
        new_policy['by'].append(ug_policy)

        # Build the for element from resource_types
        new_policy['for'] = {}
        for resource in policy['resource_types']:
            new_policy['for'][resource['type']] = []
            for rule in resource['rules']:
                new_rule = {}
                if rule.has_key("filter"):
                    new_rule[rule['filter']['filter_type']] = {}
                    new_rule[rule['filter']['filter_type']][rule['filter']['filter_property']] = rule['filter']['filter_value']
                    new_rule[rule['filter']['filter_type']][rule['name']] = rule['rule']
                else:
                    new_rule[rule['name']] = rule['rule']
                new_policy['for'][resource['type']].append(new_rule)

        # Add the policy to the list of new policies
        new_acl_policies.append(new_policy)
    return new_acl_policies

# with open("acl1.yml", 'r') as stream:
with open("hiera/rundeck.yaml", 'r') as stream:
    try:
        data = yaml.load(stream)
        # load the acl policies from the stream and convert the policy
        new_acl_policies = convert_policies(data['rundeck::acl_policies'])
        new_api_policies = convert_policies(data['rundeck::api_policies'])
        hiera = { "rundeck::acl_policies": new_acl_policies, "rundeck::api_policies": new_api_policies}

        # Write the result to file
        with open('result.yaml', 'w') as f:
        #   yaml.dump(new_acl_policies, f, default_flow_style=False)
          yaml.dump(hiera, f, default_flow_style=False)
    except yaml.YAMLError as exc:
        print(exc)
