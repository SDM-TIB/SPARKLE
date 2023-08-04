# 1.  About

Datalog reasoning with AMIE rules

## 2. Requirements

* pyDatalog
* pandas

## 3. Running example for extracting *Datalog Terms*
`French Royalty KG`
```python
python .\Datalog_Terms.py ../KG/FrenchRoyalty/french_training.tsv AMIERules/FrenchRoyalty/terms_FrenchRoyalty.csv 
```
`Family KG`
```python
python .\Datalog_Terms.py ../KG/Family/family_training_triples.tsv AMIERules/Family/terms_Family.csv
```
## 4. Running example for *Datalog program*: *AMIE_Datalog*
```python
python .\AMIE_Datalog.py ./AMIERules/Family/family_training_99.csv ../KG/Family/family_training_triples.tsv ./AMIERules/Family/Deduced/ 99
```
## 5. Running example for creating subset of AMIE rules given a percentile *CreateSubsetAMIE_Rule*
```python
python .\CreateSubsetAMIE_Rule.py 90 AMIERules/FrenchRoyalty/ FrenchRoyalty_AMIE_Rules
```
