import requests
from bs4 import BeautifulSoup
from summarizer import Summarizer
from flask import Flask, render_template, request

app = Flask(__name__)

def get_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1').text
    paragraphs = soup.find_all('p')
    text = ' '.join([p.text for p in paragraphs])
    return title, text

def summarize_article(url):
    title, text = get_article(url)
    bert_model = Summarizer()
    summary = bert_model(text, ratio=0.3)  # Adjust the ratio to control the length of the summary
    return title, summary

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        title, summary = summarize_article(url)
        return render_template('summary.html', title=title, summary=summary)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
