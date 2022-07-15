# Panda import
import pandas as pd

  
# URL of the web page whose table we want to extract
url = "http://127.0.0.1:5000/class_result/class_9"
  
# Assign table data to Pandas dataframe
table = pd.read_html (url) [ 0 ]
  
# Print data frame
print (table)

# ---------------------------------------------------------------------
# Pandas import
import pandas as pd

 
# URL of the web page whose table we want m extract
url = "http://127.0.0.1:5000/class_result/class_9"

  
# Assign table data to a Pandas dataframe
table = pd.read_html (url) [ 0 ]

 
# Save data frame to Excel file
table .to_excel ( "data.xlsx" )
