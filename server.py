from progress import main
from flask import Flask, render_template_string
import pandas as pd
import os
from server_plot import main as plotter

app = Flask(__name__)


@app.route('/')
def home():
    # Generate the DataFrame
    df = main()
    best_data = plotter()
    # Convert DataFrame to HTML table with Bootstrap classes
    table_html = df.to_html(classes='table table-striped table-bordered', index=False)
    best_data_html = best_data.to_html(classes='table table-striped table-bordered', index=False)
    # HTML template with mobile-responsive design
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Runs tracker</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            /* Additional custom styling for mobile-friendliness */
            .container { max-width: 100%; }
            .table { width: 600px; max-width: 100%; margin: 0px auto 0px auto;}
        </style>
    </head>
    <body>
        <div class="container my-4">
            <h2 class="text-center">Data Table</h2>
            <div class="table-responsive">
                {{ table1|safe }}
            </div>
            <div class="table-responsive">
                {{ table2|safe }}
            </div>
            <div class="image-container">
                {% for image_path in images %}
                    <img src="{{ url_for('static', filename=image_path) }}" alt="Image {{ loop.index }}" width=600px style="max-width:90%">
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    '''

    # Render the HTML template and pass the table HTML
    return render_template_string(html_template, table1=table_html, table2=best_data_html, images=os.listdir("static"))



if __name__ == '__main__':
    app.run(debug=True)
