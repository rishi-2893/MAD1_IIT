from flask import Flask, render_template, request
import csv


# Data
data = []
with open("data.csv", 'r') as file:
    file.readline()
    reader = csv.reader(file)
    for r in reader:
        data += [tuple(r)]




app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    elif request.method == 'POST':
        if request.form.get('ID') == 'student_id':
            s_id = request.form.get('id_value')

            s_data = []
            tot_marks = 0
            for tup in data:
                if tup[0] == s_id:
                    s_data += [tup]
                    tot_marks += int(tup[2])
            if not s_data:
                return render_template('wrong.html')
            return render_template('student.html',data=s_data, tot_marks=tot_marks )

        else:
            c_id = request.form.get('id_value')

            c_data = []
            for tup in data:
                if tup[1] == " " + c_id:
                    c_data += [tup]
            
            if not c_data:
                return render_template('wrong.html')

            max_marks = max(list(map(lambda x: int(x[-1]), c_data)))
            avg_marks = sum(list(map(lambda x: int(x[-1]), c_data)))/len(c_data)
            
            import numpy as np
            import matplotlib.pyplot as plt
            c_data = np.array(c_data)
            # Extracting marks column
            marks = c_data[:, 2]

            # Creating histogram
            plt.hist(marks, edgecolor='black')

            # Setting labels and title
            plt.xlabel('Marks')
            plt.ylabel('Frequency')

            plt.savefig('static/graph.png')

            return render_template('course.html', avg_marks = avg_marks, max_marks = max_marks)



if __name__ == '__main__':
    app.run(debug=True)