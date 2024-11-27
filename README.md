 # Automated Sentiment and Readability Analysis

#### **Description**  
This Python project fetches web content from a list of URLs, analyzes the sentiment and readability of the content, and saves the results in a structured Excel file. It provides insights into the tone and complexity of text, making it suitable for content analysis and reporting.

#### **Features**  
- Fetches and processes web content using `requests` and `BeautifulSoup`.  
- Performs sentiment analysis, calculating polarity and subjectivity.  
- Computes readability metrics, including Gunning Fog Index and average word/sentence lengths.  
- Outputs results in both `.txt` and `.xlsx` formats.  

#### **Usage**  
1. **Setup:**  
   Ensure you have Python installed and the necessary libraries:  
   ```bash  
   pip install pandas beautifulsoup4 nltk  
   ```  

2. **Prepare Input Files:**  
   - Place `Input.xlsx` (with `URL_ID` and `URL` columns) in the working directory.  
   - Include stopword files and sentiment dictionaries in their respective folders (`StopWords/` and `MasterDictionary/`).  

3. **Run the Script:**  
   Execute the script using:  
   ```bash  
   python main.py  
   ```  

4. **Check Output:**  
   - Text files will be saved in the `output/` folder.  
   - The analysis results will be saved in `Output Data Structure.xlsx`.  

#### **Folder Structure**  
```
Project/
├── Input.xlsx
├── main.py
├── StopWords/
│   ├── StopWords_Generic.txt
│   ├── StopWords_Names.txt
├── MasterDictionary/
│   ├── positive-words.txt
│   ├── negative-words.txt
├── output/
└── Output Data Structure.xlsx
```

#### **Contributing**  
Feel free to submit issues or pull requests to improve this project.
