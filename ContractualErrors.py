#!/usr/bin/env python
# coding: utf-8


import sys
import os

sys.path.append(
    os.path.abspath(r"S:\Data\Stores Payroll\FY20\FY20 Code Base\Master Scripts")
)
from connector import *

pd.options.display.float_format = "{:,.2f}".format
import datetime


## Add in a modified version of newest, which takes in two arguments,
## one is the time the second is a pattern match to get a specific file
## from a data dump.


def newest(path, pattern):
    files = glob.glob(f"*{pattern}*.*xlsx")
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)


## Read in Store Structure for merges

st = pd.read_sql("SELECT * from structureTab", engine)


# # Step 1 - Manual Data Wrangling from Raw Reports & YTD Table.


os.chdir(r"S:\Data\Stores Payroll\FY20\Weekly Tasks\Contract Errors - REVIVED\rawData")
path = os.getcwd()


params = urllib.parse.quote(
    "DRIVER={SQL Server Native Client 11.0};SERVER="
    + server
    + ";DATABASE="
    + database
    + ";UID="
    + username
    + ";PWD="
    + password
)

engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)


# # Bank Details - YTD Table


bank = pd.read_excel(newest(path, "Bank"), skiprows=1, date_parser="Effective Start")

## Select Relevant Columns

bank = bank[["First Name", "Number", "Last Name", "Location", "Seniority Date"]].copy()


## Set Error Type for Week Table

bank["Missing Bank Details"] = "True"

## Get Store Number


bank = bank.loc[bank['Location'].dropna()]

bank["Store"] = bank["Location"].str.extract("(\d+)").astype(int)

## Set Error Type for YTD Table


bank["ErrorType"] = "Missing Bank Details"

## Sort Columns for Table.

bank = bank[
    [
        "First Name",
        "Last Name",
        "Number",
        "Store",
        "Seniority Date",
        "Missing Bank Details",
        "ErrorType",
    ]
].copy()


## Rename to make merges easier.


bank.rename(
    columns={"Seniority Date": "Effective Start", "Number": "Employee Number"},
    inplace=True,
)

## Copy for the SQL DataFrame Table.

b1 = bank[
    [
        "First Name",
        "Last Name",
        "Employee Number",
        "Store",
        "Effective Start",
        "ErrorType",
    ]
].copy()


# ## Contracts


# # Contract Errors YTD Table


# Read in Latest File

cont = pd.read_excel(
    newest(path, "Contract"), skiprows=1, date_parser="Effective Start"
)


# Set Error for Week Table

cont["Missing Work Contract"] = "True"

# Extract Store Number.

cont["Store"] = cont["Org Unit"].str.extract("(\d+)").fillna(0).astype(int)

## Set error for YTD Table

cont["ErrorType"] = "Contract Error"

# Make a copy of DataFrame for YTD and Week Tables.

cont = cont[
    [
        "First Name",
        "Last Name",
        "Employee Number",
        "Store",
        "Effective Start",
        "Missing Work Contract",
        "ErrorType",
    ]
].copy()

c1 = cont[
    [
        "First Name",
        "Last Name",
        "Employee Number",
        "Store",
        "Effective Start",
        "ErrorType",
    ]
].copy()


# # Hours Check YTD Table


hours = pd.read_excel(newest(path, "Hours"), skiprows=1, date_parser="Effective Start")

## Set Error to True for Weekly Table (Store Level)

hours.loc[hours["Work Pattern Start Day"] != "Saturday", "Saturday"] = "True"

## Set Error to True for Weekly Table (Store Level)

hours.loc[
    hours["Work Contract Hours"] != (hours["Normal Weekly Hours"] * 2),
    "Work Contract Hours not Bi-Weekly",
] = "True"

## Set Error to True for Weekly Table (Store Level)

hours.loc[
    hours["Work Contract Hours"] != hours["Work Pattern Hours"],
    "No Matching Work Pattern",
] = "True"

## Set Error to True for Weekly Table (Store Level)

hours.loc[hours["Work Contract"] == "Weekly", "No Matching Work Pattern"] = "True"

## Extract Store Number

hours["Store"] = hours["Location"].str.extract("(\d+)").fillna(0).astype(int)


## Error for YTD Table.

hours["ErrorType"] = "Missing Work Pattern"


## Copy Table

hours = hours[
    [
        "First Name",
        "Last Name",
        "Employee Number",
        "Store",
        "Effective Start",
        "Saturday",
        "Work Contract Hours not Bi-Weekly",
        "No Matching Work Pattern",
        "ErrorType",
    ]
].copy()


h1 = hours[
    [
        "First Name",
        "Last Name",
        "Employee Number",
        "Store",
        "Effective Start",
        "ErrorType",
    ]
]


SQLdf = pd.concat([h1, c1, b1], ignore_index=True)

st.Store = st.Store.astype(int)

SQLdf = pd.merge(st, SQLdf, on="Store", how="right")

SQLdf = SQLdf.fillna(0)

SQLdf["Week"] = int(tw) - 1
SQLdf = SQLdf[
    [
        "Area",
        "Store",
        "Employee Number",
        "First Name",
        "Last Name",
        "Effective Start",
        "Week",
        "ErrorType",
    ]
].copy()

ct = pd.read_sql("SELECT TOP 1 * from contracterrorsYTD", engine)
SQLdf.columns = ct.columns


day_today = datetime.date.today().strftime("%A")


datetime.date.today().strftime("%A")


max_week = int(pd.read_sql("SELECT max(Week) as W from contractErrorsYTD", engine)["W"])


data_types = {
    "First Name": sa.types.VARCHAR,
    "Last Name": sa.types.VARCHAR,
    "Effective Start": sa.types.VARCHAR,
    "Error Type": sa.types.VARCHAR,
}

while True:
    print(
        f"Do you use to append to the YTD table? the current week is {int(tw)-1} and the max week in SQL is {max_week}"
    )
    cmd = input("Enter [Y] or [N]")
    if cmd.lower().strip() == "y":
        SQLdf.to_sql(
            "contractErrorsYTD",
            engine,
            schema="dbo",
            if_exists="append",
            index=False,
            dtype=data_types,
        )
        print("YTD updated to SQL")
        break
    elif cmd.lower().strip() == "n":
        print("Not updating YTD updating weekly table")
        break
    else:
        print("Enter either yes/no")


# # WTD Table.


cont.loc[cont.Store == 733]


df = pd.DataFrame(
    pd.concat(
        [
            hours[["Employee Number", "Effective Start", "First Name", "Last Name"]],
            bank[["Employee Number", "Effective Start", "First Name", "Last Name"]],
            cont[["Employee Number", "Effective Start", "First Name", "Last Name"]],
        ],
        axis=0,
    )
).drop_duplicates()


df = pd.merge(
    df,
    hours[
        [
            "Employee Number",
            "Saturday",
            "Work Contract Hours not Bi-Weekly",
            "No Matching Work Pattern",
        ]
    ],
    on="Employee Number",
    how="left",
).copy()


df = pd.merge(df, cont[["Employee Number", "Missing Work Contract"]], how="left").copy()


df = pd.merge(df, bank[["Employee Number", "Missing Bank Details"]], how="left").copy()


df.iloc[:, -5:] = df.iloc[:, -5:].fillna(" ")


df["Effective Start"] = pd.to_datetime(
    df["Effective Start"], dayfirst=True, errors="coerce"
)


col_path = r"S:\Data\Stores Payroll\FY20\BAU FY20\All_Colleagues\raw_data"
os.chdir(col_path)

cols = pd.read_excel(newest(col_path, "All"), skiprows=1)


cols.rename(columns={"Location Ledger Code": "Shop"}, inplace=True)

df.rename(columns={"Shop Number": "Shop", "Employee Number": "Number"}, inplace=True)


df = pd.merge(df, cols[["Number", "Shop"]], on="Number", how="left")


df = pd.merge(df, st[["Shop", "Area"]], on="Shop", how="left")

df["Area"] = df["Area"].fillna(0)


df.rename(
    columns={
        "Missing Bank Details": "missingBank",
        "No Matching Work Pattern": "noMatching",
        "Missing Work Contract": "missingCont",
        "Work Contract Hours not Bi-Weekly": "biWeekly",
    },
    inplace=True,
)


df = df[
    [
        "Area",
        "Shop",
        "Number",
        "First Name",
        "Last Name",
        "Effective Start",
        "Saturday",
        "biWeekly",
        "noMatching",
        "missingCont",
        "missingBank",
    ]
].copy()


# remove cycle republic.

df = df.loc[(df.Area.isnull() == False)]

# Rename Columns

df.rename(columns={"Shop Number": "Shop"}, inplace=True)


# Select columns

df.columns = [
    "Area",
    "Shop",
    "Number",
    "First Name",
    "Last Name",
    "Effective Start",
    "Saturday",
    "biWeekly",
    "noMatching",
    "missingCont",
    "missingBank",
]


d = {
    "Area": sa.types.BIGINT,
    "Shop": sa.types.BIGINT,
    "Employee Number": sa.types.BIGINT,
    "First Name": sa.types.NVARCHAR(length=50),
    "Last Name": sa.types.NVARCHAR(length=50),
    "Effective Start": sa.types.NVARCHAR(length=50),
    "Saturday": sa.types.NVARCHAR(length=50),
    "biWeekly": sa.types.NVARCHAR(length=50),
    "noMatching": sa.types.NVARCHAR(length=50),
    "missingCont": sa.types.NVARCHAR(length=50),
    "missingBank": sa.types.NVARCHAR(length=50),
    "NumberOfWeeks": sa.types.BIGINT,
}

# replace spaces with NaN's (True NaN)

df = df.replace(" ", np.nan)


exclude_me = [8016106, 360279, 8014262, 8015521, 8013882]


df = df.loc[~df.Number.isin(exclude_me)]


df.loc[df["First Name"] == "Erin"]


df.to_sql(
    "contractErrorsWeek",
    engine,
    schema="dbo",
    index=False,
    if_exists="replace",
    dtype=d,
)
print("Weekly Table Added to SQL")


last_updated = datetime.date.today().strftime("%A %d %B")
lu = pd.DataFrame({"Today": last_updated}, index=[0])
tDtypes = {"Today": sa.types.VARCHAR(length=255)}
lu.to_sql(
    "CE_Update", engine, dtype=tDtypes, index=False, schema="dbo", if_exists="replace"
)


# In[ ]:


# In[ ]:
