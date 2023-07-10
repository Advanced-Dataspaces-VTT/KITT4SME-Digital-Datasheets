import json

def load_saved_datasheeet(saved_schema, filter_text):
    with open('content.json') as content_file:
        original_schema = json.load(content_file)
        relevance_oneOf = original_schema['relevance']['oneOf']

    # Properties to check for
    properties_to_check = ['quality', 'performance', 'management', 'operator']

    # Create a new list to store the updated data
    updated_data = []

    # Traverse the objects in dump.json
    for obj in saved_schema:
        module_properties = obj['datasheet']['module_properties']
        updated_properties = {}

        # Traverse the properties to check
        for prop in properties_to_check:
            if prop in module_properties:
                prop_value = module_properties[prop]
                if isinstance(prop_value, list):
                    updated_items = []
                    for item in prop_value:
                        if 'relevance' in item and isinstance(item['relevance'], str):
                            relevance_value = item['relevance']
                            for content_relevance_item in relevance_oneOf:
                                if content_relevance_item['const'] == relevance_value:
                                    item['relevance'] = content_relevance_item['title']
                                    break
                        if 'issue' in item and isinstance(item['issue'], str):
                            issue_value = item['issue']
                            module_property_properties = original_schema['module_property']['properties']
                            if prop in module_property_properties:
                                issue_oneOf = module_property_properties[prop]['items']['properties']['issue']['oneOf']
                                for issue_item in issue_oneOf:
                                    if issue_item['const'] == issue_value:
                                        item['issue'] = issue_item['title']
                                        break
                        updated_items.append(item)
                    updated_properties[prop] = updated_items

        # Update the module_properties in the current object
        obj['datasheet']['module_properties'] = updated_properties

        # Add the updated object to the new list
        updated_data.append(obj)

    # Save the modified data to new_dump.json
    #with open('new_dump.json', 'w') as output_file:
       #json.dump(updated_data, output_file)
    
    # Convert the updated_data to a JSON string
    updated_data_json = json.dumps(updated_data)

    # Parse the JSON data
    data = json.loads(updated_data_json)
    found_ids = []
    
    def recursive_search(obj, word):
        if isinstance(obj, dict):
            if "id" in obj:
                found_ids.append(obj["id"])
            
            for value in obj.values():
                recursive_search(value, word)
        
        elif isinstance(obj, list):
            for item in obj:
                recursive_search(item, word)
        
        elif isinstance(obj, str) and word in obj:
            found_ids.append(obj)
    
    for entry in data:
        datasheet = entry.get("datasheet", {})
        word = filter_text.split()
        for w in word: 
            recursive_search(datasheet, w)
   
    return set(found_ids)
