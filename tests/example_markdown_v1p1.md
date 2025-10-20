## Survey
Optional survey name
## Dataset
Recommended dataset name
## Table
Required table name
## Version
Required version (string, integer, or float)
## Date
2025-09-01
## Author
Required lead author name <email>
## Coauthors
* Optional coauthor name <email1>
* ... <...>
## Dois
| Doi | Type |
| --- | --- |
| Valid DOI | DOI type |
## Depends
| Survey | Dataset | Table | Version |
| --- | --- | --- | --- |
| Dependent survey | Dependent dataset | Dependent table | Dependent table version |
## Description
Recommended short description of the table
## Comments
* Optional comment or interesting fact
* ...
## License
Recommended license for the dataset / table
## Keywords
* Optional keyword tag
* ...
## Keyarray
| Key | Value | Comment |
| --- | --- | --- |
| test_scalar | 8.1 | something |
| test_string | Fun times | something |
| test_vector | <ul><li>1.8</li><li>2.0</li><li>5.0</li></ul> | something |
## Extra
### Anything
#### I
##### Like
1.3



## Maml_Version
1.1
## Fields
| Name | Unit | Info | Ucd | Data_Type | Array_Size | Qc |
| --- | --- | --- | --- | --- | --- | --- |
| ID | None | None | <ul><li>meta.id</li><li>meta.main</li></ul> | int32 | None | {'min': 1.0, 'max': 5.0, 'miss': 'Null'} |
| Name | None | None | None | string | None | {'min': 'A', 'max': 'E', 'miss': 'Null'} |
| Date | None | None | <ul><li>time</li><li>obs.exposure</li></ul> | string | None | {'min': '2025-06-13', 'max': '2025-09-03', 'miss': 'Null'} |
| Flag | None | None | None | boolean | None | {'min': 0.0, 'max': 1.0, 'miss': 'Null'} |
| RA | deg | None | pos.eq.ra | float64 | None | {'min': 43.1, 'max': 48.9, 'miss': 'Null'} |
| Dec | deg | None | [Ucd](pos.eq.dec) | float64 | None | {'min': 1.2, 'max': 3.5, 'miss': 'Null'} |
| Mag | None | None | [Ucd](phot.mag) | float64 | None | {'min': 15.2, 'max': 22.1, 'miss': 'Null'} |
