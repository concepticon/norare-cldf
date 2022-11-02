"""

"""
import sqlite3

from PIL import Image
from clldutils.clilib import PathType

QUERY = """
SELECT
  cid,
  avg(CASE WHEN vid = 'Scott-2019-Ratings-ENGLISH_AROUSAL_MEAN' THEN cast(v as float) ELSE null END) AS English,
  avg(CASE WHEN vid = 'Moors-2013-Ratings-DUTCH_AROUSAL_MEAN' THEN cast(v as float) ELSE null END) AS Dutch
FROM (
SELECT
  f.cldf_parameterReference as cid, v.Value as v, v.Variable_ID as vid
FROM
  FormTable as f, `unit-values.csv` as v
WHERE
  (v.Variable_ID = 'Scott-2019-Ratings-ENGLISH_AROUSAL_MEAN' OR v.Variable_ID = 'Moors-2013-Ratings-DUTCH_AROUSAL_MEAN')
  AND v.cldf_formReference = f.cldf_id) AS vals
GROUP BY cid
HAVING English > 0 AND Dutch > 0
"""


def register(parser):
    parser.add_argument('db', type=PathType(type='file'))


def run(args):
    try:
        import pandas as pd
        import seaborn as sns
    except ImportError:
        args.log.error('Please install the dataset with "pip install -e .[correlation]"')
        return
    plot = sns.lmplot(x="English", y="Dutch", data=pd.read_sql(QUERY, sqlite3.connect(args.db)))
    plot.fig.savefig("out.png")
    Image.open('out.png').show()
