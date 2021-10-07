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
from joblib import dump, load

#%%
# IMPORTANDO Y TRATANDO LOS DATOS

fake_news_dataset = pd.read_csv('data/fake_news_elmercioco.csv',index_col=['Unnamed: 0'])
real_news_dataset = pd.read_csv('data/real_complete_dataset.csv',index_col=['Unnamed: 0'])
news_dataset = pd.concat([fake_news_dataset,real_news_dataset])
news_dataset = news_dataset.drop_duplicates(subset=["titulo"])

# %%

#  FUNCIÓN QUE PERMITE HACER STEMMING A CADA PALABRA

stem = SnowballStemmer('spanish')

def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]', ' ',content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split() 
    stemmed_content = [stem.stem(word) for word in stemmed_content if not word in stopwords.words('spanish')]
    stemmed_content = ' '.join(stemmed_content) 
    return stemmed_content
 
news_dataset['descripcion_stem'] = news_dataset['titulo'].apply(stemming)
# %%

# DIVISIÓN EN DATOS DE ENTRENAMIENTO Y DATOS DE PRUEBA

from sklearn.model_selection import train_test_split

training_data, testing_data = train_test_split(news_dataset, test_size=0.2, random_state=0)

X = training_data['descripcion_stem'].values
y = training_data['is_fake'].values

dump(X, '/home/cbpaguay/PycharmProjects/mineria_api_rest/api/data/x_t.joblib')
dump(y, '/home/cbpaguay/PycharmProjects/mineria_api_rest/api/data/y_t.joblib')
# %%

# ENTRENAMIENTO DEL MODELO

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X)
classifier = LogisticRegression(C = 1.0, penalty = 'l2', solver= 'liblinear')
modelo = classifier.fit(X, y)
dump(modelo, '/home/cbpaguay/PycharmProjects/mineria_api_rest/api/data/modelo.joblib')
# %%

# VERIFICANDO LA PRECISIÓN DEL MODELO PARA LOS DATOS DE ENTRENAMIENTO

y_pred_train = modelo.predict(X)
accuracy_train = accuracy_score(y,y_pred_train)
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = modelo,X = X,y= y , cv = 10)

print("-------------------------------")
print("Accuracy score on training data: ", accuracy_train)
print("Accuracy: {:.2f} %".format(accuracies.mean()*100))
print("Standard Deviation: {:.2f}".format(accuracies.std()*100))

# %%

# EVALUACIÓN DEL MODELO CON LOS DATOS DE PRUEBA

X_test = testing_data['descripcion_stem']
X_test = vectorizer.transform(X_test)

y_pred_final = modelo.predict(X_test)

actual = testing_data['is_fake']
predicted = y_pred_final

#%%

# RESULTADOS DEL MODELO
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

matrix = confusion_matrix(actual,predicted, labels=[1,0])
print('Matriz de Confusion : \n',matrix)

tp, fn, fp, tn = confusion_matrix(actual,predicted,labels=[1,0]).reshape(-1)
print('Outcome values : \n', tp, fn, fp, tn)

matrix = classification_report(actual,predicted,labels=[1,0])
print('Reporte de Clasificacion : \n',matrix)
