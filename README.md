# FixFAST5
Fixing Oxford Nanopore FAST5 files which are missing entries.

The scripts were written by [HalfPhoton](https://github.com/HalfPhoton) and provided in a [github issue](https://github.com/nanoporetech/pod5-file-format/issues/97). I am just bringing them together here to make it easier on myself should I come accross this problem again in the future. 

The scripts in this repository require [pod5 tools](https://pod5-file-format.readthedocs.io/) to be installed.

## Find problems in FAST5 files

```
python find_fast5_issues.py FOLDER_CONTAINING_FAST5_FILES/
```

## Extract bad reads

```
grep -o "read_[0-9a-f-]*" issues.txt > bad_reads.txt
```

## Delete broken entries from FAST5 files

```
python delete_fast5_reads.py FOLDER_CONTAINING_FAST5_FILES/ bad_reads.txt
```

## All in one

```
python find_fast5_issues.py FOLDER_CONTAINING_FAST5_FILES/ && \
grep -o "read_[0-9a-f-]*" issues.txt > bad_reads.txt && \
python delete_fast5_reads.py FOLDER_CONTAINING_FAST5_FILES/ bad_reads.txt
```