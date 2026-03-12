# bdf-datastore

## How to Contribute
- Fork the repo 
- Make the changes following the below format
- Raise a Pull Request against main

**Folder Structure**
- {contributor}
    - {cell}
        - {eis}
          - {raw} [from test hardware]
          - **{processed}.bdf**
          - {metadata}.json [test metadata]
        - {timeseries}
          - {raw} [from test hardware]
          - **{processed}.bdf**
          - {metadata}.json [test metadata]
        - {metadata}.json [cell metadata]
   
      
## Conventions
- Contributor - full name of organization contributing dataset following DNS rules
- Cell = CellName = manufacturer-model-batch-id
    - Please note: bdf-datastore has additional constraints on CellName. CellName = manufacturer-model-batch-id
- Data Type {eis, timeseries}
- Data Processing {raw, processed}
- BDF File Naming Conventions `InstitutionCode__CellName__YYYYMMDD_XXX.csv`
    - SINTEF__google-g20m7__{generation_date}__001.bdf.csv
    - Microsoft__google-g20m7__{generation_date}_XXX.bdf.csv
- Metadata Data convention [Link to Example](https://github.com/battery-data-alliance/battery-data-format/blob/main/examples/metadata.ipynb)


      
      
