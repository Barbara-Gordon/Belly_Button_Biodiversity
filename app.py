import sqlite3 

import pandas as pd

from flask import Flask, jsonify, render_template

app = Flask(__name__)


#################################################
# Database Setup
#################################################
conn = sqlite3.connect("db/bellybutton.sqlite")


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Return a list of sample names."""
    names = []
    conn = sqlite3.connect("db/bellybutton.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT(sample) from Sample_Metadata")
    results = cur.fetchall()
    for r in results:
        names.append(r[0])

    return jsonify(names)


@app.route("/metadata/<sample>")
def sample_metadata(sample):
    #"""Return the MetaData for a given sample."""
    input_sample = sample
    conn = sqlite3.connect("db/bellybutton.sqlite")
    cur = conn.cursor()
    cur.execute(f"SELECT SAMPLE, ETHNICITY, GENDER, AGE, LOCATION, BBTYPE, WFREQ from Sample_Metadata where SAMPLE = {input_sample}")
    results = cur.fetchall()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        sample_metadata["ETHNICITY"] = result[1]
        sample_metadata["GENDER"] = result[2]
        sample_metadata["AGE"] = result[3]
        sample_metadata["LOCATION"] = result[4]
        sample_metadata["BBTYPE"] = result[5]
        sample_metadata["WFREQ"] = result[6]

    print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/samples/<sample>")
def samples(sample):
   # """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    conn = sqlite3.connect("db/bellybutton.sqlite")
    df_test = pd.read_sql("SELECT * from samples", conn)

    sample_data = df_test[['otu_id','otu_label',str(sample)]]

    sample_data = sample_data.loc[sample_data[str(sample)]>1,:]
    sample_data.sort_values(by=str(sample), ascending=False)

    # Format the data to send as json
    data = {
        "otu_ids": sample_data['otu_id'].tolist(),
        "sample_values": sample_data[str(sample)].tolist(),
        "otu_labels": sample_data['otu_label'].tolist(),
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
