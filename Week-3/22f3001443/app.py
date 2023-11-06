import sys, csv
from jinja2 import Template


# Data
data = []
with open("data.csv", 'r') as file:
    file.readline()
    reader = csv.reader(file)
    for r in reader:
        data += [tuple(r)]



# Text for Querying on student
st = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Data</title>
</head>
<body>
    <h1>Student Details</h1>
    <table border="1">
        <thead>
            <th>Student id</th>
            <th>Course id</th>
            <th>Marks</th>
        </thead>
            {%- for row in data -%}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
            </tr>
            {%- endfor -%}
        <tfoot>
            <td colspan="2" align="center">Total Marks</td>
            <td >{{ tot_marks }}</td>
        </tfoot>
    </table>
</body>
</html>
"""


ct = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Data</title>
</head>
<body>
    <h1>Course Details</h1>
    <table border="1">
        <thead>
            <th>Average Marks</th>
            <th>Maximum Marks</th>
        </thead>
        <tr>
            <td>{{ avg_marks }}</td>
            <td>{{ max_marks }}</td>
        </tr>
    </table>
    <img src='graph.png' />
</body>
</html>
"""

wt = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Something Went Wrong</title>
</head>
<body>
    <h1>Wrong Inputs</h1>
    <p>Something went wrong</p>
</body>
</html>
"""



if sys.argv[1] == "-s":
    s_id = sys.argv[2]
    t = Template(st)

    s_data = []
    tot_marks = 0
    for tup in data:
        if tup[0] == s_id:
            s_data += [tup]
            tot_marks += int(tup[2])

    final = t.render(data = s_data, tot_marks = tot_marks)
    out = open("output.html", 'w')
    out.write(final)
    out.close()

elif sys.argv[1] == "-c":
    c_id = sys.argv[2]
    t = Template(ct)
    c_data = []
    for tup in data:
        if tup[1] == " " + c_id:
            c_data += [tup]

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

    plt.savefig('graph.png')

    final = t.render(avg_marks = avg_marks, max_marks = max_marks)
    out = open("output.html", 'w')
    out.write(final)
    out.close()

else:
    t = Template(wt)
    final = t.render()
    out = open("output.html", 'w')
    out.write(final)
    out.close()