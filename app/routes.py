import re
from app import app
from flask import flash, request, redirect, url_for, render_template, send_from_directory, render_template_string
from config import Config


#perlengkapan convert
import bibtexparser
import pandas as pd
from bibtexparser.bparser import BibTexParser

#convert from ris file
from pprint import pprint
from RISparser import parser, readris, read, TAG_KEY_MAPPING

#rispy
import rispy

#pip install bibliograph.parsing
from bibliograph.parsing import parsers

#xml
import xml.etree.ElementTree as ET
from io import StringIO
import xmltodict, json


html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="shortcut icon" href={{ url_for('static', filename='favicon.ico')}} type="image/x-icon">
    <link rel="stylesheet" href={{ url_for('static',filename='bootstrap-4.6.0-dist/css/bootstrap.css')}} type="text/css">
    <link rel="stylesheet" href={{ url_for('static',
    filename='DataTables/DataTables-1.10.23/css/dataTables.bootstrap4.min.css') }} type="text/css">
    <link rel="stylesheet" href={{ url_for('static',
    filename='DataTables/Buttons-1.6.5/css/buttons.bootstrap4.min.css') }} type="text/css">

    <!-- Jquery-->
    <script src={{ url_for('static',filename='jquery-3.5.1.js')}}></script>
    <!-- Datatable-->
    <script src={{ url_for('static',
    filename='DataTables/datatables.min.js') }}></script>
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
    <style>
        /* Sticky footer styles
        -------------------------------------------------- */
        html {
        position: relative;
        min-height: 100%;
        }
        body {
        /* Margin bottom by footer height */
        margin-bottom: 60px;
        }
        .footer {
        position: absolute;
        bottom: 0;
        width: 100%;
        /* Set the fixed height of the footer here */
        height: 60px;
        line-height: 60px; /* Vertically center the text there */
        background-color: #f5f5f5;
        }


        /* Custom page CSS
        -------------------------------------------------- */
        /* Not required for template or sticky footer method. */

        body > .container {
        padding: 60px 15px 0;
        }

        .footer > .container {
        padding-right: 15px;
        padding-left: 15px;
        }

        code {
        font-size: 80%;
        }
    </style>
    <title>Convert from {{ filenm }}</title>
  </head>
  <body>
    <header>
        <nav class="navbar navbar-dark bg-dark">
        <a class="navbar-brand" href="/">Home</a>
        </nav>
    </header>
    <br>
      <h1 class="text-center">Convert {{ filenm }} </h1>
      <div class="col-md-12">
      {{table | safe}}
      <br>
       </div>
      <script>
         $(document).ready(function(){
        $('#example').DataTable({
            dom: 'Blfrtip',
        buttons: [
            'csv', 'excel', 'pdf', 'colvis'
        ]
        });
    });
      </script>
    
      <footer class="footer bg-dark">
      <div class="">
        <span class="text-muted">File Converter From Export Mendeley </span>
      </div>
    </footer>
  </body>
</html>

'''


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
                df.index += 1
                return render_template_string(html, filenm = file.filename, 
                                                table = df.to_html(index='Nomor', header='true', table_id='example', 
                                                classes='table table-striped table-bordered'))
            elif file and file_ris(file.filename):
                ris_file = file
                # ris_str = ris_file
                entries = rispy.load(ris_file)
                # for enri in entries:
                #     print(enri)
                # mapping = TAG_KEY_MAPPING
                # for data in ris_file:
                #     entries = list(readris(ris_file, mapping=mapping))
                #     return render_template('output1.html', data= entries.decode())
                    ###############################
                # mapping = TAG_KEY_MAPPING
                # ris_file = file
                # entries = list(readris(ris_file, mapping=mapping))
                # render_template('output1.html', ris_file=entries)
                # entries = list(readris(ris_file, mapping=mapping))
                # pprint(sorted(entries[1].items()))
                # data = pd.DataFrame(entries)
                # output = data.to_html(header='true', table_id='example', classes='table table-striped table-bordered')
                # # data1 = str(data, encoding='utf-8')
                # return  render_template_string(html.decode(), filenm = file.filename, table = output )
            else:
                data = xmltodict.parse(file)
                json_data = json.dumps(data)
                wanda = pd.read_json(StringIO(json_data))
                vision = wanda["xml"]['records']['record']
                axel = pd.DataFrame(vision)
                if axel.index[0] == '@name':
                    if axel['database'] is not None:
                        del axel['database']
                        # axel.index +=1
                    else:
                        None
                else:
                    if axel['database'] is not None:
                        del axel['database']
                    else:
                        None
                    #for get type value
                    type_data = []
                    for i, each in enumerate(axel['ref-type']):
                        if '@name' in axel['ref-type'][i].keys():
                            try:
                                data_type = axel['ref-type'][i]['@name']
                                type_data.append(data_type)
                            except Exception as e:
                                print(e)
                    axel['ref-type'] = type_data
                    #for get author value
                    authors = []
                    for i, each in enumerate(axel['contributors']):
                        if 'authors' in axel['contributors'][i].keys():
                            try:
                                data_author = axel['contributors'][i]['authors']['author']
                                authors.append(data_author)
                            except Exception as e:
                                print(e)
                    axel['contributors'] = authors
                    # for get title
                    titles=[]
                    for i, each in enumerate(axel['titles']):
                        title_data = axel['titles'][i].values()
                        titles.append(title_data)
                    axel['titles']= titles
                    # for get full-tittle
                    periodical=[]
                    for i, each in enumerate(axel['periodical']):
                        hulk = axel['periodical'][i]
                        if hulk is not None: # else hulk = 'NaN' 
                            periodical_data = hulk.values()
                        periodical.append(periodical_data)
                    axel['periodical']= periodical
                    # FOR GET keywords
                    # keyw=[]
                    # for i, each in enumerate(axel['keywords']):
                    #     hawk_eye = axel['keywords'][i]
                    #     if hawk_eye is not None: # else hulk = 'NaN' 
                    #         keyw_data = hawk_eye.values()
                    # keyw.append(keyw_data)
                    # axel['keywords']= keyw
                    axel.index += 1
                return render_template_string(html, filenm = file.filename, 
                                                table = axel.to_html(header='true', table_id='example', 
                                                classes='table table-striped table-bordered'))
        else:
            return render_template('output1.html')
    return render_template('index.html')
    # return df.to_.json
@app.route('/output')
def output():
    data = request.args.get('data', None)
    return render_template('output.html', data=data)