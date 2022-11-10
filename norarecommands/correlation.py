"""
"""
import sqlite3

from PIL import Image
from clldutils.clilib import PathType
from pycldf import Database
from cldfbench_norare import Dataset

QUERY = """
SELECT
  cid,
  avg(CASE WHEN vid = '{0}' THEN cast(v as float) ELSE null END) AS x,
  avg(CASE WHEN vid = '{1}' THEN cast(v as float) ELSE null END) AS y
FROM (
SELECT
  f.cldf_parameterReference as cid, v.Value as v, v.Variable_ID as vid
FROM
  FormTable as f, `norare.csv` as v
WHERE
  (v.Variable_ID = '{0}' OR v.Variable_ID = '{1}')
  AND v.cldf_formReference = f.cldf_id) AS vals
GROUP BY cid
HAVING x > 0 AND y > 0
"""

CORRS = [
    [
        'Scott-2019-Ratings',
        'Cortese-2008-AoA',
        'english_aoa_mean',
        'english_aoa_mean',
    ],
    [
        'Scott-2019-Ratings',
        'Warriner-2013-AffectiveRatings',
        'english_arousal_mean',
        'english_arousal_mean',
    ],
    [
        'Brysbaert-2014-Concreteness',
        'Scott-2019-Ratings',
        'english_concreteness_mean',
        'english_concreteness_mean',
    ],
    [
        'Scott-2019-Ratings',
        'Warriner-2013-AffectiveRatings',
        'english_dominance_mean',
        'english_dominance_mean',
    ],
    [
        'Scott-2019-Ratings',
        'Warriner-2013-AffectiveRatings',
        'english_valence_mean',
        'english_valence_mean',
    ],
    [
        'GonzalezNosti-2014-LexicalDecision',
        'Alonso-2015-AoA',
        'spanish_aoa_mean',
        'spanish_aoa_mean',
    ],
    [
        'Cuetos-2011-Frequency',
        'Alonso-2011-OralFrequency',
        'spanish_frequency_log',
        'spanish_frequency_log',
    ],
    [
        'Alonso-2016-AoA',
        'Luniewska-2019-299',
        'spanish_aoa_mean',
        'spanish_aoa',
    ],
    [
        'Cuetos-2011-Frequency',
        'Desrochers-2010-330',
        'spanish_frequency_log',
        'subjective_freq_mean',
    ],
    [
        'Luniewska-2019-299',
        'Kuperman-2012-AoA',
        'english_aoa',
        'english_aoa_mean',
    ],
    [
        'Lynott-2013-400',
        'Lynott-2019-Sensorimotor',
        'olfactory_mean',
        'english_olfactory_mean',
    ]
]
CORRS = [
    ('{}-{}'.format(ds1, v1.upper()), '{}-{}'.format(ds2, v2.upper()))
    for ds1, ds2, v1, v2 in CORRS]


def register(parser):
    parser.add_argument(
        '--db',
        help="SQLite database created from the CLDF dataset via 'cldf createdb'",
        type=PathType(type='file'),
        default=None)
    parser.add_argument('-x', default='Scott-2019-Ratings-ENGLISH_AROUSAL_MEAN')
    parser.add_argument('-y', default='Moors-2013-Ratings-DUTCH_AROUSAL_MEAN')
    parser.add_argument('-o', default='correlation.png')


def run(args):
    if args.db is None:
        db = Database(Dataset().cldf_reader())
        db.write_from_tg()
        conn = db.connection()
    else:
        conn = sqlite3.connect(str(args.db))
    try:
        import pandas as pd
        import seaborn as sns
    except ImportError:
        args.log.error('Please install the dataset with "pip install -e .[correlation]"')
        return
    plot = sns.lmplot(x='x', y='y', data=pd.read_sql(QUERY.format(args.x, args.y), conn))
    plot.set(title='x: {} vs. y: {}'.format(args.x, args.y))
    plot.fig.savefig(args.o, bbox_inches='tight')
    Image.open(args.o).show()
