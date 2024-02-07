#데이터들 모두 모아서 하나로 만들어주는거임 어려울거 없음
import pandas as pd
import glob
import datetime

last_data = []
keyword = ['cook', 'game', 'music', 'nature', 'pets', 'sports']
for i in keyword:
    data_paths = glob.glob('./data/crawling_data_{}_*'.format(i))
    if data_paths:
        last_data.append(data_paths[-1])

print(last_data)

df = pd.DataFrame()
for path in last_data:
    df_temp = pd.read_csv(path)     #csv파일 읽어오고
    df_temp.dropna(inplace=True)    #nan빼줌
    df = pd.concat([df, df_temp])   #합침.

if not df.empty:
    # Check if 'keyword' column is present in the DataFrame
    if 'keyword' in df.columns:
        print(df['keyword'].value_counts())
    else:
        print("Column 'keyword' not found in the DataFrame.")

    df.info()

    df.to_csv('./Youtube_titles_{}.csv'.format(
        datetime.datetime.now().strftime('%Y%m%d')), index=False)
else:
    print("DataFrame is empty. No CSV file generated.")