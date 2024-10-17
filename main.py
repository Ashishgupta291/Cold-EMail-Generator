from flask import Flask, render_template, request, jsonify
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

app = Flask(__name__)

chain = Chain()
portfolio = Portfolio()

@app.route('/', methods=['GET','POST'])
def home():
    try:
        email_responses = None
        if request.method == 'POST':
            url = request.form.get('url')
            loader = WebBaseLoader([url])
            # enter correct link
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = chain.extract_jobs(data)
            print(jobs)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = chain.write_mail(job, links)
                email_responses=email 
                print(email)
                break # usually only one job
        return render_template('index.html', mail=email_responses)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
