from data_import import BMImport
from data_percentage import DataPercentage

bm_import = BMImport()
data_percentage = DataPercentage(bm_import.bm_gating_df)
