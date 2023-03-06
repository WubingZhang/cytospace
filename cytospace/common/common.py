import numpy as np
import pandas as pd
from pathlib import Path
import warnings
import datatable as dt
from numpy.linalg import norm
import tarfile
import os
import scanpy as sc

def read_file(file_path):
    # Read file
    try:
        file_delim = "," if file_path.endswith(".csv") else "\t"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=pd.errors.ParserWarning)
            #file_data = pd.read_csv(file_path, header=0, index_col=0, delimiter=file_delim)
            file_data = dt.fread(file_path)
            rownames = file_data[:,0].to_pandas().values.flatten()
            file_data = file_data[:,1:file_data.ncols].to_pandas()
            file_data = file_data.set_index(rownames)
   
    except Exception as e:
        raise IOError("Make sure you provided the correct path to input files. "
                      "The following input file formats are supported: .csv with comma ',' as "
                      "delimiter, .txt or .tsv with tab '\\t' as delimiter.")

    return file_data


def read_visium(file_name,output_folder):
    out_dir = str(output_folder)
    sr_dir = out_dir+'/SpaceRanger'
    
    print(out_dir)
    print(sr_dir)
    print(file_name)

    file = tarfile.open(file_name,'r')
    file.extractall(sr_dir)
    file.close()

    count_dir = os.listdir(sr_dir)
    count_dir = [d for d in count_dir if os.path.isdir(os.path.join(sr_dir, d))][0]
    count_dir = sr_dir+'/'+count_dir

    fin_count = os.listdir(count_dir)
    fin_count = [fin for fin in fin_count if fin.endswith('.h5')]
    fin_count = [fin for fin in fin_count if not fin.startswith('.')][0]

    visium_adata = sc.read_visium(count_dir,count_file=fin_count)

    genes = visium_adata.var_names
    spots = visium_adata.obs_names
    df_expression = pd.DataFrame.sparse.from_spmatrix(visium_adata.X,index=spots,columns=genes).transpose()

    df_expression = df_expression.loc[(df_expression!=0).any(1), (df_expression!=0).any(0)]

    df_coords = pd.DataFrame(visium_adata.obsm['spatial'],index=spots,columns=['X','Y'])
    df_coords = df_coords.loc[df_expression.columns,:]

    return df_expression, df_coords

def estimate_cell_type_fractions(scRNA_path, cell_type_path, st_path, output_folder):
    run_str = "Rscript get_cellfracs_seuratv3.R --scrna-path "+scRNA_path+" --ct-path "+cell_type_path+" --st-path "+st_path+" --outdir "+output_folder
    out = os.system(run_str)
    frac_file = output_folder+'/Seurat_weights.txt'
    return out, frac_file

def normalize_data(data):
    data = np.nan_to_num(data).astype(float)
    data *= 10**6 / np.sum(data, axis=0, dtype=float)
    np.log2(data + 1, out=data)
    np.nan_to_num(data, copy=False)
    return data


def check_paths(output_folder, output_prefix):
    # Create relative path
    output_path = Path().cwd() / output_folder

    # Make sure that the folder exists
    output_path.mkdir(parents=True, exist_ok=True)

    if Path(output_path / f"{output_prefix}assigned_locations.csv").exists():
        print("\033[91mWARNING\033[0m: Running this will overwrite previous results, choose a new"
              " 'output_folder' or 'output_prefix'")

    return output_path


def matrix_correlation_pearson(v1, v2):
    if v1.shape[0] != v2.shape[0]:
        raise ValueError("The two matrices v1 and v2 must have equal dimensions; ST and scRNA data must have the same genes")

    n = v1.shape[0]
    sums = np.multiply.outer(v2.sum(0), v1.sum(0))
    stds = np.multiply.outer(v2.std(0), v1.std(0))
    correlation = (v2.T.dot(v1) - sums / n) / stds / n

    return correlation


def matrix_correlation_spearman(v1, v2):
    
    if v1.shape[0] != v2.shape[0]:
        raise ValueError("The two matrices v1 and v2 must have equal dimensions; ST and scRNA data must have the same genes")
        
    v1 = pd.DataFrame(v1).rank().values
    v2 = pd.DataFrame(v2).rank().values
    
    n = v1.shape[0] # v1 and v2 should have the same number of rows
    sums = np.multiply.outer(v2.sum(0), v1.sum(0))
    stds = np.multiply.outer(v2.std(0), v1.std(0))
    correlation = (v2.T.dot(v1) - sums / n) / stds / n
    
    return correlation
