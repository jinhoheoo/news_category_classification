#전처리 단계에서 카테고리를 라벨 인코더로 라벨 0 1 2 이런식으로 부여하고
# 그 이후에 원핫엔코더로 0을 1 0 0 이렇게 1을 0 1 0 이렇게 쭈우욱 라벨을 머신러닝할때 사용하게 만듬
# 그후에 okt로 형태소를 만들기 위해 어간들을 뽑아냄 즉 많다에서 많 이걸 각각 만들어냄 그걸 한글자든 두글자든 인덱스 한칸에 넣음
# 그 후에 불용어 stopword로 필요없는 글자들을 타이틀에서 각각 for과 if not이용해 각각의 항목에 똑같은거 있으면 빼는식으로 처리함
# 그 다음에 각 글자와 문장들을 토큰화해서 번호 부여함 사랑을 1 행복을 2 이런식으로 토큰화하는거임.
# 그 후에 각 문장들의 길이를 맞춰주고 검증데이터와 훈련데이터를 구분해서 저장해주면됨.
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

df = pd.read_csv('./naver_news_titles_20240125.csv')
print(df.head())
df.info()

X = df['titles']
Y = df['category']

label_encoder = LabelEncoder()
labeled_y = label_encoder.fit_transform(Y) #라벨 부여
print(labeled_y[:3])
label = label_encoder.classes_  #부여된 라벨 정보를 확인
print(label)
with open('./models/label_encoder.pickle', 'wb') as f:
    pickle.dump(label_encoder, f)   # 이걸실행하면 models 폴더에 label_encoder.pickle이라는 폴더가 열음, wb(writebinary)
    # pickle : 원래 그 형태 그대로 가져옴 ( 피클을 담그면 나중에 먹어도 그 맛 그대로 가져옴 )
onehot_y = to_categorical(labeled_y)
print(onehot_y[:3])
print(X[:5])
okt = Okt()
#for i in range(len(X[:5])):
 #   X[i] = okt.morphs(X[i])  #그냥 짜르기만 한다.
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True) #원형으로 바꾸어 주고
    if i % 1000:
        print(i)
#print(X[:5]) #한글자는 학습이 불가능, 접속사, 감탄사 는 의미 없음

# 0       한동훈  민주당 운동권에 죄송한 마음 전혀 없어 청년에겐 죄송함 커   Politics
# 어절 하나하나에다가 토큰을 붙여주면 너무 말이 많으니까, 쪼개진 애들이 형태소 야.
# 그 작업을 하기 위해서 필요한 게 Okt 야. okt: 형태소 분리를 해주는 거야.
#감탄사는 의미 학습에서 의미가 없고 오히려 방해만 되서 제거해 줘야함. 이렇게 모델이 학습하는데 필요없는 단어를 불용어라고함.


stopwords = pd.read_csv('./stopwords.csv', index_col=0)
for j in range(len(X)):
    words = [] # j는 문장
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:            #한글은 한글자짜리 단어 의미 없어서 이렇게 없앰 영어는 그냥 띄어쓰기로 구분하면 되서 더 쉬움
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)
#print(X[:5]) #불필요한 문자들을 삭제하고 리스트에 저장

#각 단어에 번로를 부여 (같은 형태소에 같은 번호를 붙여 주었다.)
token = Tokenizer()  #문재인을 4로 저장했는데 다시 fit on texts를 하면 4말고 5로 부여할 수 도 있음 그래서 이것을 저장해 놔야함
token.fit_on_texts(X) #라벨을 붙이기
tokened_x = token.texts_to_sequences(X) #문장을 숫자 번호로 만듬
wordsize = len(token.word_index) + 1 #index가 1붙어 만들어 진다. +1를 더한 이유는 0을 쓰기 위함
#print(tokened_x)
print(wordsize) #사실 모든 총 숫자는 33개

with open('./models/Youtube_token.pickle', 'wb') as f:
    pickle.dump(token, f)

# lstm을 쓰지만, 의미있는 단어들은 뒤쪽에 배치하고 아무것도 없는 것은 앞쪽에 0을 입력시킬거에요.
 #lstm을 쓰지만, 의미있는 단어는 뒷쪽에 위치하는게 좋음 사이즈가 작은 애들은 앞쪽에 0을 붙여서 모델들의 사이즈를 맞춰줌
max = 0 #최대값을 찾는 코드
for i in range(len(tokened_x)):
    if max < len(tokened_x[i]):
        max = len(tokened_x[i])
print(max)

x_pad = pad_sequences(tokened_x, max) #앞에 다가 0을 채워 길이를 맞추기 위함 (뒤로 가는게 학습에 좋기 때문에)
print(x_pad)

X_train, X_test, Y_train, Y_test = train_test_split(
    x_pad, onehot_y, test_size = 0.2)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
xy = np.array(xy, dtype=object)
np.save('./Youtube_data_max_{}_wordsize_{}'.format(max, wordsize), xy) #저장