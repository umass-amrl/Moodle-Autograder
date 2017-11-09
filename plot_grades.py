#! /usr/bin/env python3
import csv
import sys
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    print("Usage: plot_grades.py <output CSV file>")
    exit(-1)

csvfile = open(sys.argv[1], 'rt')
reader = csv.reader(csvfile, delimiter=',', quotechar='"')
grades = [row[4] for row in reader]
grades = sorted([float(g) for g in grades[1:]])
print("Grades: {}".format(grades))
print("Students 100+: {}".format(len([g for g in grades if g >= 100])))
print("Students [90 to 100): {}".format(len([g for g in grades if g >= 90 and g < 100])))
print("Students [80 to 90): {}".format(len([g for g in grades if g >= 80 and g < 90])))
print("Students [70 to 80): {}".format(len([g for g in grades if g >= 70 and g < 80])))
print("Students [60 to 70): {}".format(len([g for g in grades if g >= 60 and g < 70])))
print("Students below 60: {}".format(len([g for g in grades if g < 60])))
bin_size = 1
max_grade = 110
bins = [bin_size * x for x in range(int(max_grade / bin_size) + 1)]
plt.hist(grades, bins=bins , facecolor='green', alpha=0.75)
plt.xlabel('Grade')
plt.ylabel('Number of students')
plt.title('Histogram of students grades, bin size of {}, max grade of {}'.format(bin_size, str(max_grade)))
plt.grid(True)
plt.xlim([0, 110])
plt.show()
