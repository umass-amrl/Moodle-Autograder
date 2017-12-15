#!/usr/bin/python3

# Copyright 2017 Kyle Veddder (kvedder@umass.edu)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
import glob
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
import time
import math
from functools import reduce

if len(sys.argv) < 3:
  print ('Usage: late-calculate.py output_worksheet.csv assignements_worksheet.csv*')
  sys.exit(1)
output_worksheet = sys.argv[1]
grading_worksheets = sys.argv[2:]
print ('Output worksheet : "' + output_worksheet + '"')

for assignment in grading_worksheets:
  if not os.path.isfile(assignment):
    print ('ERROR: {} is not a valid file!'.format(assignment))
    sys.exit(3)

def get_fieldnames(file):
  return csv.DictReader(open(file, 'rt'),
                        delimiter=',', quotechar='"').fieldnames

def setup_output_writer(output_worksheet, grading_worksheets):
  writer = csv.DictWriter(open(output_worksheet, 'wt'),
                        delimiter = ',',
                        quotechar = '"',
                        fieldnames = get_fieldnames(grading_worksheets[0]))
  writer.writeheader()
  return writer

def setup_input_readers(grading_worksheets):
  return [csv.DictReader(open(grading_worksheet, 'rt'), delimiter=',',
                         quotechar='"') for grading_worksheet in grading_worksheets]

def get_late_days(reader):
  raw_statuses = [row['Status'] for row in reader]
  def parse_status(status):
    if "No submission" in status:
      return ("No submission.", 0)
    elif "late" in status:
      late_string = status.split(" - ")[1]
      late_list = late_string.split(' ')[:-1]
      days_used = 0.0
      for i in range(int(len(late_list) / 2)):
        val = int(late_list[2 * i])
        modifier = late_list[2 * i + 1]
        if "day" in modifier:
          days_used += val
        elif "hour" in modifier:
          days_used += (val / 24)
        elif "mins" in modifier:
          days_used += (val / 24 / 60)
        elif "sec" in modifier:
          days_used += (val / 24 / 60 / 60)
      leniency_amount = 20 / 60 / 24
      return (("Handed in " + late_string + "!"), int(math.ceil(days_used - leniency_amount)))
    else:
      return ("Handed in on time!", 0)
  return [parse_status(status) for status in raw_statuses]

def merge_late_days(list_of_assignment_late_days):
  base_list = [[assignment] for assignment in list_of_assignment_late_days[0]]
  for assignment in list_of_assignment_late_days[1:]:
    for idx, grade in enumerate(assignment):
      base_list[idx].append(grade)
  return base_list

def calculate_late_sum(merged_student):
  # reduce(lambda total_days, assignment: total_days + assignment[1], merged_student, 0)
  days_used = 0
  days_used_list = []
  for assignment in merged_student:
    days_used += assignment[1]
    days_used_list.append(days_used)
  return [(assignment, total) for assignment, total in zip(merged_student, days_used_list)]

def generate_final_string(student):
  string_list = ["{} Late days used on this assignment: {}. Total late days used: {}\n".format(assignment[0][0], assignment[0][1], assignment[1]) for assignment in student]
  return reduce(lambda acc, s: acc + s, string_list, "")

writer = setup_output_writer(output_worksheet, grading_worksheets)
readers = setup_input_readers(grading_worksheets)
result_csv_format = setup_input_readers([grading_worksheets[0]])[0]

late_days = [get_late_days(reader) for reader in readers]
late_days_with_sum = [calculate_late_sum(student_late_days) for student_late_days in merge_late_days(late_days)]
final_strings = [generate_final_string(student) for student in late_days_with_sum]

for row, final_string in zip(result_csv_format, final_strings):
  row['Grade'] = 100
  row['Feedback comments'] = final_string
  writer.writerow(row)
