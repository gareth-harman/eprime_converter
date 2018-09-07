# eprime_converter

Converts all .edat files into .txt or csv files

 ARGUMENTS:

  -eprime => Path to Eprime executible
  -data   => Path to all .edat files
  -out    => Output path for .txt/.csv files if not specified dame as -data
  -format => Defaults to .txt but but will take "csv" as well
  
    ex.\npython auto_EPRIME.py -u "C:/Users/Program Files(x86)/Eprime... -data "C:/Users/documents/my_data/
    
 NOTES: 
 
    * Paths must include quotes
    * Options for format = txt or csv
    * If using \ as filesep make sure last filesep is \\
    * Watch spaces in file paths
