import pandas as pd
import numpy as np
import os.path

def ismember(A, B):
    return [ np.sum(a == B) for a in A ]

def ismember2(A, B):
    
    A = np.array(A, dtype=object)
    B = np.array(B, dtype=object)
    
    Indices = np.arange(0, B.size)
    revIndices = np.arange(0, A.size)
    
    Locs = np.empty_like(A)
    revLocs = np.empty_like(B)
    
    Exists = np.empty_like(A)
    
    i = 0
    j = 0
    
    for a in A:
        Filter = (a == B)
        Exists[i] = np.sum(Filter)        
        Locs[i] = Indices[Filter]                
        i += 1
    
    for b in B:
        revFilter = (b == A)
        revLocs[j] = revIndices[revFilter]
        j += 1            
                                                            
    return(Exists, Locs, revLocs)
        
def ImportData():
    
  # Get path of present working directory
  CodeDir = os.path.dirname(os.path.realpath(__file__))
  DataDir = 'F:\LAS_files'
      
  #Get path to data file
  #DataFilePath = '8944.LAS'
  DataFilePath = raw_input('Enter .LAS file to be processed: ')
  
  # User specifies source of LAS file (ie. Eaton, West Coast, Newman or Pacific Surveys)
  DictIndex = raw_input('LAS file source? (0 = Eaton, 1 = West Coast, 2 = Newman, 3 = Pacific, 4 = Pacific [Merged CSV]): ')
  DictIndex = int(DictIndex)
  
  # Define dictionary for source-specific import parameters (i.e. relevant header names and header line no.) 
  ColumnHeadersDict = {'Depth':['Depth', 'Depth', 'Depth', 'Depth', 'Depth'],  # Depth values header
                       'RSN':['16', '16\"', 'RSN', 'RSN', 'RSN'],    # Short normal resistivity trace header
                       'RLN':['64', '64\"', 'RLN', 'RLN', 'RLN'],    # Long normal resistivity trace header
                       'SP':['SP', 'SP', 'SP', 'SP', 'SP'],         # Spontaneous Potential resistivity trace header 
                       'PR':['DET', 'SPT','SPR','SPR', 'SPR'],          # Single-point resistance trace header (Water conductance for Pacific Surveys)
                       'hline':[32, 96, 25, 67, 0]               # Line containing header info (counting from 0)
  #                     'hline':[32, 96, 25, 64, 0] 
                     }
                     
  HeaderLine = ColumnHeadersDict['hline'][DictIndex]
  LinesToSkip = HeaderLine+1

  # Change directory to folder containing LAS files
  os.chdir(DataDir)  

  #Get Column names
  if (DictIndex == 4):
    ColumnNamesTable = pd.read_csv(DataFilePath, sep=',', header = HeaderLine, nrows = 1)
  else:
    ColumnNamesTable = pd.read_csv(DataFilePath, sep='\s+', header = HeaderLine, nrows = 1)
    
    
  #Eliminate bad ~A character from list
  if (DictIndex == 4):
    ColumnsToKeep = ColumnNamesTable.columns.values
  else:
    ColumnsToKeep = ColumnNamesTable.columns.values
    ColumnsToKeep = ColumnsToKeep[1:]
  
  # Select relevant columns and use universal header names in dataframe to be formed
  NamesToMatch = np.array([ColumnHeadersDict['Depth'][DictIndex],
                ColumnHeadersDict['RSN'][DictIndex],
                ColumnHeadersDict['RLN'][DictIndex],
                ColumnHeadersDict['SP'][DictIndex],
                ColumnHeadersDict['PR'][DictIndex]])
                
  ColumnNames = np.array(['Depth', 'RSN', 'RLN', 'SP', 'PR'])
  

  #IndexFilter = ismember(ColumnsToKeep, NamesToMatch) 
  IndexFilter, Locs, revLocs = ismember2(ColumnsToKeep, NamesToMatch)
  ColumnIndices = np.empty_like(np.arange(0,ColumnNames.size))
  NamesMap = np.empty_like(np.arange(0,ColumnNames.size))
  
  j = 0
  for l in revLocs:
      if (l.size != 0):
            ColumnIndices[j] = l[0]
            j += 1
  
  i = 0
  for l in Locs:
      if (l.size != 0):
          NamesMap[i] = l[0]
          i += 1
            
  # Rearrange Lables
      
  #IndexFilter = np.array(IndexFilter)
  #IndexFilter = (IndexFilter == 1)
  
  # Read text file to a Table (DataFrame)
  #NamesMap = np.unique(NamesMap)
  #ColumnIndices = np.unique(ColumnIndices)
  
  if (DictIndex == 4):
    LogDataTable = pd.read_csv(DataFilePath, sep=',', skiprows=LinesToSkip, 
      names = ColumnNames[NamesMap], usecols = ColumnIndices)
  else:
    LogDataTable = pd.read_csv(DataFilePath, sep='\s+', skiprows=LinesToSkip, 
      names = ColumnNames[NamesMap], usecols = ColumnIndices)
  
  # Return to code directory
  os.chdir(CodeDir)
      
  return(LogDataTable)