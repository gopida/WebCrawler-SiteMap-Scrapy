import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


nltk.download('stopwords')
english_stopwords = stopwords.words('english')
ps = PorterStemmer()

print("stop words", english_stopwords)
""" cleaning up keywords """

df_keys = pd.read_csv('datafiles/us-unemployment.csv')
keywords_list = df_keys.iloc[:, 0].tolist()
keywords_str = " ".join(keywords_list)
keywords_str_fl = re.sub('[^a-zA-Z \.]', '', keywords_str)
keywords_set = set(keywords_str_fl.split())
keywords = keywords_set.difference(english_stopwords)
print("keywords ", keywords)

""" cleaning and processing news articles"""

df_news = pd.read_csv('datafiles/news.csv')
cleaned_df = pd.DataFrame()
for index, row in df_news.iterrows():
    content = row.content
    content_str = re.sub('[^a-zA-Z ]', '', content)
    content_str = re.sub('[\.]', ' ', content_str)
    content_list = content_str.split()
    content_set = set(content_list)
    if content_set.intersection(keywords):
        content_fl = [word for word in content_list if word.lower() not in english_stopwords]
        clean_content = " ".join(ps.stem(content_fl))
        row.content = clean_content
        cleaned_df = cleaned_df.append(row)

# writing the processed data out to file
cleaned_df.to_csv('datafiles/processed_news_stem.csv', index=False, columns=df_news.columns.values)


