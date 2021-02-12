from app import app
from flask import flash, request, redirect, url_for, render_template, jsonify, render_template_string
from config import Config

#perlengkapan convert
import bibtexparser
import pandas as pd
from bibtexparser.bparser import BibTexParser

#convert from ris file
from pprint import pprint
from RISparser import readris



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def file_bib(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS[0]

def file_xml(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS[1] 

def file_ris(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS[2] 

html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href={{ url_for('static',filename='bootstrap-4.6.0-dist/css/bootstrap.css')}} type="text/css">
    <link rel="stylesheet" href={{ url_for('static',
    filename='DataTables/DataTables-1.10.23/css/dataTables.bootstrap4.min.css') }} type="text/css">
    <link rel="stylesheet" href={{ url_for('static',
    filename='DataTables/Buttons-1.6.5/css/buttons.bootstrap4.min.css') }} type="text/css">

    <!-- Jquery-->
    <script src={{ url_for('static',filename='jquery-3.5.1.js')}}></script>
    <!-- Datatable-->
    <script src={{ url_for('static',
    filename='DataTables/dataTables.min.js') }}></script>
    <!-- datatable bbotstrap-->
    <script src={{ url_for('static',
    filename='DataTables/DataTables-1.10.23/js/dataTables.bootstrap4.min.js') }}></script>
    <!-- Button-->
    <script src={{ url_for('static',
    filename='DataTables/Buttons-1.6.5/js/buttons.bootstrap4.min.js') }}></script>
    <script src={{ url_for('static',
    filename='DataTables/Buttons-1.6.5/js/buttons.colVis.min.js') }}></script>
     <!-- Jquery-->
    <script src={{ url_for('static',filename='jszip.min.js')}}></script>
    <script src={{ url_for('static',filename='pdfmake.min.js')}}></script>
    <script src={{ url_for('static',filename='vfs_fonts.js')}}></script>
    <script src={{ url_for('static',filename='buttons.html5.min.js')}}></script>
    <script src={{ url_for('static',filename='buttons.print.min.js')}}></script>
    <title>Convert from {{ filenm }}</title>
  </head>
  <body>
    
      <h1 class="center">Convert {{ filenm }} </h1>
      <div class="col-md-12">

      {{table | safe}}

       </div>
    

      <script>
         $(document).ready(function(){
        $('#example').DataTable({
            dom: 'Blfrtip',
        buttons: [
            'csv', 'excel', 'pdf', 'print', 'colvis'
        ]
        });
    });
      </script>
  </body>
</html>

'''

@app.route('/', methods=['GET', 'POST'])
def convert():
    parser = BibTexParser(common_strings=False)
    parser.ignore_nonstandard_types=False
    parser.homogenize_fields= False
    
    if request.method== 'POST':
        file = request.files['filer_input']
        if file.filename == '':
            flash('no selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if file and file_bib(file.filename):
                bibtex_file = file.stream
                bibtex_str = bibtex_file.read() 
                bib_database = bibtexparser.loads(bibtex_str, parser)
                df = pd.DataFrame(bib_database.entries)
                # return bib_database.entries_dict
                # data = df.to_html()
                return render_template_string(html, filenm = file.filename, table = df.to_html(header='true', table_id='example', classes='table table-striped table-bordered'))
                # return render_template('output1.html', table = df.to_html(header='true', table_id='example', classes='table table-striped table-bordered'))
            elif file and file_ris(file.filename):
                ris_file = file.stream
                entries = readris(ris_file)
                data = pd.DataFrame(entries)
                return render_template_string(html, filenm = file.filename, table = data.to_html(encoding= 'utf-8',header='true', table_id='example', classes='table table-striped table-bordered',))
            else:    
                return '<h1>ini file xml</h1>'
        else:
            return '<h1>extensi file salah</h1>'
    return render_template('index.html')
    # return df.to_.json
@app.route('/output')
def output():
    data = request.args.get('data', None)
    return render_template('output.html', data=data)