# %%
import numpy as np
import pandas as pd
import re # regular expression is used to find a specific text or letter/ word in a sentence or paragraph
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords # these are basically the words which don't convey much meaning like a the an etc.
from nltk.stem.porter import PorterStemmer # this is used to stem the word like for eg if we have loved --> love!
from sklearn.feature_extraction.text import CountVectorizer #to vectorize the words into a vector of frequent words count!
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from nltk.stem import SnowballStemmer
# %%
#print(stopwords.words('spanish'))

# %%
fake_news_dataset = pd.read_csv('data/complete_dataset.csv')
real_news_dataset = pd.read_csv('data/real_complete_dataset.csv',index_col=['Unnamed: 0'])
# %%
del(fake_news_dataset['link'])
news_dataset = pd.concat([fake_news_dataset,real_news_dataset])
# %%
stem = SnowballStemmer('spanish')# basically creating an object for stemming! Stemming is basically getting the root word, for eg: loved --> love! 
# %%
# now let's create a function to preprocess a cell and then apply it to the entire feature!
def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]', ' ',content) # this basically replaces everything other than lower a-z & upper A-Z with a ' ', for eg apple,bananna --> apple bananna
    stemmed_content = stemmed_content.lower() # to make all text lower case
    stemmed_content = stemmed_content.split() # this basically splits the line into words with delimiter as ' '
    stemmed_content = [stem.stem(word) for word in stemmed_content if not word in stopwords.words('spanish')] # basically remove all the stopwords and apply stemming to the final data
    stemmed_content = ' '.join(stemmed_content) # this basically joins back and returns the cleaned sentence
    return stemmed_content
# %%
# let's apply the function on our feature content
news_dataset['descripcion_stem'] = news_dataset['descripcion'].apply(stemming)
# %%
from sklearn.model_selection import train_test_split

training_data, testing_data = train_test_split(news_dataset, test_size=0.2, random_state=0)

# %%
X = training_data['descripcion_stem'].values
y = training_data['is_fake'].values
# %%
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X)
# %%
#classifier = LogisticRegression(C = 100, penalty = 'l2', solver= 'newton-cg')
classifier = LogisticRegression(C = 0.1, penalty = 'l2', solver= 'liblinear')
modelo = classifier.fit(X, y)
# %%
# accuracy score on training data
y_pred_train = modelo.predict(X)
accuracy_train = accuracy_score(y,y_pred_train)
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = modelo,X = X,y= y , cv = 10)


print("-------------------------------")
print("Accuracy score on training data: ", accuracy_train)
print("Accuracy: {:.2f} %".format(accuracies.mean()*100))
print("Standard Deviation: {:.2f}".format(accuracies.std()*100))
# %%
# grid search to find better hyper parameters
#from sklearn.model_selection import GridSearchCV
#parameters = [{'solver': ['newton-cg','liblinear'], 'penalty': ['l2'],'C': [100, 10, 1.0, 0.1, 0.01]}]
#grid_search = GridSearchCV(estimator=modelo,
#                          param_grid=parameters,
#                          scoring='accuracy',
#                          cv=10)
#grid_search.fit(X,y)
#print("Best Accuracy: {:.2f} %".format(grid_search.best_score_*100))
#print("Best Parameters: ", grid_search.best_params_)
# %%
# seperating the data and vectorizing to predict the labels from the model we made!
X_test = testing_data['descripcion_stem']
X_test = vectorizer.transform(X_test)
# %%
# now to predict the labels from the model!
y_pred_final = modelo.predict(X_test)
print(y_pred_final)
# %%
y_pred_final.shape
# %%
testing_data['is_fake'].shape
# %%
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# actual values
actual = testing_data['is_fake']
# predicted values
predicted = y_pred_final

# confusion matrix
matrix = confusion_matrix(actual,predicted, labels=[1,0])
print('Matriz de Confusion : \n',matrix)

# outcome values order in sklearn
tp, fn, fp, tn = confusion_matrix(actual,predicted,labels=[1,0]).reshape(-1)
print('Outcome values : \n', tp, fn, fp, tn)

# classification report for precision, recall f1-score and accuracy
matrix = classification_report(actual,predicted,labels=[1,0])
print('Reporte de Clasificacion : \n',matrix)
#%%
# Guardando el modelo generado
from joblib import dump, load 
# Save the model as a pickle in a file
dump(modelo, './data/clasificador_reportes.pkl')
 
# Load the model from the file
#knn_from_joblib = joblib.load('filename.pkl')
# Use the loaded model to make predictions
#knn_from_joblib.predict(X_test)
# %%
