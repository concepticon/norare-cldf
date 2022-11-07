"""
Create a wordcloud from the tags used to describe NoRaRe variables.
"""
import collections

from clldutils.clilib import PathType
from wordcloud import WordCloud

from cldfbench_norare import Dataset


def register(parser):
    parser.add_argument('-o', '--output', type=PathType(must_exist=False), default=None)


def run(args):
    ds = Dataset().cldf_reader()
    wc = WordCloud().generate_from_frequencies(
        collections.Counter([r['Tag'] for r in ds['variables.csv']]))
    img = wc.to_image()
    if args.output:
        img.save(str(args.output))
    else:
        img.show()
