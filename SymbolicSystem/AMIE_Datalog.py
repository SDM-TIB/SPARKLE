#!/usr/bin/env python
# coding: utf-8
import sys
import pandas as pd

from pyDatalog import pyDatalog
from pyDatalog.pyDatalog import assert_fact, load, ask


def load_AMIE_rule(file_name):
    result = pd.read_csv(file_name)  # , delimiter='\t'
    result.Body = result.Body.str.rstrip()
    result.replace('>', '', regex=True, inplace=True)
    result.replace('<', '', regex=True, inplace=True)
    return result


# ## Intensional Data Base
def create_IDB(result):
    amie_rule = result[['Body', 'Head']]
    rule_list = """"""
    head_dict = dict()
    terms = set()
    for d in amie_rule.values:
        #     === Creating Head of the Rule ===
        head = d[1].split('  ')
        sub, pred, obj = head[0], head[1], head[2]
        terms.add(pred)
        sub = sub.replace('?', '')
        sub = sub.capitalize()
        terms.update(sub)
        head_literal = pred + '(' + sub + ', '

        if obj.startswith('?'):
            obj = obj.replace('?', '')
            obj = obj.capitalize()
            terms.update(obj)
            head_literal += obj + ')'
        else:
            head_literal += """'""" + obj + """')"""
        rule = head_literal + """ <= """
        head_dict[head_literal] = [pred, """'""" + obj + """'"""]

        #     === Creating Body of Rule ===
        body = d[0].split('  ')
        for i in range(2, len(body), 3):
            sub, pred, obj = body[i - 2], body[i - 1], body[i]
            terms.add(pred)
            if sub.startswith('?'):
                sub = sub.replace('?', '')
                sub = sub.capitalize()
                terms.update(sub)
                rule += pred + '(' + sub + ', '
            else:
                rule += pred + """('""" + sub + """', """
            if obj.startswith('?'):
                obj = obj.replace('?', '')
                obj = obj.capitalize()
                terms.update(obj)
                rule += obj + ') & '
            else:
                rule += """'""" + obj + """') & """
        rule = rule[:-3]
        rule_list += '\n' + rule
    return rule_list, head_dict, terms


def load_graph(file_name):
    data = pd.read_csv(file_name, delimiter='\t', header=None)  #
    data.columns = ['s', 'p', 'o']
    data.replace('>', '', regex=True, inplace=True)
    data.replace('<', '', regex=True, inplace=True)
    data.replace(' .', '', regex=True, inplace=True)
    return data


# #### List of Terms considered in Datalog program
term_graph = pd.read_csv('AMIERules/FrenchRoyalty/terms_FrenchRoyalty.csv')
pyDatalog.create_terms(','.join(term_graph.term.tolist()))
# def create_terms(data, terms):
#     terms.update(set(data.p.unique()))
#     pyDatalog.create_terms(','.join(terms))


def build_datalog_model(data, rule_list, terms):
    pyDatalog.clear()
    for d in data.values:
        # === Extensional Database ===
        assert_fact(d[1], d[0], d[2])

    load(rule_list)
#     load("""spouse(A, B) <= parent(E, A) & predecessor(E, B)
# hasSpouse(A, 'No') <= gender(A, '"male"@en')
# successor(A, B) <= spouse(E, A) & successor(E, B)""") # rule_list


def reasoning_datalog(data, head_dict, rule_list, terms):
    build_datalog_model(data, rule_list, terms)
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
    graph_deduced = pd.concat([data, list_deduced_link])
    graph_deduced.drop_duplicates(keep='first', inplace=True)
    return graph_deduced, list_deduced_link


# file_name = 'AMIERules/FrenchRoyalty_AMIE_Rules.csv'
# path = '../KG/FrenchRoyalty/french_training.tsv'
def main(*args):
    """Load AMIE Rules"""
    result = load_AMIE_rule(args[0])
    """Create Intensional Data Base """
    rule_list, head_dict, terms = create_IDB(result)
    """Load Knowledge Graph"""
    data = load_graph(args[1])
    """List of Terms considered in Datalog program"""
    # create_terms(data, terms)
    """Reasoning Datalog program"""
    graph_deduced, list_deduced_link = reasoning_datalog(data, head_dict, rule_list, terms)
    list_deduced_link.to_csv(args[2], index=None, header=None)
    graph_deduced.to_csv(args[3], index=None, header=None)


if __name__ == '__main__':
    main(*sys.argv[1:])
