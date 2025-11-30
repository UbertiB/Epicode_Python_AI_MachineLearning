import pandas as pd
import numpy as np

date_rng=pd.date_range(start="2025-01-01",end="2025-03-31",free="D")
df=pd.DataFrame({"Data":date_rng, "Valore":np.random.randint(10,100,len(date_rng))})