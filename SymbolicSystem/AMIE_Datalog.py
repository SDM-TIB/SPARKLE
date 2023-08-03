#!/usr/bin/env python
# coding: utf-8
import sys
import pandas as pd

from pyDatalog import pyDatalog
from pyDatalog.pyDatalog import assert_fact, load, ask


def load_AMIE_rule(file_name):
    result = pd.read_csv(file_name)  # , delimiter='\t'
    result.replace('type', 'Type', regex=True, inplace=True)
    result.Body = result.Body.str.rstrip()
    # result.replace('>', '', regex=True, inplace=True)
    # result.replace('<', '', regex=True, inplace=True)
    return result


# ## Intensional Data Base
def create_IDB(result):
    amie_rule = result[['Body', 'Head']]
    rule_list = """"""
    head_dict = dict()
    for d in amie_rule.values:
        #     === Creating Head of the Rule ===
        head = d[1].split('  ')
        sub, pred, obj = head[0], head[1], head[2]
        sub = sub.replace('?', '')
        sub = sub.capitalize()
        head_literal = pred + '(' + sub + ', '

        if obj.startswith('?'):
            obj = obj.replace('?', '')
            obj = obj.capitalize()
            head_literal += obj + ')'
        else:
            head_literal += """'""" + obj + """')"""
        rule = head_literal + """ <= """
        head_dict[head_literal] = [pred, """'""" + obj + """'"""]

        #     === Creating Body of Rule ===
        body = d[0].split('  ')
        rule_b = """"""
        for i in range(2, len(body), 3):
            sub, pred_body, obj = body[i - 2], body[i - 1], body[i]
            # print(pred, '===', pred_body)
            if pred_body == pred:
                if sub.startswith('?'):
                    sub = sub.replace('?', '')
                    sub = sub.capitalize()
                    b = pred_body + '(' + sub + ', '
                else:
                    b = pred_body + """('""" + sub + """', """
                if obj.startswith('?'):
                    obj = obj.replace('?', '')
                    obj = obj.capitalize()
                    b += obj + ') & '
                else:
                    b += """'""" + obj + """') & """
                b += rule_b
                # print(rule_b, '--', b)
                rule_b = b
            else:
                if sub.startswith('?'):
                    sub = sub.replace('?', '')
                    sub = sub.capitalize()
                    rule_b += pred_body + '(' + sub + ', '
                else:
                    rule_b += pred_body + """('""" + sub + """', """
                if obj.startswith('?'):
                    obj = obj.replace('?', '')
                    obj = obj.capitalize()
                    rule_b += obj + ') & '
                else:
                    rule_b += """'""" + obj + """') & """
        
        rule_b = rule_b[:-3]
        rule += rule_b
        # print(rule)
        rule_list += '\n' + rule
    return rule_list, head_dict


def load_graph(file_name):
    data = pd.read_csv(file_name, delimiter='\t', header=None)  #
    data.columns = ['s', 'p', 'o']
    data.replace('type', 'Type', regex=True, inplace=True)
    # data.replace('>', '', regex=True, inplace=True)
    # data.replace('<', '', regex=True, inplace=True)
    # data.replace(' .', '', regex=True, inplace=True)
    return data


# #### List of Terms considered in Datalog program
# term_graph = pd.read_csv('AMIERules/Family/terms_Family.csv')
term_graph = pd.read_csv('AMIERules/FrenchRoyalty/terms_FrenchRoyalty.csv')
pyDatalog.create_terms(','.join(term_graph.term.tolist()))


# def create_terms(data, terms):
#     terms.update(set(data.p.unique()))
#     pyDatalog.create_terms(','.join(terms))


def build_datalog_model(data, rule_list):
    print(rule_list)
    pyDatalog.clear()
    for d in data.values:
        # === Extensional Database ===
        assert_fact(d[1], d[0], d[2])

    load(rule_list)
    # Type(A, B) <= Type(E, B) & child(E, A)
#     load("""parent(A, B) <= father(A, B)
# parent(A, B) <= mother(A, B)
# successor(A, B) <= predecessor(B, A) & spouse(A, B)
# successor(A, B) <= mother(B, A) & predecessor(B, A)
# predecessor(A, B) <= predecessor(B, A) & successor(B, A)
# parent(A, B) <= father(A, B) & successor(B, A)
# name(A, B) <= name(F, B) & name(A, F)
# Type(A, B) <= Type(E, B) & mother(E, A)
# spouse(A, B) <= spouse(B, A) & successor(B, A)
# spouse(A, B) <= spouse(B, A) & successor(A, B)
# Type(A, B) <= Type(E, B) & successor(E, A)
# """)  # rule_list


def reasoning_datalog(data, head_dict, rule_list):
    build_datalog_model(data, rule_list)
    list_deduced_link = pd.DataFrame(columns=['s', 'p', 'o'])
    #     === Query Datalog model ===
    for rule_h, val in head_dict.items():
        deduced_link = pyDatalog.ask(rule_h).answers
        #         === Creating DataFrame with deduced links ===
        for i in range(len(deduced_link)):
            if len(deduced_link[i]) == 2:
                x = {'s': [deduced_link[i][0]], 'p': val[0], 'o': deduced_link[i][1]}
            else:
                x = {'s': [deduced_link[i][0]], 'p': val[0], 'o': val[1]}
            list_deduced_link = pd.concat([list_deduced_link, pd.DataFrame(data=x)])
    #     === enriching original graph with the new links deduced ===
    list_deduced_link = list_deduced_link.merge(data, how='outer', indicator=True).loc[
        lambda x: x['_merge'] == 'left_only']  # , on='DrugName'
    list_deduced_link = list_deduced_link.drop(columns=['_merge'])
    graph_deduced = pd.concat([data, list_deduced_link])
    graph_deduced.drop_duplicates(keep='first', inplace=True)
    list_deduced_link.replace('Type', 'type', regex=True, inplace=True)
    graph_deduced.replace('Type', 'type', regex=True, inplace=True)
    return graph_deduced, list_deduced_link


# file_name = 'AMIERules/FrenchRoyalty_AMIE_Rules.csv'
# path = '../KG/FrenchRoyalty/french_training.tsv'
def main(*args):
    """Load AMIE Rules"""
    result = load_AMIE_rule(args[0])
    """Create Intensional Data Base """
    rule_list, head_dict = create_IDB(result)
    """Load Knowledge Graph"""
    data = load_graph(args[1])
    """List of Terms considered in Datalog program"""
    # create_terms(data, terms)
    """Reasoning Datalog program"""
    graph_deduced, list_deduced_link = reasoning_datalog(data, head_dict, rule_list)
    list_deduced_link.to_csv(args[2], index=None, header=None, sep='\t')
    graph_deduced.to_csv(args[3], index=None, header=None, sep='\t')


if __name__ == '__main__':
    main(*sys.argv[1:])
