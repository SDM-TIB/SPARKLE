"""## Installing the dependencies required for SPaRKLE"""

"""##pip install -r requirements.txt"""

"""## Importing the libraries"""

import time
import pandas as pd
from rdflib.plugins.sparql.processor import SPARQLResult
from pandasql import sqldf
from rdflib import Graph
import re
import os
import csv
import time

"""## Loading RDF Graph"""

def load_graph(file):
    g1 = Graph()
    with open(file, "r", encoding="utf-8") as rdf_file:
        lines = rdf_file.readlines()
        for line_number, line in enumerate(lines, start=1):
            try:
                g1.parse(data=line, format="nt")
                # Successfully parsed this line
            except Exception as e:
                print(f"Error parsing line {line_number}: {e}")
    return g1

def sparql_results_to_df(results: SPARQLResult) -> pd.DataFrame:
    return pd.DataFrame(
        data=([None if x is None else x.toPython() for x in row] for row in results),
        columns=[str(x) for x in results.vars],
    )

"""### Generating Symbolic Learning Predictions using AMIE"""

def rdflib_query(rule_df, prefix_query, rdf_data,head_val, predictions_folder, predictions_score_folder):
    global query, body_str1, body_str2, qres_df, new_result_df, new_res_df
    result_df = pd.DataFrame()
    new_result_df = pd.DataFrame()

    for idx, item in rule_df.iterrows():
        sub_dataframe = pd.DataFrame([item])
        for i, val in sub_dataframe.iterrows():
            fun_var = val['Functional_variable']
            body = val['Body']
            head = val['Head']
            conf = val['Std_Confidence']

            # Split the input string into individual words
            words = body.split()
            head_split = head.split()
            # Define the prefix
            prefix = 'fr:'
            # Define the regular expression pattern to match words without special characters like "?"
            pattern = re.compile(r'^\w+$')
            # Iterate through the list and modify the elements accordingly
            modified_list = [prefix + item if pattern.match(item) else item for item in words]
            modified_head = [prefix + item if pattern.match(item) else item for item in head_split]
            new_head = ' '.join(modified_head)
            # print(new_head)
            # Split the list into two parts after every three elements
            split_index = 3
            part1 = modified_list[:split_index]
            part2 = modified_list[split_index:]

            # Join the parts into strings
            string1 = ' '.join(part1)
            string2 = ' '.join(part2)

            # Print the strings if they are non-empty
            if string1:
                body_str1 = string1 + "."
            else:
                body_str1 = ""
            if string2:
                body_str2 = string2 + "."
            else:
                body_str2 = ""


            if fun_var == '?a':
                query = f"""
                            PREFIX fr: <{prefix_query}>
                            SELECT DISTINCT ?a ?b WHERE{{
                            {body_str1}
                            {body_str2}
                            {new_head}1 .
                            FILTER(?b1 != ?b).
                            FILTER(!EXISTS {{{new_head}}})
                            }}"""
                print(query)
                file_triple = load_graph(file=rdf_data)
                qres = file_triple.query(query)
                qres_df = pd.DataFrame(qres, columns=qres.vars)
                # print(qres_df)
                new_res_df = pd.DataFrame(qres, columns=qres.vars)
                new_res_df['Score'] = conf
                print(new_res_df)

            else:
                h = new_head.replace("?a", "?a1")
                query = f"""
                               PREFIX fr: <{prefix_query}>
                               SELECT DISTINCT ?a ?b WHERE{{
                               {body_str1}
                               {body_str2}
                               {h} .
                               FILTER(?a1 != ?a).
                               FILTER(!EXISTS {{{new_head}}})
                               }}"""
                print(query)
                file_triple = load_graph(file=rdf_data)
                qres = file_triple.query(query)
                qres_df = pd.DataFrame(qres, columns=qres.vars)
                # print(qres_df)
                new_res_df = pd.DataFrame(qres, columns=qres.vars)
                new_res_df['Score'] = conf
                print(new_res_df)

        result_df = pd.concat([result_df,qres_df], ignore_index=True)

        new_result_df = pd.concat([new_result_df, new_res_df], ignore_index=True)
    # Reset the index to maintain continuous order
    result_df.reset_index(drop=True, inplace=True)

    new_result_df.reset_index(drop=True, inplace=True)

    # print(result_df)
    result_df = result_df.replace(prefix_query, '', regex=True)
    result_df.insert(loc=1, column='predicate', value=head_val)
    result_df.to_csv(predictions_folder+head_val+'.tsv', sep='\t', index=False, header=None)

    new_result_df = new_result_df.replace(prefix_query, '', regex=True)
    new_result_df.insert(loc=1, column='predicate', value=head_val)
    new_result_df.to_csv(predictions_score_folder+head_val+'.tsv', sep='\t', index=False)

    # return result_df

def readRules(file, prefix, rdf_data, predictions_folder, predictions_score_folder):
    rules = pd.read_csv(file)
    q1 = f"""SELECT DISTINCT Head, COUNT(*) AS num FROM rules GROUP BY Head ORDER BY num DESC"""
    head_df = sqldf(q1, locals())
    for i, val in head_df.iterrows():
        head = val['Head']
        head_val = head.split()[1]
        q2 = f"""SELECT * FROM rules WHERE Head LIKE '%{head}%' ORDER BY Std_Confidence DESC"""
        rule = sqldf(q2, locals())
        result = rdflib_query(rule, prefix, rdf_data, head_val, predictions_folder, predictions_score_folder)

"""## Intersection"""

def read_tsv_intersection(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        values = set(line.strip() for line in lines)
    return values

def calculate_and_save_intersection(input_folder1, input_folder2, output_folder1, output_folder2):
    # Create the output folders if they don't exist
    if not os.path.exists(output_folder1):
        os.makedirs(output_folder1)
    if not os.path.exists(output_folder2):
        os.makedirs(output_folder2)

    file_list = os.listdir(input_folder1)

    for file_name in file_list:
        file1_path = os.path.join(input_folder1, file_name)
        file2_path = os.path.join(input_folder2, file_name)

        if os.path.isfile(file2_path):  # Check if corresponding file exists in input_folder2
            file1_values = read_tsv_intersection(file1_path)
            file2_values = read_tsv_intersection(file2_path)

            intersection1 = [value for value in file1_values if value in file2_values]
            intersection2 = [value for value in file2_values if value in file1_values]

            output_path1 = os.path.join(output_folder1, file_name)
            with open(output_path1, 'w', encoding='utf-8') as output_file1:
                for value in intersection1:
                    output_file1.write(value + '\n')

            output_path2 = os.path.join(output_folder2, file_name)
            with open(output_path2, 'w', encoding='utf-8') as output_file2:
                for value in intersection2:
                    output_file2.write(value + '\n')

"""### Evaluation"""

def read_tsv_evaluate(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        for row in reader:
            data.append(row)
    return data

def calculate_mrr(ranks):
    if not ranks:
        return 0.0
    return sum(1.0 / r for r in ranks) / len(ranks)

def calculate_hits_at_k(ranks, k):
    if not ranks:
        return 0.0
    return sum(1 for r in ranks if r <= k) / len(ranks)

def evaluate(predictions_folder, ground_truth_folder):
    mrr_values = []
    hits_at_10_values = []

    prediction_files = [f for f in os.listdir(predictions_folder) if f.endswith(".tsv")]
    ground_truth_files = [f for f in os.listdir(ground_truth_folder) if f.endswith(".tsv")]


    for pred_file, gt_file in zip(prediction_files, ground_truth_files):
        pred_path = os.path.join(predictions_folder, pred_file)
        gt_path = os.path.join(ground_truth_folder, gt_file)

        pred_data = read_tsv_evaluate(pred_path)
        # print(len(pred_data))
        gt_data = read_tsv_evaluate(gt_path)
        # print(len(gt_data))
        ranks = []
        for gt_row in gt_data:
            gt_entity = gt_row[2]
            pred_row = [row[2] for row in pred_data]
            if gt_entity in pred_row:
                rank = pred_row.index(gt_entity) + 1
                # print(rank)
                ranks.append(rank)

        if ranks:
            mrr_values.append(calculate_mrr(ranks))
            hits_at_10_values.append(calculate_hits_at_k(ranks, k=10))

    return mrr_values, hits_at_10_values

def getemptyfiles(rootdir):
    for root, dirs, files in os.walk(rootdir):
        for d in ['RECYCLER', 'RECYCLED']:
            if d in dirs:
                dirs.remove(d)

        for f in files:
            fullname = os.path.join(root, f)
            try:
                if os.path.getsize(fullname) == 0:
                    # print(fullname)
                    os.remove(fullname)
            except WindowsError:
                continue

if __name__ == '__main__':
    start_time = time.time()
    # AMIE rules
    rulesfile = "/SPaRKLE/YAGO3-enriched/AMIE_rules/YAGO3-enriched-training.csv"
    prefix = "http://YAGO3.org/"
    # RDF data to generate predictions
    rdf_data = "/SPaRKLE/YAGO3-enriched/YAGO3-enriched-training.nt"
    predictions_folder = "/SPaRKLE/YAGO3-enriched/AMIE_predictions/YAGO3-enriched-predictions/"
    predictions_score_folder = "/SPaRKLE/AMIE_SPaRKLE/YAGO3-enriched/AMIE_predictions/YAGO3-enriched-predictions-score/"
    rule_df = readRules(rulesfile, prefix, rdf_data, predictions_folder, predictions_score_folder)
    #Intersection
    ground_truth_folder = '/SPaRKLE/AMIE_SPaRKLE/YAGO3-enriched/ground_truth/'
    output_folder_ground_truth = ground_truth_folder+'ground_truth_intersection'
    output_folder_predictions = predictions_folder+'predictions_intersection'
    calculate_and_save_intersection(ground_truth_folder, predictions_folder, output_folder_ground_truth,output_folder_predictions)
    getemptyfiles(output_folder_ground_truth)
    getemptyfiles(output_folder_predictions)
    #Evaluation
    predictions_folder = output_folder_predictions
    ground_truth_folder = output_folder_ground_truth
    mrr_values, hits_at_10_values = evaluate(predictions_folder, ground_truth_folder)

    if mrr_values:
        print("Mean Reciprocal Rank (MRR):", sum(mrr_values) / len(mrr_values))
    else:
        print("Mean Reciprocal Rank (MRR): N/A (No matching entities in the ground truth)")

    if hits_at_10_values:
        print("Hits@10:", sum(hits_at_10_values) / len(hits_at_10_values))
    else:
        print("Hits@10: N/A (No matching entities in the ground truth)")

    end_time = time.time()
    execution_time = end_time - start_time

    print('Elaspsed time', execution_time)

