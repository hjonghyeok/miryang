import pandas as pd
import numpy as np

def 해시태그별_평균(df):
    # 2개 이상 있는 해시태그만 추출
    hashtag_list = list(np.ravel(df.loc[:,'해시태그1':'해시태그15'].values, order='C'))
    removes = []
    
    for i in hashtag_list:
        count = hashtag_list.count(i)
        if count <= 5:
            removes.append(i)

    hashtag_list = list(set(hashtag_list))
    for i in removes:
        if i in hashtag_list:
            hashtag_list.remove(i)
            
    # 빈 리스트 생성
    hashtag_data = []
    
    # 추출한 해시태그 평균 값 데이터 리스트에 저장
    for i in hashtag_list:
        키워드 = i
        조회수 = df[df.filter(like='해시태그').eq(키워드).any(axis=1)]['조회 수'].mean()
        댓글수 = df[df.filter(like='해시태그').eq(키워드).any(axis=1)]['댓글 수'].mean()
        LIST = [키워드, 조회수, 댓글수]
        hashtag_data.append(LIST)

    # 리스트를 데이터프레임으로 변환
    hashtag_df = pd.DataFrame(hashtag_data, columns=['해시태그', '평균조회수', '평균댓글수'])

    # 시각화
#     hashtag_df[:7].plot.bar(x='해시태그', y='평균조회수', rot=1)
    hashtag_df = hashtag_df.dropna()
    return hashtag_df

def 키워드추출(df, 키워드):
    hashtag_columns = [f'해시태그{i}' for i in range(1, 11)]  # '해시태그1'부터 '해시태그10'까지의 열 이름 리스트 생성
    condition = df[hashtag_columns].eq(키워드).any(axis=1)  # 키워드가 포함된 행을 찾는 조건 생성
    return df[condition]

def 예측(LIST, df):    
    all_hashtag = list(np.ravel(df.loc[:, '해시태그1':'해시태그15'].values, order='C'))
    LIST2 = [[i, all_hashtag.count(i)] for i in LIST]
    LIST2.sort(key=lambda x: -x[1])
    LIST = [i[0] for i in LIST2]
    for i in LIST:
        ndf = 키워드추출(df, i)
        if i == LIST[-1]:
            ndf = 해시태그별_평균(ndf)
    
    return ndf.sort_values(by='평균조회수', ascending=False)

def run(입력):
    df = pd.read_csv('m_data.csv')
    df = df.loc[:,'조회 수':'해시태그15']
    입력 = 입력.split(" ")
    for i in range(len(입력)):
        if 입력[i][0] != "#":
            입력[i] = "#" + 입력[i]
            
    예측값 = 예측(입력, df)
    # 예측값 = 예측값["평균조회수"].sort_values(ascending=False)
    예측값 = 예측값.dropna().astype({'평균조회수':'int', '평균댓글수':'int'})
    return 예측값

