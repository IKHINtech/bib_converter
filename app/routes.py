from app import app
from flask import flash, request, redirect, url_for, render_template
from config import Config

#perlengkapan convert
import bibtexparser
import pandas as pd
from bibtexparser.bparser import BibTexParser



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def convert():
    parser = BibTexParser(common_strings=False)
    parser.ignore_nonstandard_types=False
    parser.homogenize_fields= False
    
    if request.method== 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('no selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            bibtex_file = file.stream
            # with open(file.stream, encoding='utf-8') as bibtex_file:
            bibtex_str = bibtex_file.read() 
            bib_database = bibtexparser.loads(bibtex_str, parser)
            df = pd.DataFrame(bib_database.entries)
            return df.to_json()
        else:
            return 'extensi file salah'
    return render_template('index.html')
    # return df.to_.json
            