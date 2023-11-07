# Steps to execute SPaRKLE for AMIE 

AMIE_SPaRKLE contains twpo subfolders `Baseline` and `SPaRKLE` folders. 
`Baseline` represents the state-of-the-art execution of AMIE and generating predictions. 

### Configuration file (input.json) to execute AMIE SPaRKLE
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
- ``Type`` corresponds to the type of execution, i.e., ```Baseline``` or ```SPaRKLE```. <br>
- ``KG`` is the type of knowledge graph, i.e., ```FrenchRoyalty``` or ```Family``` or ```YAGO3-10```. <br>
- ```prefix```parameter is used for preprocessing the predictions results for readability. <br>
- ```rules_file``` and ```rdf_file``` are the file names for pre-mined rules and KG in the form of `NT` (N triples) file.<br>

### Step 1: Setting Configuration 
To run ``AMIE_SPaRKLE``, the user must change the configuration file. 
Users can modify the configuration file based on the dataset and settings they want to utilize. The parameters in the configuration file are described in detail above.

### Step 2: Executing sparkle_amie.py
SPaRKLE will execute the script `sparkle_amie.py` to reproduce results based on the type parameter selected in the input configuration file. 
Execute the script ``python sparkle_amie.py``.
