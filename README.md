# CytoSPACE: Optimal mapping of scRNA-seq data to spatial transcriptomics data

**CytoSPACE** is a novel computational strategy for assigning single-cell transcriptomes to in situ spatial transcriptomics data, in case that spatial transcriptomics (ST) measurements may contain contributions from multiple cells. Our method solves single cell/spot assignment by minimizing a correlation-based cost function through a linear programming-based optimization routine. 

The key innovations of our method are:

- In contrast to conventional methods, CytoSPACE dissects spatial organizations of cells in a given tissue at single cell level.

- Since our method maps single cells from scRNA-sequencing data, in which larger numbers of genes are sequenced per each cell compared to available spatial transcriptomics technology, our method imporves the gene coverage of a recontructed tissue significantly.

### Installation
To install Cytospace please clone this repository, and install <a href="https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html" target="_blank">Miniconda</a> if not already available.

To create an environment with the required dependencies:

    conda env create -f cytospace.yml

Now you can install CytoSPACE by executing:

    pip install .


### File format
CytoSPACE requires 5 files as input. All files should be provided in tab-delimited tabular input format (.txt) with no double quotations. Further formatting details for each input file are specified below:

1. __A scRNA-seq gene expression file:__
- The matrix must be genes (rows) by cells (columns).
- The first row must contain the single cell IDs and the first column must contain the gene names.
- The gene expression data should be represented as non-normalized counts. 

2. __A cell type label file:__
- Cell type labels corresponding to the single cell IDs in the scRNA-seq gene expression matrix. 
- The table should contain two columns, where column 1 contains the single cell IDs corresponding to the columns of the scRNA-seq matrix and column 2 contains the corresponding cell type labels.
- The columns must have a header. 

3. __A spatial transcriptomics (ST) gene expression file:__
- The matrix must be genes (rows) by ST spots (columns).
- The first row must contain the ST spot IDs and the first column must contain the gene names.
- The gene expression data should be represented as non-normalized counts. 

4. __A spatial transcriptomics coordinates file:__
- A table consisting of 3 columns, where the first column contains the ST spot IDs corresponding to the columns of the ST gene expression matrix, and column 2 and 3 contain the X and Y coordinates of the spatial transcriptomics data, respectively. 
- The columns must have a header. 

5. __A file with cell type fraction estimates, obtained from the `R` script `get_cellfracs_seuratv3.R`.__ 
- A table consisting of 2 rows, where the first row is the cell type labels, and the second row is the cell fractions of each cell type represented as proportions between 0 and 1. The first column is the row names. 
- For further details on running `get_cellfracs_seuratv3.R`, see section "__Preprocessing__" below.

### Preprocessing
To account for the disparity between scRNA-seq and ST data in the number of cells per cell type, the fractional composition of each cell type per spot needs to be provided as input to CytoSPACE. This is determined using an external deconvolution tool, such as Spatial Seurat, CIBERSORTx, or SPOTlight. In the manuscript, we used Spatial Seurat, and provide here a script to obtain the cell type fractions using this approach.

__Importantly__, we use `Seurat v3` for this purpose. 

Run the script `get_cellfracs_seuratv3.R` from command line with the following inputs:
1. Path to scRNA counts file (same scRNA-seq gene expression matrix input file format as specified in __File format__ section point 1)
2. Path to cell type labels file (same cell type label input file format as specified above in __File format__ section point  2)
3. Path to ST data (same ST gene expression matrix input file format as specified above in __File format__ section point  3)
4. Name of output file

For example:
```bash
Rscript /path/to/get_cellfracs_seuratv3.R melanoma_scRNA_GEP.txt melanoma_scRNA_celllabels.txt melanoma_STdata_slide1_GEP.txt melanoma_cell_fraction_estimates.txt
```

### Running CytoSPACE
CytoSPACE can be called from the command line from any folder using `cytospace`. 
A typical CytoSPACE run with default settings would look like this: 
 ```bash
 cytospace --scRNA-path /path/to/scRNA_geneexpression
    --cell-type-path /path/to/scRNA_celllabels
    --st-path /path/to/ST_geneexpression
    --coordinates-path /path/to/ST_coordinates
    --cell-type-fraction-estimation-path path/to/cellfracestimates
```

For example, running CytoSPACE on a melanoma specimen profiled by the legacy ST platform (Thrane et al):
 ```bash
cytospace -sp melanoma_scRNA_GEP.txt -ctp melanoma_scRNA_celllabels.txt -stp melanoma_STdata_slide1_GEP.txt -cp melanoma_STdata_slide1_coordinates.txt -ctfep melanoma_cell_fraction_estimates.txt
```


 To see a list of variables and default values for running CytoSPACE, you can call `cytospace` from the command line along with the `-h` or 
`--help` flag, i.e., `cytospace -h`.

 ### Other ways CytoSPACE can be run:
 (1) You can call the `cytospace.py` script directly with python:
 `python cytospace/cytospace.py`
 
 (2) You can import methods or functions from `CytoSPACE` in python and modify/create your own 
    pipeline. For example:
```python
from cytospace import cytospace

for mean_cell_numbers in [5, 10, 20]:
    cytospace(..., mean_cell_numbers=mean_cell_numbers)
```

### Authors
CytoSPACE was developed by

* Milad R. Vahid (miladrv)
* Erin L. Brown (erinlbrown)
* Chloé B. Steen (cbsteen)
* Aaron M. Newman (aaronmnewman)

### Licence
CytoSPACE is licensed under the GNU GPL, version 3 or (at your option) any
later version.
CytoSPACE is Copyright (2022-) by the authors.

### Reference
If you are using the library for scientific work please reference it by:

    TODO
