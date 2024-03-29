#!/usr/bin/python

import fileinput
import sys
import re

rules = {}

for line in fileinput.input():
    line = line.strip()
    if not line:
        break

    m = re.match(r".*ingress\.([0-9]+)\.([a-z_]+)([^:]*)\:\s+\"(.*)\" => \"(.*)\".*", line)
    # group 0 valid match
    # group 1 group id
    # group 2 group access type
    # group 3 group rule number
    # group 4 current value
    # group 5 new value
    if m and m.group(0):
        group_id = m.group(1)
        if group_id not in rules:
            rules[group_id] = {}

        if m.group(2) in ['security_groups', 'cidr_blocks','prefix_list_ids']:
            if m.group(2) not in rules[group_id]:
                rules[group_id][m.group(2)] = []
            if m.group(3) != '.#':
                rules[group_id][m.group(2)].append([m.group(4), m.group(5)])
        else:
            rules[group_id][m.group(2)] = [m.group(4), m.group(5)]
old = {}
new = {}

OLD = 'OLD'
NEW = 'NEW'

def add_rule(port, proto, id_, map_):
    key_ = "{}_{}_{}".format(port, proto, id_)
    if key_ in map_:
        print 'ERROR: Duplicate rule: ' + key_
    else:
        map_[key_] = [port, proto, id_]

for group_id in rules:
    port = rules[group_id]['from_port'][0] if (rules[group_id]['from_port'][0] != '0' and rules[group_id]['from_port'][0] != '') else rules[group_id]['from_port'][1]
    proto = rules[group_id]['protocol'][0] if rules[group_id]['protocol'][0] != '' else rules[group_id]['protocol'][1]
    proto = proto.lower()
    if 'security_groups' in rules[group_id]:
        for sg in rules[group_id]['security_groups']:
            _map_ref = None
            _id = None
            if sg[0]:
                add_rule(port, proto, sg[0], old)
            if sg[1]:
                add_rule(port, proto, sg[1], new)
    if 'cidr_blocks' in rules[group_id]:
        for ip in rules[group_id]['cidr_blocks']:
            if ip[0]:
                add_rule(port, proto, ip[0], old)

            if ip[1]:
                add_rule(port, proto, ip[1], new)
    if 'prefix_list_ids' in rules[group_id]:
        for pl in rules[group_id]['prefix_list_ids']:
            if pl[0]:
                add_rule(port, proto, pl[0], old)
            if pl[1]:
                add_rule(port, proto, pl[1], new)


for old_rule in old:
    if old_rule not in new:
        print 'Removed rule: %s' % old_rule

for new_rule in new:
    if new_rule not in old:
        print 'New rule: %s' % new_rule


