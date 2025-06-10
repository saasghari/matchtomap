#####  load data (local)
from mappymatch import package_root
import pandas as pd

def loadData(data_file):
    df = pd.read_csv(data_file)
    print(df.head())

    from mappymatch.constructs.trace import Trace
    trace = Trace.from_csv(
                            data_file,
                            lat_column="latitude",
                            lon_column="longitude",
                            xy=True,
                            )
    