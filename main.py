import pandas as pd     
from bs4 import BeautifulSoup         
import requests                                
import os
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('punkt')                                      
nltk.download('stopwords') 
nltk.download('punkt_tab')
stop_words = set(stopwords.words('english'))  
import re      
import time    

#function to scrap only the title and contents text from the URL. Returns a string, containing the heading followed by the main content, without the tags and classes
def fetch_content(url,tries=10,delay=10):
    for attempts in range(tries):
        try:
            page=requests.get(url)
            page.raise_for_status
            soup=BeautifulSoup(page.content,'html.parser')
            heading=soup.find('h1', class_='entry-title')
            body=soup.find('div', class_='td-post-content tagdiv-type')
            return heading.text+body.text.replace('\n',' ')
        except requests.exceptions.RequestException as e:
            print("Failed to fetch"+url+":"+e)
            time.sleep(delay)
    return None

#fucntion to extract all the stopwords from its corresponding folders, and accordingly forming a sentiment dictionary. Using this sentiment dictionary, we calculate the derived variables
def sentiment_analyse(content):
    stopwords=load_words_from_folder('StopWords/')
    positive_words=load_words_from_file('MasterDictionary/positive-words.txt')
    negative_words=load_words_from_file('MasterDictionary/negative-words.txt')
    sentiment_dict={words:'positive' for words in positive_words if words not in stopwords}
    for i in negative_words:
        if i not in stopwords:
            if i not in sentiment_dict:
                sentiment_dict[i]='negative'
    dummy_str=content.split()
    new_str=[word for word in dummy_str if word.lower() not in stopwords]
    new_str=" ".join(new_str)
    return derived_variables(new_str,sentiment_dict)

#function to calculate the analysis of readability using the gunning fox index method. Returns a array containing the average sentence length, percentage of complex words, and the fog_index.
def gunning_fox_index(content): 
    words=word_tokenize(content)
    words=[word for word in words if word not in string.punctuation]
    sentences=sent_tokenize(content)
    l_words=len(words)
    l_sentences=len(sentences)
    complex_words=complex_count(words)
    average_sentence_length=l_words/l_sentences
    p_complex_words=complex_words/l_words
    fog_index=0.4*(average_sentence_length+p_complex_words) 
    return [average_sentence_length,p_complex_words*100,fog_index]

#function to find the number of clean words, defined as per the question. Returns the count
def clean_word_count(words):
    nltk.word_tokenize(words)
    clean_words=[word for word in words if word not in stop_words or word not in string.punctuation]
    return len(clean_words)

#function to convert a string of words to a list of words to find its number of complex words. Returns the count
def complex_count_c(content):
    words=word_tokenize(content)
    words=[word for word in words if word not in string.punctuation]
    return complex_count(words)

#function to calculate the number of complex words in a list of words. Returns the count of the number of the words
def complex_count(words):
    count=0
    for word in words:
        if syllable_count(word)>2:
            count+=1
    return count

# function to calculate the number of syllables in a word. Returns a integer
def syllable_count(word):
    vowels = "aeiou"
    word = word.lower()
    output = 0
    if word[0] in vowels:
        output += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index-1] not in vowels:                   #ensures no consecutive syllables are counted
            output += 1
    if word.endswith("es") or word.endswith("ed"):
        output -= 1
    return max(output, 1)

#function to derive the positive score, negative score, polarity and the subjectivity. Input is the main string and the sentiment dictionary, output is the array of output variables derived using the respective formulas
def derived_variables(content,sentiment_dict):
    tokens = word_tokenize(content.lower())
    p_score,n_score=0,0
    for i in tokens:
        if i not in sentiment_dict:
            continue
        elif sentiment_dict[i]=="positive":
            p_score+=1
        elif sentiment_dict[i]=="negative":
            n_score+=1
    polarity_score=(p_score-n_score)/((p_score+n_score)+0.000001)
    subjectivity_score=(p_score+n_score)/(len(tokens)+0.000001)
    return [p_score,n_score,polarity_score, subjectivity_score]
    
#function to write a array of data, namely the contents of each url and its analysis to a excel file situated at a destination
def write_to_excel(data,destination):
    output=pd.DataFrame(data)
    output.to_excel(destination, index=False)

#function to load words from a file directly
def load_words_from_file(filename):
    with open(filename, 'r',encoding='latin-1') as file:
        words = file.read().splitlines()
    return set(word for word in words)

#function to load words from a folder. This function only extracts data from the files ending with .txt
def load_words_from_folder(path):
    stopwords_set=set()
    for files in os.listdir(path):
        if files.endswith(".txt"):
            stopwords_set.update(load_words_from_file(path+files))
            # with open(path+files, 'r') as file:
            #     words=file.read().splitlines()
            #     stopwords_set.update(word.lower() for word in words)
    return stopwords_set
        
#function to find the average number of words per sentence, calculated as described in the question
def average_words_per_sentence(content):
    words=word_tokenize(content)
    words=[word for word in words if word not in string.punctuation]
    sentences=sent_tokenize(content)
    total_words=len(words)
    total_sentences=len(sentences)
    average_wps=total_words/total_sentences 
    return average_wps

#function to count the number fo syllables per word
def scpw(content):
    words=word_tokenize(content)
    words=[word for word in words if word not in string.punctuation]
    total_words=len(words)
    s_count=0
    for i in words:
        s_count+=syllable_count(i)
    return s_count/total_words

#function to calculate the number of personal pronouns in the passed content
def cal_personal_pron(content):
    pattern = r'\b(I|we|my|ours|us)\b'
    personal_pron = re.findall(pattern, content)
    personal_pron=[word for word in personal_pron if word.lower()!="us" or word.islower()]
    return len(personal_pron)

#function to calculate the average word length of the passed content
def awl(content):
    words=word_tokenize(content)
    words=[word for word in words if word not in string.punctuation]
    word_count=len(words)
    letter_count=0
    for word in words:
        letter_count+=len(word)
    return letter_count/word_count 

#the main function, which actually processes each of the said variables, and is the main entry function to start the code
def processUrls(input, output):
    df=pd.DataFrame(columns=['URL_ID', 'URL', 'POSITIVE SCORE',	'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS',	'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'])
    rows_of_data=[]
    ds=pd.read_excel(input)
    path='output/'
    if not os.path.exists(path):
        os.mkdirs(path)
    # text_files_array=[]
    j=0
    for i,rows in ds.iterrows():
        row=[]
        url_id=rows['URL_ID']
        filename=url_id+'.txt'
        url=rows['URL']
        # path='output/'
        original=[url_id,filename]
        content=fetch_content(url)
        with open(path+filename, 'w', encoding='utf-8') as file:
            file.write(content)
        s_analysis=sentiment_analyse(content)
        analysis_readability=gunning_fox_index(content)
        avg_wps=[average_words_per_sentence(content)]
        complex_word_count=[complex_count_c(content)]
        clean_words=[clean_word_count(content)]
        syllable_count_per_word=[scpw(content)]
        personal_pronouns=[cal_personal_pron(content)]
        avg_word_length=[awl(content)]
        row=original+s_analysis+analysis_readability+avg_wps+complex_word_count+clean_words+syllable_count_per_word+personal_pronouns+avg_word_length
        # print(row)
        rows_of_data.append(row)
    i=0
    for row in rows_of_data:
        df.loc[i]=row
        i+=1
    write_to_excel(df, output)

input='Input.xlsx'
destination='Output Data Structure.xlsx'
processUrls(input,destination)