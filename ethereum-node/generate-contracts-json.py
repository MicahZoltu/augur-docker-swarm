import codecs
import json
import os
import sys

def upper_first_character(string):
    return string[0].upper() + string[1:]

def get_contract_to_address_map():
    this_file_directory = os.path.dirname(os.path.realpath(sys.argv[0]))
    contract_to_adress_map_json_file_path = os.path.join(this_file_directory, 'build.json')
    with open(contract_to_adress_map_json_file_path) as contract_details_file:
        contract_details = json.load(contract_details_file)
    contract_to_address_map = {}
    source_directory = os.path.join(this_file_directory, os.pardir, "src")
    for _, _, file_names in os.walk(source_directory):
        if not file_names: continue
        for file_name in file_names:
            if not file_name.endswith(".se"): continue
            file_name_without_extension = file_name[:-3]
            if not file_name_without_extension in contract_details: continue
            address = contract_details[file_name_without_extension]["address"]
            contract_name = upper_first_character(file_name_without_extension).replace("&", "And")
            contract_to_address_map[contract_name] = address
    return contract_to_address_map

def write_contract_to_address_map_to_file_as_json():
    contract_to_address_map = get_contract_to_address_map()
    with open('/contracts.json', 'w') as contract_to_address_map_file:
        utf8_writer = codecs.getwriter('utf-8')
        json.dump({ '17': contract_to_address_map }, utf8_writer(contract_to_address_map_file), ensure_ascii=False, indent=2, sort_keys=True)

write_contract_to_address_map_to_file_as_json()
