# convert

## What

The purpose of the `convert` command is to convert AncientMetagenomeDir tables to input sheets for different pipelines and software. It will also download citation information for you.

It is a partial command-line equivalent to the `filter` graphical user interface.

## When

You typically will use `convert` if you are a command-line power user, and prefer to perform table filtering and sample selection programmtically (e.g. in R or python) rather than in a graphical-user-interface.

## How

The following description assumes that you have already have a AncientMetagenomeDir **samples** table that has been filtered to the samples you wish to run through a given pipeline(s).

> ⚠️ _The header, and present columns etc. should match exactly that on AncientMetagenomeDir, only rows may be removed._

To generate sample sheets of the support pipelines, you can run the command (an example being a filtered `ancientmetagenome-hostassociated_samples_warinnersamplesonly.tsv` table):

```bash
mkdir samplesheets/
AMDirT convert ancientmetagenome-hostassociated_samples_warinnersamplesonly.tsv ancientmetagenome-hostassociated -o samplesheets/
```

where you provide the filtered TSV, which AncientMetagenomeDir samples table the filtered table is derived from, and then the output directory where the samplesheets should be saved into.

The output is as follows:

- `<outdir>`: where all the pipeline samplesheets are placed
- `AncientMetagenomeDir_citations.bib`: a BibTex format citation information file

To use a **pipeline input samplesheet**, you should always double check the sheet is correctly configured. Once you have validated it, you can supply it to your selected pipeline as follows (using nf-core/eager as an example):

```bash
nextflow run nf-core/eager <...> --input ancientMetagenomeDir_eager_input.csv
```

The **citations BibTex** file contains all the citation information of your selected samples in a widely used format called BibTex. You can import this file into most referencing or bibliography managing tools (Zotero, Paperpile etc.).

> ⚠️ _Occasionally the cross-ref databases do not have citation information for certain publications. You will receive a warning if so, with the relevant DOIs for you to manually get this information._
