import postgresql
from databaseConfig import dbConfig
from prettytable import PrettyTable

selectAttributes = ""
groupingVarCount = 
groupingAttributes = ""
fVect = ""
predicates = ""
havingCondition = ""
MF_Struct = {}
db = postgresql.open(user = dbConfig['user'],password = dbConfig['password'],host = dbConfig['host'],port = dbConfig['port'],database = dbConfig['database'],)

query = db.prepare('SELECT * FROM sales;')
