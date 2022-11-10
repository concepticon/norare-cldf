# Releasing NoRaRe CLDF

- update `raw/norare-data` and `raw/concepticon-data` to the corresponding released versions
- recreate the CLDF dataset:
  ```shell
  cldfbench makecldf --with-cldfreadme cldfbench_norare.py --glottolog-version v4.6
  ```
- check validity:
  ```shell
  pytest
  ```
- recreate the metadata for Zenodo:
  ```shell
  cldfbench zenodo cldfbench_norare.py
  ```
- recreate the wordcloud for the README and the correlation plot for the docs:
  ```shell
  cldfbench norare.wordcloud -o doc/wc.png
  cldfbench norare.correlation -o doc/corr.png
  ```
- recreate the README:
  ```shell
  cldfbench readme cldfbench_norare.py 
  ```
