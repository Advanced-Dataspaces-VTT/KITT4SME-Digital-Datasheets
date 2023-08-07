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
    print("----------")
    print(datasheet)
    print("----------")
    datasheet_root_path = datasheet["context"]["benefits"]

    for item in datasheet_root_path.copy():
        if item in schema_root_path:
            for sub_item in datasheet_root_path[item].copy():
                schema_title = schema_root_path[item]["properties"][sub_item]["title"]
                datasheet_root_path[item][schema_title] = datasheet_root_path[item].pop(sub_item)
 
    return datasheet

def convert_features(datasheet):
    schema_root_path = schema["features"]["properties"]
    datasheet_root_path = datasheet["context"]["features"]

    for item in datasheet_root_path:
        if item in schema_root_path:
            for index, sub_item in enumerate(datasheet_root_path[item]):
                schema_title = schema_root_path[item]["items"]["oneOf"][int(sub_item) - 1]["title"]
                datasheet_root_path[item][index] = schema_title

    return datasheet

def convert_datamodel(datasheet):
    schema_root_path = schema["datamodel"]["properties"]
    datasheet_root_path = datasheet["datamodel"]

    reference_model = []
    for entity_type in ["input", "output"]:
        if entity_type in schema_root_path:
            for sub_item in datasheet_root_path[entity_type].copy():
                print("---")
                print(schema_root_path[entity_type]["properties"][sub_item])
                if "items" in schema_root_path[entity_type]["properties"][sub_item]:
                    reference_model.append(schema_root_path[entity_type]["properties"][sub_item]["items"]["$ref"])
                else:
                    # If 'items' key is not present, skip this iteration.
                    continue
                print("---")
                
    
    schema_model = []
    datasheet_model = []
    for model in reference_model:
        model = model.split("#/")[1]
        schema_model.append(model)
        datasheet_model.append(model.split("_")[1])

    for model_type in ["datamodel_links", "input", "output"]:
        datasheet_root_path_reference_model = datasheet["datamodel"][model_type]
        for d_model in datasheet_root_path_reference_model:
            updated_list = []
            for index, d_model_value in enumerate(datasheet_root_path_reference_model[d_model]):
                try:
                    index = int(d_model_value) - 1
                except ValueError:
                    print(f"Error: Invalid value '{d_model_value}' for {d_model}. Skipping this value.")
                    continue

                for s_model in schema_model:
                    if s_model not in schema:
                        print(f"Error: {s_model} not found in schema.")
                        continue

                    one_of_list = schema[s_model]["oneOf"]
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
    datasheet_root_path = datasheet["skills"]

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

def convert_industry(datasheet):
    schema_industry = schema["industry"]["oneOf"]

    datasheet_industry_codes = datasheet["context"]["industry"]
    datasheet_industry_titles = []

    for code in datasheet_industry_codes:
        code_int = int(code) - 1
        if 0 <= code_int < len(schema_industry):
            title = schema_industry[code_int]["title"]
            datasheet_industry_titles.append(title)
        else:
            print(f"Error: Invalid industry code '{code}'. Skipping this value.")

    datasheet["context"]["industry"] = datasheet_industry_titles
    return datasheet

def convert_quality(datasheet):
    schema_quality = schema["module_property"]["properties"]["quality"]["items"]["properties"]["issue"]["oneOf"]
    schema_relevance = schema["relevance"]["oneOf"]

    datasheet_quality = datasheet["module_properties"]["quality"]

    for item in datasheet_quality:
        issue_title = item["issue"]
        relevance_title = item["relevance"]

        issue_code = None
        for schema_item in schema_quality:
            if schema_item["title"] == issue_title:
                issue_code = schema_item["const"]
                break

        if issue_code is not None:
            item["issue"] = issue_title
        else:
            print(f"Error: Invalid quality issue title '{issue_title}'. Skipping this value.")

        relevance_code = None
        for schema_item in schema_relevance:
            if schema_item["title"] == relevance_title:
                relevance_code = schema_item["const"]
                break

        if relevance_code is not None:
            item["relevance"] = relevance_title
        else:
            print(f"Error: Invalid relevance title '{relevance_title}'. Skipping this value.")

    return datasheet

def convert_performance(datasheet):
    schema_performance = schema["module_property"]["properties"]["performance"]["items"]["properties"]["issue"]["oneOf"]
    schema_relevance = schema["relevance"]["oneOf"]

    datasheet_performance = datasheet["module_properties"]["performance"]

    for item in datasheet_performance:
        issue_title = item["issue"]
        relevance_title = item["relevance"]

        issue_code = None
        for schema_item in schema_performance:
            if schema_item["title"] == issue_title:
                issue_code = schema_item["const"]
                break

        if issue_code is not None:
            item["issue"] = issue_title
        else:
            print(f"Error: Invalid performance issue title '{issue_title}'. Skipping this value.")

        relevance_code = None
        for schema_item in schema_relevance:
            if schema_item["title"] == relevance_title:
                relevance_code = schema_item["const"]
                break

        if relevance_code is not None:
            item["relevance"] = relevance_title
        else:
            print(f"Error: Invalid relevance title '{relevance_title}'. Skipping this value.")

    return datasheet

def convert_management(datasheet):
    schema_management = schema["module_property"]["properties"]["management"]["items"]["properties"]["issue"]["oneOf"]
    schema_relevance = schema["relevance"]["oneOf"]

    datasheet_management = datasheet["module_properties"]["management"]

    for item in datasheet_management:
        issue_title = item["issue"]
        relevance_title = item["relevance"]

        issue_code = None
        for schema_item in schema_management:
            if schema_item["title"] == issue_title:
                issue_code = schema_item["const"]
                break

        if issue_code is not None:
            item["issue"] = issue_title
        else:
            print(f"Error: Invalid management issue title '{issue_title}'. Skipping this value.")

        relevance_code = None
        for schema_item in schema_relevance:
            if schema_item["title"] == relevance_title:
                relevance_code = schema_item["const"]
                break

        if relevance_code is not None:
            item["relevance"] = relevance_title
        else:
            print(f"Error: Invalid relevance title '{relevance_title}'. Skipping this value.")

    return datasheet

def convert_os(datasheet):
    schema_os = schema["os"]["items"]["oneOf"]

    datasheet_os = datasheet["technicalrequirements"]["os"]

    for index, os_code in enumerate(datasheet_os.copy()):
        os_code_int = int(os_code) - 1
        if 0 <= os_code_int < len(schema_os):
            os_title = schema_os[os_code_int]["title"]
            datasheet_os[index] = os_title
        else:
            print(f"Error: Invalid OS code '{os_code}'. Skipping this value.")

    return datasheet

def convert_operator(datasheet):
    schema_operator = schema["module_property"]["properties"]["operator"]["items"]["properties"]["issue"]["oneOf"]
    schema_relevance = schema["relevance"]["oneOf"]

    datasheet_operator = datasheet["module_properties"].get("operator", [])

    for item in datasheet_operator:
        issue_title = item["issue"]
        relevance_title = item["relevance"]

        issue_code = None
        for schema_item in schema_operator:
            if schema_item["title"] == issue_title:
                issue_code = schema_item["const"]
                break

        if issue_code is not None:
            item["issue"] = issue_title
        else:
            print(f"Error: Invalid operator issue title '{issue_title}'. Skipping this value.")

        relevance_code = None
        for schema_item in schema_relevance:
            if schema_item["title"] == relevance_title:
                relevance_code = schema_item["const"]
                break

        if relevance_code is not None:
            item["relevance"] = relevance_title
        else:
            print(f"Error: Invalid relevance title '{relevance_title}'. Skipping this value.")

    return datasheet

def manage_conversion(datasheet):
    random_number = random.random()
    scaled_random_number = random_number * 100
    rounded_random_number = math.ceil(scaled_random_number)

    datasheet = datasheet[0]
    datasheet = convert_benefits(datasheet)
    datasheet = convert_features(datasheet)
    datasheet = convert_datamodel(datasheet)
    datasheet = convert_skills(datasheet)


    if "industry" in datasheet["module_properties"]:
        datasheet = convert_industry(datasheet)
    if "quality" in datasheet["module_properties"]:
        datasheet = convert_quality(datasheet)
    if "operator" in datasheet["module_properties"]:
        datasheet = convert_operator(datasheet)
    if "performance" in datasheet["module_properties"]:
        datasheet = convert_performance(datasheet)
    if "management" in datasheet["module_properties"]:
        datasheet = convert_management(datasheet)
    if "os" in datasheet["technicalrequirements"]:
        datasheet = convert_os(datasheet)

    datasheet_filename = "datasheet_" + str(rounded_random_number) + ".json"
    save_json(datasheet, datasheet_filename)

if __name__ == '__main__': 
    with open('datasheet-AIGreenWaste (35).json', 'r') as f:
        datasheet_json = f.read()
        datasheet = json.loads(datasheet_json)
    
    manage_conversion([datasheet])
