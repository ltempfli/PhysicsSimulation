import json
import csv

def is_statically_stable(result_file_path: str) -> bool:
    file_not_found = []
    try:
        with open(result_file_path) as file:
            result_dic = json.load(file)
            return all(entry['score'] == 1.0 for entry in result_dic['assesmentEvaluationSet'] if entry['criterion']['criterionType'] == 'PhysicalSimulationCriterion')
    except FileNotFoundError:
        file_not_found.append(result_file_path)
        with open("../file_not_found_log.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(file_not_found)
        return False