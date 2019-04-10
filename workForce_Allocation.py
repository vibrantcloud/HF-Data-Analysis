## On the back of the Hal Labour model ## 

## Allocate budgets to FT / PT allowance per location ## 

import pandas as pd
import numpy as np
import random

## Create some dummy data ## 
"""
Some general rules:

no location can have less than 37.5 hours (UK FTE Equivilent).
A location can have an existing allocation in place for this specific problem which is between 0 - +/- 10% of their current budget.
The current budget plays no part in our calculation, it's used to soley drive the decision 
that we may or may not need to increase or decrease current headcount.

"""


df = pd.DataFrame({'Store' : random.sample(range(450),450),
             'Hours' : np.random.randint(37.5,120,size=450),
                   'Current Budget' : np.random.randint(0,37.5,size=450)
                   })
"""
print(df)

Current Budget	Hours	Store
0	28	102	232
1	19	73	218
2	23	39	362
3	27	43	22
4	32	77	334
"""

## Use a vectorised operation to work out FT // PT allocation using divmod operation ##

# Okay, this will give us our FT Allocation(s) 
ft, remainder = divmod(df['Hours'], 37.5)

# Further more, this will give the PT Allowance up to 25
pt_20, remainder = divmod(remainder, 25)

#Lets go two levels further down to 16 and 8, 
pt_16, remainder = divmod(remainder, 16)
pt_8, remainder = divmod(remainder, 8)


# Now lets apply this to our main DF #



df = df.assign(
    ft = ft,
    pt_25 = pt_25,
    pt_16 = pt_16,
    pt_8 = pt_8,
    remainder = remainder)


## Great, this gives us a headcount as per the budget, we can then apply the same formula on the current budget
## To work out any variances. 

"""

Current Budget	Hours	Store	ft	pt_25	pt_16	pt_8	remainder
0	27	63	243	1.0	1.0	0.0	0.0	0.5
1	11	64	108	1.0	1.0	0.0	0.0	1.5
2	35	86	152	2.0	0.0	0.0	1.0	3.0
3	2	71	350	1.0	1.0	0.0	1.0	0.5
4	14	42	169	1.0	0.0	0.0	0.0	4.5

"""

