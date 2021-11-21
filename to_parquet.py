from utils import load_print_data
import pandas as pd

# tar -xvzf yelp_dataset.tar -C "G:/My Drive/data_science/projects/customer-seg"

# instruction: activate env to export
# conda env export > environment.yml
# conda env create -f environment.yml


path, filename = 'source/', '6M-0K-99K.users.dataset.public' 
df = load_print_data(path, filename, filetype="csv")
me2n.to_parquet("source/SAP_ME2N_pq.parquet")