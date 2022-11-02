"""
Create a wordcloud from the tags used to describe NoRaRe variables.
"""
from clldutils.clilib import PathType
from wordcloud import WordCloud

from cldfbench_norare import Dataset


def register(parser):
    parser.add_argument('-o', '--output', type=PathType(must_exist=False), default=None)


def run(args):
    ds = Dataset().cldf_reader()
    wc = WordCloud().generate(' '.join([r['Tag'] for r in ds['unit-parameters.csv']]))
    img = wc.to_image()
    if args.output:
        img.save(str(args.output))
    else:
        img.show()
