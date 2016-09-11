from matplotlib import pyplot as plt
import csv

# read 3 trials
reader1 = list(csv.reader(open("data/s7v2t1.csv", "U")))
reader2 = list(csv.reader(open("data/s7v2t2.csv", "U")))
reader3 = list(csv.reader(open("data/s7v2t3.csv", "U")))

max_lines = min(len(reader1), len(reader2), len(reader3))

# trial data
time = []
x = []
upper_xs = []
lower_xs = []
uncertainty_x = []
y = []
upper_ys = []
lower_ys = []
uncertainty_y = []

# graphs of 3 trials
g1 = []
g2 = []
g3 = []

for i in range(1, max_lines):

    # increment time
    if len(time) == 0:
        time.append(0)
    else:
        time.append(time[len(time) - 1] + 1/30.0)

    g1.append([float(reader1[i][1]), float(reader1[i][2])])
    g2.append([float(reader2[i][1]), float(reader2[i][2])])
    g3.append([float(reader3[i][1]), float(reader3[i][2])])

    # calculate
    line_x = [float(reader1[i][1]), float(reader2[i][1]), float(reader3[i][1])]
    line_y = [float(reader1[i][2]), float(reader2[i][2]), float(reader3[i][2])]
    avg_x = sum(line_x)/3
    avg_y = sum(line_y)/3
    x.append(avg_x)
    y.append(avg_y)
    upper_x = max(line_x)
    lower_x = min(line_x)
    upper_y = max(line_y)
    lower_y = min(line_y)
    upper_xs.append(upper_x)
    lower_xs.append(lower_x)
    upper_ys.append(upper_y)
    lower_ys.append(lower_y)
    uncertainty_x.append((upper_x - lower_x)/2.0)
    uncertainty_y.append((upper_y - lower_y)/2.0)

unc_x = sum(uncertainty_x)/len(uncertainty_x)
unc_y = sum(uncertainty_y)/len(uncertainty_y)

# set scale and title graphs
plt.ylim([min(lower_xs), max(upper_xs)])
plt.xlim([0, max(time)])
plt.ylabel("Position X (cm)")
plt.xlabel("Time (s)")
title_text = "Illustration 1 (G2): Position X vs. Time (Avg. Uncert. = +/- " + "{0:.4f}".format(unc_x) + " cm)"

# plot average and upper + lower bounds
plt.fill_between(time, lower_xs, upper_xs, facecolor = "red")
plt.plot(time, x, linewidth=2.0)

# plot trials side by side
#plt.plot(time, zip(*g1)[0], linewidth=2.0)
#plt.plot(time, zip(*g2)[0], linewidth=2.0)
#plt.plot(time, zip(*g3)[0], linewidth=2.0)

plt.title(title_text)
plt.show()
