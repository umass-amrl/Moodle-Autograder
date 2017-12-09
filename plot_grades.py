#! /usr/bin/env python3
import csv
import sys
import matplotlib.pyplot as plt


if len(sys.argv) < 4:
    print("Usage: plot_grades.py <output CSV file> <bin size> <max_grade>")
    exit(-1)

csvfile = open(sys.argv[1], 'rt')
bin_size = int(sys.argv[2])
max_grade = int(sys.argv[3])
reader = csv.reader(csvfile, delimiter=',', quotechar='"')
raw_data = [row for row in reader][1:]
grades = sorted([float(row[4]) for row in raw_data])
zeros_comments = [row[9] for row in raw_data if float(row[4]) <= 0]
zeros_comments = [comment.replace('\\n', '\n') for comment in zeros_comments]
for c in zeros_comments:
    print("==========================")
    print(c)
    print("==========================")
print("Grades: {}".format(grades))
print("Students with perfect scores: {}".format(len([g for g in grades if g >= max_grade])))
print("Students 100+: {}".format(len([g for g in grades if g >= 100])))
print("Students [90 to 100): {}".format(len([g for g in grades if g >= 90 and g < 100])))
print("Students [80 to 90): {}".format(len([g for g in grades if g >= 80 and g < 90])))
print("Students [70 to 80): {}".format(len([g for g in grades if g >= 70 and g < 80])))
print("Students [60 to 70): {}".format(len([g for g in grades if g >= 60 and g < 70])))
print("Students below 60: {}".format(len([g for g in grades if g < 60])))
print("Average score: {}".format(sum(grades) / len(grades)))
bins = [bin_size * x for x in range(int(max_grade / bin_size) + 1)]
plt.hist(grades, bins=bins , facecolor='red', alpha=0.75)
plt.xlabel('Grade')
plt.ylabel('Number of students')
plt.title('Histogram of students grades, bin size of {}, max grade of {}'.format(bin_size, str(max_grade)))
plt.grid(True)
plt.xlim([0, max_grade])
plt.show()
