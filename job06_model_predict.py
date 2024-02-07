#예측 할 데이터도 전처리가 필요하기 때문에 전처리할때 라벨링 했던정보를 로드해서
#다시 라벨링하면 앞에서 한것 기억해서 그대로 라벨링해줌
# 그렇게 라벨링하고나서 형태소 분리하고 불용어 처리하고
#토큰화 했던 정보활용해서 토큰화하고 모델가져와서 예측하면됨.
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
from tensorflow.keras.models import load_model



df = pd.read_csv('./news_titles_20240126.csv')
print(df.head())
df.info()

X = df['titles']
Y = df['category']

with open('./models/label_encoder.pickle','rb') as f:
    label_encoder = pickle.load(f)

label = label_encoder.classes_

print(label)

okt = Okt()

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)

stopwords = pd.read_csv('./stopwords.csv', index_col=0)
for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)

with open('./models/news_token.pickle', 'rb') as f:
    token = pickle.load(f)
tokened_x = token.texts_to_sequences(X)
for i in range(len(tokened_x)):
    if len(tokened_x[i]) > 29:
        tokened_x[i] = tokened_x[i][:29]
print(tokened_x)

x_pad = pad_sequences(tokened_x, 29)

model = load_model('./models/news_catrgory_calssification_model_0.9060083031654358.h5')
preds = model.predict(x_pad)

##여기서부턴 예측한거 표시해주려고 아래와같이 작성함

predicts = []
for pred in preds:
    most = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0
    second = label[np.argmax(pred)]
    predicts.append([most, second]) #제일 확률높은것과 그다음 높은거
df['predict'] = predicts

print(df)

df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] in df.loc[i, 'predict']:
        df.loc[i, 'OX'] = 'O'   #예측맞으면 O
    else:
        df.loc[i, 'OX'] = 'X'   #틀리면 X인걸 OX열에 나타냄
print(df['OX'].value_counts())
print(df['OX'].value_counts()/len(df))
















