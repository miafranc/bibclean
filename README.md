# bibclean - Clean BibTeX file

Cleans a BibTeX database removing unused references

```
usage: bib_parse.py [-h] [--cites <file.tex>] [--dups <file.bib>] {clean} ...

positional arguments:
  {clean}
    clean             Clean a .bib file, i.e. remove unused bib entries.

options:
  -h, --help          show this help message and exit
  --cites <file.tex>  Extract cites from a .tex file.
  --dups <file.bib>   Find duplicate entries in a .bib file.
```

```
bib_parse.py clean [-h] --bib <in.bib> --tex <main.tex> --out <out.bib>

options:
  -h, --help        show this help message and exit
  --bib <in.bib>    Input BibTeX file.
  --tex <main.tex>  Main TeX file.
  --out <out.bib>   Output BibTeX file.
```
