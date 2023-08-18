[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
# SPaRKLE:  Symbolic caPtuRing of knowledge for Knowledge graph enrichment with LEarning

SPaRKLE is a hybrid method that combines symbolic and mathematical methodologies 
while leveraging Partial Completness Assumption (PCA) heuristics to capture implicit information and enrich Knowledge Graphs (KGs).
The combination of symbolic and numerical strategies offers a comprehensive approach to KG enrichment that capitalizes on the strengths of both paradigms. 
This technique has the potential to provide more extensive, accurate, interpretable, and flexible knowledge representations, thereby improving the usefulness and efficacy of KGs across several domains.



![SPaRKLE Design Pattern](https://raw.githubusercontent.com/SDM-TIB/SPARKLE/main/images/SPARKLE.png "SPaRKLE Design Pattern")




### Building SPaRKLE from Source
Clone the repository
```git
git clone git@github.com:SDM-TIB/SPARKLE.git
```

## Running SPaRKLE
Installing the dependencies for ```SPaRKLE``` create a virtual environment and 
install the dependencies in the virtual environment created for SPaRKLE. To install the 
required dependencies run the following command:
```python
pip install -r requirements.txt
```

### Running Symbolic Learning (AMIE) for baseline and SPaRKLE approach inside ``AMIE_SPaRKLE`` folder
Executing scripts to reproduce AMIE results by choosing ``Baseline`` or ``SPaRKLE`` folders and navigating to appropriate path.

Provide configuration for executing
```json
{
  "Type": "Baseline",
  "KG": "FrenchRoyalty",
  "prefix": "http://FrenchRoyalty.org/",
  "rules_file": "french_training.csv",
  "rdf_file": "french_training.nt"
}
```
The user must supply a few options in the above JSON file to select the type of approach that has to be executed with added configuration details. <br>
The parameter ``Type`` corresponds to the type of execution, i.e., ```Baseline``` or ```SPaRKLE```.<br>
Secondly, parameter ``KG`` is the type of knowledge graph, i.e., ```FrenchRoyalty``` or ```Family``` or ```YAGO3```.<br>
Nextly,```prefix```parameter is used for preprocessing the predictions results for readability.<br>
Lastly, ```rules_file``` and ```rdf_file``` are the file names for premined rules and KG in the form of `NT`file.

```python
python sparkle_amie.py 
```

### Plots demonstrating SPaRKLE Effectiveness using Linear Regression analysis
![French Royalty](https://raw.githubusercontent.com/SDM-TIB/SPARKLE/main/images/FR_linear_regression.png "FrenchRoyalty_Linear_Regression_Analysis")
![Family KG](https://raw.githubusercontent.com/SDM-TIB/SPARKLE/main/images/Family_linear_regression.png "Family_Linear_Regression_Analysis")
![YAGO3-10](https://raw.githubusercontent.com/SDM-TIB/SPARKLE/main/images/YAGO3-10_linear_regression.png "YAGO3-10_Linear_Regression_Analysis")



## Running Numerical Learning for baseline and SPaRKLE approach inside ``KGE`` folder



