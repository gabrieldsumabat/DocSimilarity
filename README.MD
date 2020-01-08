# Document Similarity Pipeline
## Gabriel Sumabat 

### Assumptions:
-User has permission to access and create files in the target directory

-Input Document File may be too large to store in memory and must be read line by line

-Capitalization of the letters is not important

-Numbers are allowed terms

### Requirements:
    Luigi

### To Run:
    Call run.sh
    Run wrapper class TfIdfPipeline.py or any of the individual python scripts
    luigi --module code.TfIdfPipeline rubrikloud.TfIdfPipeline --local-scheduler --input-path ./tmp/documents.txt

### Pipeline:

1. Clean Text 

    a. Read TXT File line by line
    
    b. Remove all non alpha numeric characters
    
    c. All alpha characters are set to lowercase to match words accurately
  
2. Compute Term Frequency (TF)

    a. Read in One Document at a Time
    
    b. Build Dict of Terms to Occurrence
    
    c. Divide each term occurrence by the total number of terms to find TF
    
3. Compute Inverse Document Frequency (IDF)

    a. Read TF Document Line by Line
    
    b. Read in Occurrence of Term for Each Document into a Dict
    
    c. Divide the Number of Documents by each Dict Occurrence to find IDF Value
    
4. Calculate Term Frequency Inverse Document Frequency Product

    a. Rebuild Term Frequency Document Dict
    
    b. Rebuild Inverse Document Frequency Dict
   
   c. Multiply each Document's TF Values with the corresponding IDF Value
   
5. Compute Similarity

    a. Read TF-IDF for each Document
    
    b. Create the Vector for each Document
    
    c. Calculate the euclidean distance between all vectors to calculate the similarity
    
    d. Write findings to csv file ordering by most similar
    
### Future Improvements
A. Add Integration Tests for all Luigi Jobs, currently only functions are tested.

B. Add negative, performance and incorrect test cases with proper test data.

C. Move all logic to functions for ease of unit testing