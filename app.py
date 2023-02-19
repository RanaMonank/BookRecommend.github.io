from flask import Flask, render_template, request
import pickle
import numpy as np

populer_df = pickle.load(open("populer.pkl",'rb'))
pt = pickle.load(open("pt.pkl",'rb'))
similarity_score = pickle.load(open("similarity_score.pkl",'rb'))
books = pickle.load(open("books.pkl",'rb'))

app = Flask(__name__)

@app.route('/')

def index():
    return render_template("index.html",
                           book_name = list(populer_df['Book-Title'].values),
                           author = list(populer_df['Book-Author'].values),
                           image = list(populer_df['Image-URL-M'].values),
                           votes = list(populer_df['num_rating'].values),
                           rating = list(populer_df['avg_rating'].values),
                           )

@app.route('/')
def recommend_ui():
    return render_template('index.html')

@app.route("/recommend_books", methods=['post'])
def recommend():
    user_input = request.form.get("user_input")
    index = np.where(pt.index==user_input)[0][0]
    distances = similarity_score[index]
    book_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:7]
    
    data = []
    for i in book_list:
        items = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates("Book-Title")['Book-Title'].values))
        items.extend(list(temp_df.drop_duplicates("Book-Title")['Book-Author'].values))
        items.extend(list(temp_df.drop_duplicates("Book-Title")['Image-URL-M'].values))
        
        data.append(items)
        
    print(data)
        
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)