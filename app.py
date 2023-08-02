# app.py
from flask import Flask, render_template, request
import pandas as pd
import pickle
import difflib
import numpy as np

app = Flask(__name__)

# Load recommendation data from a DataFrame
popularity_df = pickle.load(open('popular_books.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))
book_list = pickle.load(open('book_list.pkl','rb'))

# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    book_name = list(popularity_df['Book-Title'].values)
    author = list(popularity_df['Book-Author'].values)
    image = list(popularity_df['Image-URL-M'].values)
    rating = list(round(popularity_df['Average_rating'],1).values)
    no_of_ratings = list(popularity_df['Number_of_ratings'].values)
    return render_template('index.html', book_name = book_name, author = author, 
                            image = image, rating = rating, no_of_ratings = no_of_ratings)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['GET', 'POST'])
def recommend_books():
    user_input = str(request.form.get('user_input'))
    try:
        book_index = np.where(pt.index == user_input)[0][0]
    except:
        user_input = difflib.get_close_matches(user_input, book_list)[0]
        book_index = np.where(pt.index == user_input)[0][0]
        print(user_input)
    finally:
        distance = similarity_score[book_index]
        similar_books = sorted(list(enumerate(distance)), key= lambda x: x[1], reverse = True)[1:11]
        data = []
        for i in similar_books:
            temp = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            temp.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            temp.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            temp.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(temp)
       
    return render_template('recommend.html', data = data)


if __name__ == '__main__':
    app.run(debug=True)
