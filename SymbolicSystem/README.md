# 1.  About

Datalog reasoning with AMIE rules

## 2. Requirements

* pyDatalog
* pandas

## 3. Running example for extracting *Datalog Terms*
>python .\Datalog_Terms.py ../KG/FrenchRoyalty/french_training.tsv AMIERules/FrenchRoyalty/terms_FrenchRoyalty.csv

## 4. Running example for *Datalog program: * *AMIE_Datalog*
>python .\AMIE_Datalog.py AMIERules/FrenchRoyalty/FrenchRoyalty_AMIE_Rules.csv ../KG/FrenchRoyalty/french_training.tsv deduced.csv eriched.csv
