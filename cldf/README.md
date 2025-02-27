<a name="ds-wordlistmetadatajson"> </a>

# Wordlist Database of Cross-Linguistic Norms, Ratings, and Relations for Words and Concepts as CLDF dataset

**CLDF Metadata**: [Wordlist-metadata.json](./Wordlist-metadata.json)

**Sources**: [sources.bib](./sources.bib)

property | value
 --- | ---
[dc:bibliographicCitation](http://purl.org/dc/terms/bibliographicCitation) | Tjuka, Annika, Robert Forkel, and Johann-Mattis List. 2022. Linking Norms, Ratings, and Relations of Words and Concepts Across Multiple Language Varieties. Behavior Research Methods 54. 864–884. DOI: 10.3758/s13428-021-01650-1
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF Wordlist](http://cldf.clld.org/v1.0/terms.rdf#Wordlist)
[dc:identifier](http://purl.org/dc/terms/identifier) | https://norare.clld.org
[dc:license](http://purl.org/dc/terms/license) | https://creativecommons.org/licenses/by/4.0/
[dcat:accessURL](http://www.w3.org/ns/dcat#accessURL) | https://github.com/concepticon/norare-cldf
[prov:wasDerivedFrom](http://www.w3.org/ns/prov#wasDerivedFrom) | <ol><li><a href="https://github.com/concepticon/norare-cldf/tree/v1.0.0">concepticon/norare-cldf v1.0.0</a></li><li><a href="https://github.com/glottolog/glottolog/tree/v5.1">Glottolog v5.1</a></li><li><a href="https://github.com/concepticon/norare-data/tree/v1.1">concepticon/norare-data v1.1</a></li><li><a href="https://github.com/concepticon/concepticon-data/tree/v3.4.0">concepticon/concepticon-data v3.4.0</a></li></ol>
[prov:wasGeneratedBy](http://www.w3.org/ns/prov#wasGeneratedBy) | <ol><li><strong>python</strong>: 3.12.3</li><li><strong>python-packages</strong>: <a href="./requirements.txt">requirements.txt</a></li></ol>
[rdf:ID](http://www.w3.org/1999/02/22-rdf-syntax-ns#ID) | norare
[rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type) | http://www.w3.org/ns/dcat#Distribution


## <a name="table-glossescsv"></a>Table [glosses.csv](./glosses.csv)

Words in individual languages to which NoRaRe variables assign norms, ratings or relations.

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF FormTable](http://cldf.clld.org/v1.0/terms.rdf#FormTable)
[dc:extent](http://purl.org/dc/terms/extent) | 142527


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_\-]+` | Primary key
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | A reference to a language (or variety) the form belongs to<br>References [languages.csv::ID](#table-languagescsv)
[Parameter_ID](http://cldf.clld.org/v1.0/terms.rdf#parameterReference) | `string` | A reference to the meaning denoted by the form<br>References [concepticon.csv::ID](#table-concepticoncsv)
[Form](http://cldf.clld.org/v1.0/terms.rdf#form) | `string` | Some datasets provide data without specifying the associated word forms in the studied languages. In these cases, the 'Form' value is set to '<NA>'.
[Segments](http://cldf.clld.org/v1.0/terms.rdf#segments) | list of `string` (separated by ` `) | 
[Comment](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
[Dataset_ID](http://cldf.clld.org/v1.0/terms.rdf#contributionReference) | `string` | References [datasets.csv::ID](#table-datasetscsv)

## <a name="table-concepticoncsv"></a>Table [concepticon.csv](./concepticon.csv)

This table lists the Concepticon conceptsets to which the meaning of words, studied in NoRaRe datasets, are linked, thus providing the backbone for cross-linguistic analysis of NoRaRe data.

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ParameterTable](http://cldf.clld.org/v1.0/terms.rdf#ParameterTable)
[dc:extent](http://purl.org/dc/terms/extent) | 3634


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_\-]+` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 
[ColumnSpec](http://cldf.clld.org/v1.0/terms.rdf#columnSpec) | `json` | 
[Concepticon_ID](http://cldf.clld.org/v1.0/terms.rdf#concepticonReference) | `string` | Identifier of the corresponding concept set in Concepticon
`glosses` | `json` | 
`count_datasets` | `nonNegativeInteger` | 
`count_variables` | `nonNegativeInteger` | 

## <a name="table-datasetscsv"></a>Table [datasets.csv](./datasets.csv)

Datasets in NoRaRe are published studies from which NoRaRe variables were extracted.

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF ContributionTable](http://cldf.clld.org/v1.0/terms.rdf#ContributionTable)
[dc:extent](http://purl.org/dc/terms/extent) | 126


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_\-]+` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Description](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 
[Contributor](http://cldf.clld.org/v1.0/terms.rdf#contributor) | list of `string` (separated by ` and `) | 
[Citation](http://cldf.clld.org/v1.0/terms.rdf#citation) | `string` | 
`Year` | `integer` | 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
`URL` | `anyURI` | 
`Alias` | `string` | 

## <a name="table-languagescsv"></a>Table [languages.csv](./languages.csv)

Languages the words of which were investigated in NoRaRe datasets.

property | value
 --- | ---
[dc:conformsTo](http://purl.org/dc/terms/conformsTo) | [CLDF LanguageTable](http://cldf.clld.org/v1.0/terms.rdf#LanguageTable)
[dc:extent](http://purl.org/dc/terms/extent) | 39


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string`<br>Regex: `[a-zA-Z0-9_\-]+` | Primary key
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Macroarea](http://cldf.clld.org/v1.0/terms.rdf#macroarea) | `string` | 
[Latitude](http://cldf.clld.org/v1.0/terms.rdf#latitude) | `decimal`<br>&ge; -90<br>&le; 90 | 
[Longitude](http://cldf.clld.org/v1.0/terms.rdf#longitude) | `decimal`<br>&ge; -180<br>&le; 180 | 
[Glottocode](http://cldf.clld.org/v1.0/terms.rdf#glottocode) | `string`<br>Regex: `[a-z0-9]{4}[1-9][0-9]{3}` | 
[ISO639P3code](http://cldf.clld.org/v1.0/terms.rdf#iso639P3code) | `string`<br>Regex: `[a-z]{3}` | 

## <a name="table-variablescsv"></a>Table [variables.csv](./variables.csv)

NoRaRe variables, i.e. norms, ratings or relations pertaining to a word in a language, the meaning of which can be mapped to Concepticon.

property | value
 --- | ---
[dc:extent](http://purl.org/dc/terms/extent) | 863


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Dataset_ID](http://cldf.clld.org/v1.0/terms.rdf#contributionReference) | `string` | References [datasets.csv::ID](#table-datasetscsv)
[Language_ID](http://cldf.clld.org/v1.0/terms.rdf#languageReference) | `string` | NoRaRe variables always pertain to words in a single language. (If a study measured a variable for multiple languages, NoRaRe will list multiple variables for the corresponding dataset.)<br>References [languages.csv::ID](#table-languagescsv)
[Name](http://cldf.clld.org/v1.0/terms.rdf#name) | `string` | 
[Note](http://cldf.clld.org/v1.0/terms.rdf#description) | `string` | 
[Other](http://cldf.clld.org/v1.0/terms.rdf#comment) | `string` | 
[Source](http://cldf.clld.org/v1.0/terms.rdf#source) | list of `string` (separated by `;`) | References [sources.bib::BibTeX-key](./sources.bib)
`Category` | `string`<br>Valid choices:<br> `norms` `ratings` `relations` | Variables are categorized as either `norms`, `ratings` or `relations`
`Type` | `string`<br>Valid choices:<br> `cardinality` `linguistic` `logarithmic` `magnitude` `mean` `normalized` `numeric` `object` `ordinality` `percentage` `semantic` `standardized` `sum` `tokens` | Coarse datatype description for the variable
`Method` | `string`<br>Valid choices:<br> `concept lists` `corpus` `dictionaries` `meta` `other` `user` `users` | Keyword describing how values for the variable were determind
`Result` | `string` | Keyword describing what a variable measures
`Datatype` | `json` | CSVW Datatype description of the values for this variable.

## <a name="table-norarecsv"></a>Table [norare.csv](./norare.csv.zip)

A norm, rating or relation assigned to a word as measurement of a variable in a dataset aggregated by NoRaRe.

property | value
 --- | ---
[dc:extent](http://purl.org/dc/terms/extent) | 677593


### Columns

Name/Property | Datatype | Description
 --- | --- | --- 
[ID](http://cldf.clld.org/v1.0/terms.rdf#id) | `string` | Primary key
[Unit_ID](http://cldf.clld.org/v1.0/terms.rdf#formReference) | `string` | References [glosses.csv::ID](#table-glossescsv)
`Variable_ID` | `string` | References [variables.csv::ID](#table-variablescsv)
`Value` | `string` | A measurement of a variable for a particular word, typed according to the 'Datatype' column of the associated variable.

