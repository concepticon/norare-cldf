import pathlib
import subprocess
import collections

import pycountry
from csvw import TableGroup
from pycldf import Source
from cldfbench import Dataset as BaseDataset, CLDFSpec
from pyconcepticon import Concepticon
from pybtex.database import parse_string
from clldutils.markup import iter_markdown_tables, iter_markdown_sections
from clldutils.markup import MarkdownLink

# Map macrolanguages to the "most standard" language (mainly to get coordinates)
ISO_MAP = {
    'zho': 'cmn',
    'ara': 'arb',
    'msa': 'zsa',
    'fas': 'pes',
    'est': 'ekk',
    'swa': 'swh'}


def glosses_by_language(
        api, langs=('english', 'german', 'french', 'spanish', 'chinese', 'russian', 'portuguese')):
    res = collections.defaultdict(lambda: collections.defaultdict(set))
    for cl in api.conceptlists.values():
        slangs = [n.lower() for n in cl.source_language if n.lower() in langs]

        for i, c in enumerate(cl.concepts.values(), start=1):
            if c.concepticon_id:
                if c.english and 'english' in slangs:
                    res[int(c.concepticon_id)]['english'].add(c.english.lower())
                for k, v in c.attributes.items():
                    if k in slangs:
                        if v:
                            res[int(c.concepticon_id)][k].add(v.lower())
    return res


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "norare"

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(
            dir=self.cldf_dir,
            module='Wordlist',
            data_fnames=dict(
                ParameterTable='concepticon.csv',
                FormTable='glosses.csv',
                ContributionTable='datasets.csv',
            ),
            zipped=['norare.csv'],
        )

    def cmd_download(self, args):
        subprocess.check_call(
            'git -C {} pull --recurse-submodules'.format(self.dir.resolve()), shell=True)

    def cmd_readme(self, args):
        desc = """
This CLDF dataset provides the data of the corresponding release of
[concepticon/norare-data](https://github.com/concepticon/norare-data) as CLDF Wordlist.
The latest release of this dataset can be browsed in a clld web application at 
[https://norare.clld.org](https://norare.clld.org).
Information on how to use the data is available at [doc](doc/).

![wordcloud](doc/wc.png)
"""
        pre, head, post = super().cmd_readme(args).partition('## CLDF ')
        return pre + desc + head + post

    def get_tg(self, dsid):
        d = self.raw_dir / 'norare-data' / 'datasets' / dsid
        if not d.exists():
            d = self.raw_dir / 'concepticon-data' / 'concepticondata' / 'conceptlists'
        return d, TableGroup.from_file(d / '{}.tsv-metadata.json'.format(dsid))

    def schema(self, cldf):
        t = cldf.add_component('LanguageTable')
        t.common_props['dc:description'] = \
            "Languages the words of which were investigated in NoRaRe datasets."
        cldf.add_columns(
            'ParameterTable',
            {
                "name": "Concepticon_ID",
                "dc:description": "Identifier of the corresponding concept set in Concepticon",
                "valueUrl": "http://concepticon.clld.org/parameters/{Concepticon_ID}",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#concepticonReference",
            },
            # We need all labels for the concepts in the following languages for matching:
            # English German Chinese French Spanish Russian Portuguese
            {"name": "glosses", "datatype": "json"},
            {"name": "count_datasets", "datatype": "nonNegativeInteger"},
            {"name": "count_variables", "datatype": "nonNegativeInteger"},
        )
        cldf['ParameterTable'].common_props['dc:description'] = \
            "This table lists the Concepticon conceptsets to which the meaning of words, studied " \
            "in NoRaRe datasets, are linked, thus providing the backbone for cross-linguistic " \
            "analysis of NoRaRe data."
        cldf.add_columns(
            'FormTable',
            {
                "name": "Dataset_ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#contributionReference"}
        )
        cldf['FormTable'].common_props['dc:description'] = \
            "Words in individual languages to which NoRaRe variables assign norms, ratings or " \
            "relations."
        cldf['FormTable', 'Form'].common_props['dc:description'] = \
            "Some datasets provide data without specifying the associated word forms in the " \
            "studied languages. In these cases, the 'Form' value is set to '<NA>'."
        t = cldf.add_table(
            'variables.csv',
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id"},
            {
                "name": "Dataset_ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#contributionReference"},
            {
                "name": "Language_ID",
                "dc:description": "NoRaRe variables always pertain to words in a single language. "
                                  "(If a study measured a variable for multiple languages, NoRaRe "
                                  "will list multiple variables for the corresponding dataset.)",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#languageReference"},
            {
                "name": "Name",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#name"},
            {
                "name": "Note",
                "dc:format": "text/markdown",
                "dc:conformsTo": "CLDF markdown",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#description"},
            {
                "name": "Other",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#comment"},
            {
                "name": "Source",
                "separator": ";",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#source"},
            {
                "name": "Category",
                "dc:description": "Variables are categorized as either `norms`, `ratings` or `relations`",
                "datatype": {"base": "string", "format": "norms|ratings|relations"}},
            {
                "name": "Type",
                "dc:description": "Coarse datatype description for the variable",
                "datatype": {"base": "string", "format": "cardinality|linguistic|logarithmic|magnitude|mean|normalized|numeric|object|ordinality|percentage|semantic|standardized|sum|tokens"}},
            {
                "name": "Method",
                "dc:description": "Keyword describing how values for the variable were determind",
                "datatype": {"base": "string", "format": "concept lists|corpus|dictionaries|meta|other|user|users"}},
            {
                "name": "Result",
                "dc:description": "Keyword describing what a variable measures"},
            {
                "name": "Datatype",
                "dc:description": "CSVW Datatype description of the values for this variable.",
                "datatype": "json"},
        )
        t.common_props['dc:description'] = \
            "NoRaRe variables, i.e. norms, ratings or relations pertaining to a word in a " \
            "language, the meaning of which can be mapped to Concepticon."
        t = cldf.add_table(
            'norare.csv',
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id"},
            {
                "name": "Unit_ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#formReference"},
            'Variable_ID',
            {
                'name': 'Value',
                'dc:description': "A measurement of a variable for a particular word, typed "
                                  "according to the 'Datatype' column of the associated variable."},
        )
        t.common_props['dc:description'] = \
            "A norm, rating or relation assigned to a word as measurement of a variable in a " \
            "dataset aggregated by NoRaRe."
        cldf.add_foreign_key('norare.csv', 'Variable_ID', 'variables.csv', 'ID')
        cldf.add_columns(
            'ContributionTable',
            {"name": "Year", "datatype": "integer"},
            {
                "name": "Source",
                "separator": ";",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#source"},
            {
                "name": "URL",
                "datatype": "anyURI"},
            {
                "name": "Alias"}
        ),
        cldf['ContributionTable'].common_props['dc:description'] = \
            "Datasets in NoRaRe are published studies from which NoRaRe variables were extracted."
        cldf['ContributionTable', 'Contributor'].separator = ' and '
        cldf['ContributionTable', 'Description'].common_props.update({
            "dc:format": "text/markdown",
            "dc:conformsTo": "CLDF markdown"})

    def cmd_makecldf(self, args):
        contribs = [
            "# Contributors\n",
            "Name | Role",
            "--- | ---",
        ]
        contributors_md = {
            h.replace('#', '').strip(): text for _, h, text in iter_markdown_sections(
                self.raw_dir.joinpath('norare-data', 'CONTRIBUTORS.md').read_text(encoding='utf8'))
        }
        header, rows = next(iter_markdown_tables(contributors_md['Editors']))
        for row in rows:
            ed = dict(zip(header, row))
            if ed['Period'].endswith('-'):
                contribs.append('{} | author'.format(ed['Name']))
        contribs.append('\n\n## Grant information\n\n{}'.format(contributors_md['Grant information']))
        self.dir.joinpath('CONTRIBUTORS.md').write_text('\n'.join(contribs), encoding='utf8')
        self.schema(args.writer.cldf)
        glosses_by_id = glosses_by_language(Concepticon(self.raw_dir / 'concepticon-data'))
        glbyiso = {lg.iso: lg for lg in args.glottolog.api.languoids()}
        tgs, langs, cs, units = {}, set(), set(), set()
        count_datasets = collections.defaultdict(set)
        count_variables = collections.defaultdict(set)

        sources = {}
        for p in [['norare-data'], ['concepticon-data', 'concepticondata']]:
            for key, entry in parse_string(
                    self.raw_dir.joinpath(*p + ['references', 'references.bib'])
                            .read_text(encoding='utf8'),
                    'bibtex').entries.items():
                sources[key] = Source.from_entry(
                    key, entry,
                    _check_id=False,
                    _lowercase=True,
                    _strip_tex=[
                        'author', 'editor', 'title', 'number', 'abstract', 'publisher',
                        'booktitle', 'url', 'series', 'journal'])

        dssmd = {
            r['ID']: r for r in self.raw_dir.joinpath('norare-data').read_csv(
                'datasets.tsv', delimiter='\t', dicts=True)}
        dssmd.update({
            r['ID']: r for r in self.raw_dir.joinpath(
                'concepticon-data', 'concepticondata').read_csv(
                    'conceptlists.tsv', delimiter='\t', dicts=True)
        })
        csdefs = {
            r['ID']: r['DEFINITION'] for r in self.raw_dir.joinpath(
                'concepticon-data', 'concepticondata').read_csv(
                'concepticon.tsv', delimiter='\t', dicts=True)
        }

        def links(ml):
            if ml.url.startswith(':bib:'):
                rid = ml.url.replace(':bib:', '')
                args.writer.cldf.sources.add(sources[rid])
                return MarkdownLink(ml.label, 'sources.bib#cldf:{}'.format(rid))
            if ml.url.startswith(':ref:'):
                # References to conceptlists only work within Concepticon!
                return ml.label
            return ml

        for row in self.raw_dir.joinpath('norare-data').read_csv(
                'norare.tsv', delimiter='\t', dicts=True):
            # Each row is a variable, related to a form via Language, e.g. LANGUAGE = 'en' means,
            # we expect a column "ENGLISH" in the dataset!
            dsid = row['DATASET']
            if dsid not in tgs:
                d, tgs[dsid] = self.get_tg(dsid)
                dsmd = dssmd[dsid]
                if dsmd['REFS']:
                    args.writer.cldf.sources.add(sources[dsmd['REFS']])
                args.writer.objects['ContributionTable'].append(dict(
                    ID=dsid,
                    Name=dsid.replace('-', ' '),
                    Description=MarkdownLink.replace(dsmd['NOTE'], links),
                    Contributor=dsmd['AUTHOR'].replace('AND', 'and').split(' and '),
                    Year=int(dsmd['YEAR']),
                    Source=[dsmd['REFS']],
                    URL=dsmd['URL'],
                    Alias=dsmd['ALIAS'],
                ))
            column = tgs[dsid].tables[0].tableSchema.columndict[row['NAME']]

            lg = row['LANGUAGE']
            lg = pycountry.languages.get(**{'alpha_2' if len(lg) == 2 else 'alpha_3': lg})
            lgname = {
                'Modern Greek (1453-)': 'GREEK',
                'Scottish Gaelic': 'GAELIC',
                'Malay (macrolanguage)': 'MALAY',
                'Armenian': 'WESTERNARMENIAN',
            }.get(lg.name, lg.name)
            if dsid.startswith('Luniewska') and lgname == 'Arabic':
                lgname = 'LEBANESEARABIC'
            lgname = lgname.upper().replace(' ', '_')

            gl = glbyiso[ISO_MAP.get(lg.alpha_3, lg.alpha_3)]
            if gl.id not in langs:
                args.writer.objects['LanguageTable'].append(dict(
                    ID=lg.alpha_3,
                    Name=lg.name,
                    Description=lg.alpha_3,
                    Latitude=gl.latitude,
                    Longitude=gl.longitude,
                    Glottocode=gl.id,
                ))
                langs.add(gl.id)

            # Add a Unit-Parameter
            upid = '{}-{}'.format(dsid, row['NAME'])
            colspec = column.asdict()
            if 'valueUrl' in colspec:
                colspec['valueUrl'] = str(column.valueUrl).replace(row['NAME'], 'Value')
            args.writer.objects['variables.csv'].append(dict(
                ID=upid,
                Dataset_ID=dsid,
                Language_ID=lg.alpha_3,
                Note=MarkdownLink.replace(row['NOTE'], links),
                Other=row['OTHER'],
                Datatype=colspec,
                Category=row['NORARE'],
                Method=row['RATING'],
                Type=row['STRUCTURE'],
                Result=row['TYPE'],
                Source=[row['SOURCE']] if row['SOURCE'] else [],
            ))
            if row['SOURCE']:
                args.writer.cldf.sources.add(sources[row['SOURCE']])

            for lineno, r in enumerate(tgs[dsid].tables[0], start=1):
                if r[row['NAME']] is None:
                    continue
                if not r['CONCEPTICON_ID'] or (r['CONCEPTICON_ID'] == '0'):
                    continue
                elif r['CONCEPTICON_ID'] not in cs:
                    args.writer.objects['ParameterTable'].append(dict(
                        ID=r['CONCEPTICON_ID'],
                        Name=r['CONCEPTICON_GLOSS'],
                        Description=csdefs[str(r['CONCEPTICON_ID'])],
                        Concepticon_ID=r['CONCEPTICON_ID'],
                        glosses={
                            k: sorted(v) for k, v in
                            glosses_by_id[int(r['CONCEPTICON_ID'])].items()}))
                    cs.add(r['CONCEPTICON_ID'])
                if r['CONCEPTICON_ID']:
                    count_datasets[r['CONCEPTICON_ID']].add(dsid)
                    count_variables[r['CONCEPTICON_ID']].add(upid)
                # Units (aka glosses or translation equivalents) are identified by
                # - dataset
                # - language
                # - concept (via line number)
                uid = '{}-{}-{}'.format(dsid, gl.id, lineno)
                # Three datasets are known to have missing forms.
                assert dsid in ['Calude-2011-200', 'Gampe-2017-48', 'OmegaWiki'] or lgname in r
                if uid not in units:
                    args.writer.objects['FormTable'].append(dict(
                        ID=uid,
                        Language_ID=lg.alpha_3,
                        Parameter_ID=r['CONCEPTICON_ID'] or '0',
                        Dataset_ID=dsid,
                        Form=r.get(lgname) or '<NA>',
                    ))
                    units.add(uid)
                uvid = '{}-{}-{}'.format(dsid, row['NAME'], lineno)
                args.writer.objects['norare.csv'].append(dict(
                    ID=uvid,
                    Unit_ID=uid,
                    Variable_ID=upid,
                    Value=column.write(r[row['NAME']]),
                ))
        for p in args.writer.objects['ParameterTable']:
            p['count_datasets'] = len(count_datasets.get(p['ID'], []))
            p['count_variables'] = len(count_variables.get(p['ID'], []))
