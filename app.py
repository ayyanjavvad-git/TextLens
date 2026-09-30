                                      #app.py -> Day 26
from flask import Flask, render_template, request, redirect, url_for
import os
import string

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    name = 'TextLens'
    return render_template('home.html', name=name, title='Home')

@app.route('/about')
def about():
    name = 'TextLens'
    creator = 'Ayyan Javvad'
    techs = ['HTML', 'CSS', 'Flask', 'Python']
    return render_template('about.html', name=name, techs=techs, creator=creator, title='About')

@app.route('/post', methods=['GET', 'POST'])
def post():
    name = 'Text Analyzer'

    if request.method == 'GET':
        return render_template('post.html', name=name, title=name)

    if request.method == 'POST':
        content = request.form['content']
        words = content.lower().split()
        clean_words=[]
        for word in words:
            clean_words.append(word.strip(string.punctuation))
        
        # Count words
        number_of_words = len(clean_words)

        # Count characters
        number_of_characters = len(content)

        # Count sentences
        number_of_sentences = (
            content.count('.') +
            content.count('!') +
            content.count('?')
        )

        # Find most common words
        word_frequency = {}
        for i in clean_words:
            if i in word_frequency:
                word_frequency[i] += 1
            else:
                word_frequency[i] = 1

        common_words = sorted(word_frequency.items(), key=lambda item: item[1], reverse=True)[:5]

        #Give review
        if number_of_words <= 25:
            suggestion = "This amount of words is suitable for a short message!"
        elif number_of_words <= 75:
            suggestion = "This amount of words is suitable for a text/personal message or a short email!"
        elif number_of_words <= 250:
            suggestion = "This amount of words is suitable for a long email or a medium-sized paragraph!"
        elif number_of_words <= 500:
            suggestion = "This amount of words is suitable for a long paragraph or a formal letter!"
        elif number_of_words > 750:
            suggestion = "This amount of words (or greater) is suitable for an essay!"


        return render_template(
            'result.html',
            title='Results',
            words=number_of_words,
            characters=number_of_characters,
            sentences=number_of_sentences,
            common_words=common_words,
            review=suggestion
        )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
