import  numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import *
from  tensorflow.keras.layers import *

X_train, X_test, Y_train, Y_test = np.load(
    './Youtube_data_max_29_wordsize_15336.npy', allow_pickle=True)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

model = Sequential()
model.add(Embedding(15336, 300, input_length=29))#자연어 의미를 학습하는 레이어
model.add(Conv1D(32, kernel_size=5, padding='same', activation='relu'))#주변단어들간의 앞뒤 위치관계를 학습 2D는 주변 픽셀간임
model.add(MaxPooling1D(pool_size=1))
model.add(LSTM(128, activation='tanh', return_sequences=True)) #정가 하나만 있을때는 사용안함 return
#LSTM이든 GRU든 자연어처리를 할때는 return_sequences=True를 줘야함 하나 들어오면 하나 나가고??
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh'))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(6, activation='softmax'))
model.summary()


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=128, epochs= 10, validation_data=(X_test, Y_test))
model.save('./models/news_category_classification_model_{}.h5'.format(fit_hist.history['val_accuracy'][-1]))
plt.plot(fit_hist.history['val_accuracy'], label='validation accuracy')
plt.plot(fit_hist.history['accuracy'], label='train accuracy')
plt.legend()
plt.show()

#벡터화: 단어의 의미를 부여하는거 여러차원을 활용해서 즉 의미공간상에 벡터화하는거임. 문장을 통해서 특정 형태소 형태로
#접근해서 좌표를 바꾸면서 비슷한 애들끼리 모이게 됨.
#위의경우 10897개의 차원이 만들어지고 근데 이 차원이 커질수록 데이터의 밀도가 작아짐. 즉 요소하나하나의 거리가 멀어짐.
#즉 데이터의 개수가 같은데 차원이 커지면 각 요소들의 벡터간의 거리가 멀어져 데이터가 희소해진다고 표현함
#그래서 데이터의 성질을 최대한 유지하면서 차원을 축소해야함. 그래서 위에 300은 최종적으로 줄어든 차원수를 의미함.