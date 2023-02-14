# filter

## What

The purpose of the `filter` command is to provide a easy-to-use graphical-user interface to allow users to:

- **explore** the different AncientMetagenomeDir tables via drop down menus
- **filter** a given table based on different criteria using a standard tabular interface
- **download** the resulting sequencing data via different methods
- **download** prepared input samplesheets for pipelines
- **download** citation information of selected samples

## When

You should use this tool when you wish to find particular types of ancient metagenomic data, but wish to explore the dataset manually and interactively (i.e., don't know exactly what you're looking for yet), and/or if you do not wish to download the AncientMetagenomeDir full tables yourself and filter them within languages such as R or Python (with pandas).

## How

### Loading the interface

Before using `AMDirT filter` make sure you have modern web-browser (Chrome, Firefox, Edge, Safari etc.) available on your machine. This will in most cases be your own laptop or desktop - not a server.

To open the graphical user interface, open a terminal (activating software environments if necessary, see [AMDirT Installation Page](https://github.com/SPAAM-community/AMDirT/)) and run:

```bash
AMDirT filter
```

Your web-browser should automatically open a new tab and have the `filter` interface open for you. If your browser does not automatically open, just copy and paste one of the URLs present in the console in your web browsers URL bar.

```text
  Local URL: http://localhost:8501
  Network URL: http://172.0.0.0:8501
```

> ⚠️ _The first time you run the command, you first may get some prompts in your terminal. You can just say 'no' to all - this will not affect the usage of the tool._

![AMDirT welcome page with sidebar](images/amdirt-filter-welcome.png)

Once opened you should see a side bar and a empty pane. You can use the side bar to select various aspects of the displayed data from the AncientMetagenomeDir tables, such as the release, which table you view (e.g., environmental or host-associated metagenomics) and the number of rows to display. The data download option controls which tool the resulting download script will use to get the data.

![AMDirT side bar with version dropdown menu](images/amdirt-filter-version-select.png)

![AMDirT side bar with table dropdown menu](images/amdirt-filter-table-select.png)

![AMDirT side bar with download method menu](images/amdirt-filter-downloadmethod-select.png)

Once you have selected a version and a table, the table itself should open in the empty pane.

> In most cases the most version is recommended, whereby you pick the most recent date e.g. v22.12 over v22.09 from December and September 2022 respectively

To help decide which download method to use, see the [Miscellaneous page](miscellaneous.md).

### Exploring the Tables

To navigate the tables you can scroll up and down with your mouse. To side scroll you can hold shift and scroll. To go to the next page of samples, you can find the forward/back buttons in the bottom right of the table to navigate across pages of data entries.

To filter the tables, hover your cursor over the column of interest and you should see a 'hamburger' icon, press this to open the filter and table formatting options.

![AMDirT column configuration with row ordering options](images/amdirt-filter-column-order.png)

![AMDirT column configuration with row filtering options](images/amdirt-filter-column-filter.png)

![AMDirT column configuration with column selection options](images/amdirt-filter-column-select.png)

With this pane and tabs you can:

- Change the size and row ordering of the column (e.g. pin this column to the left or right)
- Filter the rows by various operations on this column (equal, not equal, within range, etc.)
- Change which columns are displayed overall

You can also re-order the order of columns across the table by click and holding the column name, and dragging left and right.

### Exporting Information

Now, select all the samples you wish to download and/or analyse.

You can select all samples currently displayed by clicking the empty box on the project_name column, or you can select individual samples by clicking the empty boxes on these rows in the project_name column.

![AMDirT Selecting all samples currently in table](images/amdirt-filter-select-all.png)

![AMDirT Selecting individual samples from the current table](images/amdirt-filter-select-single-samples.png)

Now validate your selection! Press the 'Validate selection' button at the bottom of the table.

> ⚠️ _If you wish to download the data, make sure you have already selected your 'Data download method' in the sidebar before pressing 'Validate selection'!_

Once the select is validated, more buttons will appear allowing you to download different files:

- a download script: contains a bash script with download commands
- a pipeline input samplesheet: a pre-configured input sheet for a pipeline, based on the downloaded files
- a citations file: citation information in BibTex format for selected samples

![AMDirT buttons after selection validation](images/amdirt-filter-validate-buttons.png)

To use the **download** script, you can simply run:

```bash
bash ancientMetagenomeDir_curl_download_script.sh
```

and the sequencing files of the selected samples will be downloaded to the directory you run the script from.

> ⚠️ _You must already have the download tool you have selected configured on your machine to use the bash script!_

> ⚠️ _Make sure you only run this script on the machine you will run your analyses from, i.e. in most cases on a server or HPC!_

To use the **pipeline input samplesheet**, you should always double check the sheet is correctly configured. Once you have validated it, you can supply it to your selected pipeline as follows (using nf-core/eager as an example):

```bash
nextflow run nf-core/eager <...> --input ancientMetagenomeDir_eager_input.csv
```

The **citations bibtex** file contains all the citation information of your selected samples in a widely used format called BibTex. You can import this file into most referencing or bibliography managing tools (Zotero, Paperpile etc.).

> ⚠️ _Occasionally the cross-ref databases do not have citation information for certain publications. You will receive a warning if so, with the relevant DOIs for you to manually get this information._

### Finishing

If you have finished your selection and file downloading, you can close the interface simply by closing the tab, and then pressing <kbd>Ctrl</kbd> + <kbd>c</kbd> on your terminal.

If you wish to generate a new selection in the same session, you **must** press the 'Start New Selection' button at the bottom of the interface, select the new samples, and press 'Validate selection' again. If you do not press 'Start New Selection', you will export the same set of files and samples from your first selection.
