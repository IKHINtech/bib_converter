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