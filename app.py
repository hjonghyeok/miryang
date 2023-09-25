from flask import Flask,render_template
import miryang
from flask import request


app = Flask(__name__)

@app.route("/")
def hello_world():
    if request.args.get('keyword') is None:
        return render_template('index.html', context=None)
    keyword = request.args.get('keyword')
    df1 = miryang.run(keyword).head(8).sort_values(by='평균조회수', ascending=False)
    df2 = miryang.run(keyword).head(8).sort_values(by='평균댓글수', ascending=False)
    df_v = df1["해시태그"].tolist()
    df_v2 = df1["평균조회수"].tolist()
    df2_v = df2["해시태그"].tolist()
    df2_v2 = df2["평균댓글수"].tolist()
    백분율 = []
    for i in range(len(df_v2)):
        백분율.append(int(df_v2[i] * 100 / df_v2[0]))
    백분율2 = []
    for i in range(len(df2_v2)):
        백분율2.append(int(df2_v2[i] * 100 / df2_v2[0]))
    context = {
        "hashtag" : df_v,
        "view" : df_v2,
        "percent" : 백분율,
        "hashtag2" : df2_v,
        "comment" : df2_v2,
        "percent2" : 백분율2,
    }
    return render_template('index.html',context=context)
    # return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()