# turn this into a function.
# do same for leavers. 

# merge into one file. 
columns = [
    "First Name",
    "Last Name",
    "Location Ledger Code",
    "Job",
    "Number",
    "Normal Weekly Hours",
    "Contract Type",
    "Date Joined",
    "Gender",
]

col = col[columns].copy()

col = pd.merge(col, dt, left_on="Date Joined", right_on="Date", how="left")

col.rename(columns={"Location Ledger Code": "Store"}, inplace=True)

st = pd.read_sql(
    "SELECT Shop AS Store, Area, Location, Division from StructureTab", engine
)
col = pd.merge(col, st, on="Store", how="left")

col["Name"] = col["First Name"] + " " + col["Last Name"]

col = col.iloc[:, 2:]
