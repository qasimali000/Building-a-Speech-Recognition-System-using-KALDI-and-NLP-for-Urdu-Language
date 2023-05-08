from flask import Flask, render_template, request, jsonify, flash, Response, url_for
import os
import pandas as pd
import numpy as np
import xlrd
import xlsxwriter

import glob
import csv
# import Pipeline
# Pipeline.main()
from werkzeug.utils import redirect

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# path =r'E:\app'
# excel_filenames = glob.glob(path + "/*.xlsx")


# for i in excel_filenames:
'''
df = pd.read_excel('/final_rep.xlsx')
df['Opening'] = df['Opening'].map({'Found': 1, 'Not Found': 0})
df['Upselling'] = df['Upselling'].map({'Found': 1, 'Not Found': 0})
df['Other'] = df['Other'].map({'Found': 1, 'Not Found': 0})
df['Address_confirmation'] = df['Address_confirmation'].map({'Found': 1, 'Not Found': 0})
df['Payment_mode_verification'] = df['Payment_mode_verification'].map({'Found': 1, 'Not Found': 0})
df['Closing'] = df['Closing'].map({'Found': 1, 'Not Found': 0})
df['order confirmation'] = df['order confirmation'].map({'Found': 1, 'Not Found': 0})
'''


def mt_2_st(time):
    hours = int(time[0:2])
    minutes = int(time[2:4])
    seconds = int(time[4:6])
    if hours >= 12:
        meridian = "pm"
        hours %= 12
    else:
        meridian = "am"
    if hours == 0:
        hours = 12
    return "{0}:{1}:{2} {3}".format(hours, minutes, seconds, meridian)


@app.route('/', methods=['GET', 'POST'])
def start():
    efilenames = os.listdir("Files/consolidated_reports")
    if request.method == "POST":
        up = request.form.get('select_file')
        return redirect(url_for("files", up=up))
    return render_template("base.html", efilenames=efilenames)


'''
@app.route('/file', methods=['GET', 'POST'])
def file():
    if request.method == "POST":
        f = request.files['file']
        up = f.filename
        #uuid = 'ABC'
        f.save(os.path.join("D:/", f.filename))
        return redirect(url_for("files", up=up))
'''


@app.route('/files/<up>', methods=['GET', 'POST'])
def files(up):
    efilenames = os.listdir("Files/consolidated_reports")
    # f = request.files['file']
    with open("Files/consolidated_reports/{}".format(up), "rb") as f:
        df = pd.read_excel(f)
    # df = pd.read_excel('E:/app/final_rep.xlsx')
    # df['Opening'] = df['Opening'].map({'Found': 1, 'Not Found': 0})
    # df['Upselling'] = df['Upselling'].map({'Found': 1, 'Not Found': 0})
    # df['Other'] = df['Other'].map({'Found': 1, 'Not Found': 0})
    # df['Address_confirmation'] = df['Address_confirmation'].map({'Found': 1, 'Not Found': 0})
    # df['Payment_mode_verification'] = df['Payment_mode_verification'].map({'Found': 1, 'Not Found': 0})
    # df['Closing'] = df['Closing'].map({'Found': 1, 'Not Found': 0})
    # df['order confirmation'] = df['order confirmation'].map({'Found': 1, 'Not Found': 0})
    filenames = list(df['Campaign'])
    df.rename(columns={'Unnamed: 0': 'S_no'}, inplace=True)

    index = request.args.get("index")
    if not index:
        index = 0
    index = int(index)
    last = len(filenames) - 1

    if index == 0:
        prev = "#"
        next = "?index=" + str(index + 1)
    elif index == last:
        prev = "?index=" + str(index - 1)
        next = "#"
    else:
        prev = "?index=" + str(index - 1)
        next = "?index=" + str(index + 1)
    '''
    #Pagination
    filename = request.args.get("filename")
    if not filename:
        filename = filenames[0]
    last = filenames[-1]


    if filename == filenames[0]:
        prev = "#"
        next = "?filename=" + str(filenames[1])
    elif filename == last:
        prev = "?filename=" + str(filenames[-2])
        next = "#"
    else:
        index = filenames.index(filename)
        prev = "?filename=" + str(filenames[index - 1])
        next = "?filename=" + str(filenames[index + 1])
    '''
    # index = filenames.index(filename)
    # index = 0
    # last_index = len(filenames)

    filename = df['Campaign'][index]
    date = df['Date'][index]
    time = df['Call Time'][index]
    d = df['Duration'][index]
    sd = df['Silence_Duration'][index]
    tod = df['Total_Overlap_Duration'][index]
    mod = df['Max_Overlap_Duration'][index]
    wg = df['Opening'][index]
    gg = df['Closing'][index]
    u = df['Suggestive_Selling'][index]
    av = df['Address_confirmation'][index]
    pv = df['Payment_mode_verification'][index]
    oc = df['order confirmation'][index]
    o = df['Other'][index]
    score = df['scores'][index]
    if request.method == 'POST':
        additional_feedback = request.form["add"]
        other = request.form["other"]
        order_confirmation = request.form["order_confirmation"]
        payment_verification_feed = request.form["payment_verification_feed"]
        address_verification_feed = request.form["address_verification_feed"]
        Upselling = request.form["Upselling_feed"]
        goodbye_feed = request.form["goodbye_feed"]
        welcome_greeting_feed = request.form["welcome_greeting_feed"]
        path = "Files/consolidated_reports/{}".format(up)
        df2 = pd.DataFrame(index=range(last+1), columns=['welcome_greeting_feed',
                                                       'goodbye_feed',
                                                       'Suggestive_Selling',
                                                       'address_verification_feed',
                                                       'payment_verification_feed',
                                                       'order_confirmation',
                                                       'other',
                                                       'additional_feedback'])
        df2['S_no'] = np.arange(len(df2))
        df2.at[index, 'additional_feedback'] = additional_feedback
        df2.at[index, 'other'] = other
        df2.at[index, 'order_confirmation'] = order_confirmation
        df2.at[index, 'payment_verification_feed'] = payment_verification_feed
        df2.at[index, 'address_verification_feed'] = address_verification_feed
        df2.at[index, 'Upselling'] = Upselling
        df2.at[index, 'goodbye_feed'] = goodbye_feed
        df2.at[index, 'welcome_greeting_feed'] = welcome_greeting_feed
        final_df = pd.merge(df, df2, on='S_no')
        print(final_df)

        return render_template('base.html',
                               efilenames = efilenames,
                               filename=filename,
                               date=date,
                               time=time,
                               d=d,
                               sd=sd,
                               tod=tod,
                               mod=mod,
                               wg=wg,
                               gg=gg,
                               u=u,
                               av=av,
                               pv=pv,
                               oc=oc,
                               o=o,
                               score=score,
                               next=next,
                               prev=prev)
    else:
        return render_template('base.html',
                               efilenames=efilenames,
                               filename=filename,
                               date=date,
                               time=time,
                               d=d,
                               sd=sd,
                               tod=tod,
                               mod=mod,
                               wg=wg,
                               gg=gg,
                               u=u,
                               av=av,
                               pv=pv,
                               oc=oc,
                               o=o,
                               score=score,
                               next=next,
                               prev=prev)


"""
@app.route("/report", methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        additional_feedback = request.form["add"]
        other = request.form["other"]
        order_confirmation = request.form["order_confirmation"]
        payment_verification_feed = request.form["payment_verification_feed"]
        address_verification_feed = request.form["address_verification_feed"]
        Upselling = request.form["Upselling_feed"]
        goodbye_feed = request.form["goodbye_feed"]
        welcome_greeting_feed = request.form["welcome_greeting_feed"]

        return render_template('test.html',
                               filename=filename,
                               date=date,
                               time=time,
                               d=d,
                               sd=sd,
                               tod=tod,
                               mod=mod,
                               wg=wg,
                               gg=gg,
                               u=u,
                               av=av,
                               pv=pv,
                               oc=oc,
                               o=o,
                               next=next,
                               prev=prev)
    else:
        return render_template('test.html')



@app.route("/report", methods=['GET', 'POST'])
def report():
    #page = request.args.get('page')
    #if not str(page).isnumeric():
    #    page = 1
    if request.method == 'POST':
        additional_feedback = request.form["add"]
        other = request.form["other"]
        order_confirmation = request.form["order_confirmation"]
        payment_verification_feed = request.form["payment_verification_feed"]
        address_verification_feed = request.form["address_verification_feed"]
        Upselling = request.form["Upselling_feed"]
        goodbye_feed = request.form["goodbye_feed"]
        welcome_greeting_feed = request.form["welcome_greeting_feed"]
        return render_template('base.html',
                               filename=filename,
                               date=date,
                               time=time,
                               d=d,
                               sd=sd,
                               tod=tod,
                               mod=mod,
                               wg=wg,
                               gg=gg,
                               u=u,
                               av=av,
                               pv=pv,
                               oc=oc,
                               o=o,
                               next=next,
                               prev=prev)
    else:
        return render_template('base.html',
                               filename=filename,
                               date=date,
                               time=time,
                               d=d,
                               sd=sd,
                               tod=tod,
                               mod=mod,
                               wg=wg,
                               gg=gg,
                               u=u,
                               av=av,
                               pv=pv,
                               oc=oc,
                               o=o,
                               next=next,
                               prev=prev)

"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000,debug=True)
