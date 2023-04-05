# AMDirT viewer

## Downloading the sequencing data of selected libraries

AMDirT provides three different methods to download the sequencing data of selected libraries from public archives:

- direct download from the FTP server using curl
- direct download via the FASP protocol using ASPERA
- indirect download via the Nextflow pipeline nf-core/fetchngs

### Downloading via curl

### Downloading via the FASP protocol using ASPERA

[FASP](https://en.wikipedia.org/wiki/Fast_and_Secure_Protocol) is a specific protocol that allows the download of large data files at a speed that is usually much higher than when downloading from the FTP server.

Prior to be able to download via this method, make sure that you have the ASPERA connect installed on your system (using `which ascp`). If this is not the case, please refer to this [installation guide](https://www.ibm.com/docs/en/aspera-connect/4.1?topic=suc-installation#installation__section_zfj_wpq_ghb) and download the binary from [here](https://www.ibm.com/aspera/connect/). You can also install this via conda (`conda create -n aspera -c HCC aspera-cli`)

AMDirT will return a script that for each sequencing file looks like this following the recommendation from [ENA](https://ena-docs.readthedocs.io/en/latest/retrieval/file-download.html#using-aspera):

```bash
ascp -QT -l 300m -P 33001 -i path/to/aspera/installation/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:path/to/sequencing/file local/target/directory

AMDirT will automatically replace `path/to/sequencing/file` to match the paths for the libraries that were selected. It will also set the `local/target/directory` to the current directory.

However, you will need to set the `path/to/aspera/installation` prior to running this. To make it more convenient, we opted for using the environment variable `ASPERA_PATH` that has to be set in the shell prior to running the script. Therefore, run:

```bash
ASPERA_PATH="$HOME/.aspera/cli"

> ⚠️ In case your institute blocks the port 33001, you will need to change the parameter `-P 33001` to another port that is not blocked.

### Downloading via nf-core/fetchngs
