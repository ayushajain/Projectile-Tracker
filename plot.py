from matplotlib import pyplot as plt
import pylab, csv, numpy as np


file1 = open("data/s9t1.csv", "U")
reader = csv.reader(file1)

c = 0
x = []
y = []

for line in reader:
    if c > 0:
        print "test"

        print line
        x.append(float(line[1]))
        y.append(float(line[2]))

    c += 1

print y
plt.ylim([0,max(y)])
plt.xlim([0,max(x)])

title_text = "Projectile Plot"
plt.plot(x, y, linewidth=2.0)
plt.title(title_text)
plt.show()
