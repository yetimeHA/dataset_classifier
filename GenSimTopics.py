import pandas
import pyarrow.parquet as pq
import re

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

if __name__ == '__main__':
    #cbanking = pq.ParquetDataset('/Users/yetime/Parquet/commercial_banking_demo/').read().to_pandas()
    dunnhumby = pq.ParquetDataset('/Users/yetime/Parquet/dunnhumby_completejourney_sample').read().to_pandas()
    #demo_fmcg = pq.ParquetDataset('/Users/yetime/Parquet/demo_fmcg_sample_sales').read().read().to_pandas()
    #demo_hr = pq.ParquetDataset('/Users/yetime/Parquet/demo_bank_hr').read().read().to_pandas()

    #cbanking_obj = cbanking.select_dtypes(include='object')
    dunnhumby_obj = dunnhumby.select_dtypes(include='object', exclude=['datetime', 'datetime64']).head(100)

    x=dunnhumby_obj.values.tolist()
    #dunnhumby_rows = x.astype(str).values.flatten().tolist()

    print(x)