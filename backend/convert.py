import json
import random
import math

def load_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def save_json(data, path):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

schema = load_json("content.json")
#datasheet = load_json("datasheet.json")

def convert_benefits(datasheet):
    schema_root_path = schema["benefits"]["properties"]
    datasheet_root_path = datasheet["datasheet"]["context"]["benefits"]

    for item in datasheet_root_path.copy():
        if item in schema_root_path:
            for sub_item in datasheet_root_path[item].copy():
                schema_title = schema_root_path[item]["properties"][sub_item]["title"]
                datasheet_root_path[item][schema_title] = datasheet_root_path[item].pop(sub_item)
 
    return datasheet

def convert_features(datasheet):
    schema_root_path = schema["features"]["properties"]
    datasheet_root_path = datasheet["datasheet"]["context"]["features"]

    for item in datasheet_root_path:
        if item in schema_root_path:
            for index, sub_item in enumerate(datasheet_root_path[item]):
                schema_title = schema_root_path[item]["items"]["oneOf"][int(sub_item) - 1]["title"]
                datasheet_root_path[item][index] = schema_title

    return datasheet

def convert_datamodel(datasheet):
    schema_root_path = schema["datamodel"]["properties"]
    datasheet_root_path = datasheet["datasheet"]["datamodel"]

    reference_model = []
    for entity_type in ["input", "output"]:
        if entity_type in schema_root_path:
            for sub_item in datasheet_root_path[entity_type].copy():
                print("---")
                print(schema_root_path[entity_type]["properties"][sub_item])
                reference_model.append(schema_root_path[entity_type]["properties"][sub_item]["items"]["$ref"])
                print("---")
                
    
    schema_model = []
    datasheet_model = []
    for model in reference_model:
        model = model.split("#/")[1]
        schema_model.append(model)
        datasheet_model.append(model.split("_")[1])

    for model_type in ["datamodel_links", "input", "output"]:
        datasheet_root_path_reference_model = datasheet["datasheet"]["datamodel"][model_type]
        for d_model in datasheet_root_path_reference_model:
            updated_list = []
            for index, d_model_value in enumerate(datasheet_root_path_reference_model[d_model]):
                for s_model in schema_model:
                    if s_model not in schema:
                        print(f"Error: {s_model} not found in schema.")
                        continue
                    one_of_list = schema[s_model]["oneOf"]
                    index = int(d_model_value) - 1
                    if index < 0 or index >= len(one_of_list):
                        print(f"Error: Index out of range for {s_model}, index: {index}")
                        continue
                    schema_root_path_reference_model = one_of_list[index]["title"]
                    updated_list.append(schema_root_path_reference_model)
                    break  # Once found, no need to continue with other models
            datasheet_root_path[model_type][d_model] = updated_list

    return datasheet


def convert_skills(datasheet):
    schema_root_path = schema["skills"]["properties"]
    datasheet_root_path = datasheet["datasheet"]["skills"]

    for skill_type in datasheet_root_path.copy():
        if skill_type in schema_root_path:
            for sub_skill in datasheet_root_path[skill_type].copy():
                reference_model = schema_root_path[skill_type]["properties"][sub_skill]["items"]["oneOf"]
                for skill_value in datasheet_root_path[skill_type][sub_skill]:
                    skill_value_int = int(skill_value) - 1
                    if 0 <= skill_value_int < len(reference_model):
                        title = reference_model[skill_value_int]["title"]
                        datasheet_root_path[skill_type][sub_skill] = title
                    else:
                        print(f"Error: Index out of range for {sub_skill}, index: {skill_value_int}")

    return datasheet


#convert_benefits()
#convert_features()
#convert_datamodel()
#convert_skills()
#save_json(datasheet, "datasheet_new.json")


def manage_conversion(datasheet):
    random_number = random.random()
    scaled_random_number = random_number * 100
    rounded_random_number = math.ceil(scaled_random_number)

    datasheet = datasheet[0]
    datasheet = convert_benefits(datasheet)
    datasheet = convert_features(datasheet)
    datasheet = convert_datamodel(datasheet)
    datasheet = convert_skills(datasheet)
    datasheet_filename = "datasheet_" + str(rounded_random_number) + ".json"
    save_json(datasheet, datasheet_filename)
