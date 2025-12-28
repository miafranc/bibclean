import re
from pprint import pprint
from collections import Counter
import argparse


def get_cites(texfile: str, cite_commands: list[str] = ['cite', 'citep', 'citet']) -> set[str]:
    f = open(texfile, 'r', encoding='utf-8')
    tex_lines = f.read()
    f.close()
    # Deleting comments:
    tex_lines = re.sub(r'%.*', '', tex_lines)

    # Finding cites:        
    refs = set()
    for c in cite_commands:
        refs = refs.union(set([y.strip() for x in re.findall(r'\\' + c + '{([^}]+)', tex_lines) for y in x.split(',')]))

    return refs


def find_dups(bibfile: str) -> dict[str, int]:
    f = open(bibfile, 'r', encoding='utf-8')
    bibtex = f.read()
    f.close()

    bibs = [x.strip() for x in re.findall(r'@[^{]+{([^,]+)', bibtex)]

    return dict(filter(lambda x: x[1] > 1, Counter(bibs).items()))


def clean_bib(bibfile: str, outbibfile: str, keys: set[str]) -> None:
    f = open(bibfile, 'r', encoding='utf-8')
    bibtex = f.read()
    f.close()

    entries = {}
    prev_key = ''
    prev_i1 = 0
    for idx, r in enumerate(re.finditer(r'@[^{]+{([^,]+)', bibtex)):
        i1 = r.start(0)
        if idx > 0:
            entries[prev_key] = bibtex[prev_i1:i1]
        prev_key = bibtex[r.start(1):r.end(1)]
        prev_i1 = i1
    entries[prev_key] = bibtex[prev_i1:]

    f = open(outbibfile, 'w', encoding='utf-8')
    for k, v in entries.items():
        if k in keys:
            f.write(v.strip() + '\n\n')
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cites', required=False, metavar='<file.tex>', help='Extract cites from a .tex file.')
    parser.add_argument('--dups', required=False, metavar='<file.bib>', help='Find duplicate entries in a .bib file.')
    subparsers = parser.add_subparsers()
    parser_clean = subparsers.add_parser('clean', help='Clean a .bib file, i.e. remove unused bib entries.')
    parser_clean.add_argument('--bib', required=True, metavar='<in.bib>', help='Input BibTeX file.')
    parser_clean.add_argument('--tex', required=True, metavar='<main.tex>', help='Main TeX file.')
    parser_clean.add_argument('--out', required=True, metavar='<out.bib>', help='Output BibTeX file.')
    
    args = parser.parse_args()

    if args.cites:
        refs = get_cites(args.cites)
        pprint(refs)
    elif args.dups:
        dups = find_dups(args.dups)
        pprint(dups)
    elif args.bib: # clean
        refs = get_cites(args.tex)
        clean_bib(args.bib, args.out, refs)
