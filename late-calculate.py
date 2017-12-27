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

csv.field_size_limit(sys.maxsize)

if len(sys.argv) < 3:
  print ('Usage: late-calculate.py output_worksheet.csv reference_worksheet assignements_worksheet.csv*')
  sys.exit(1)
output_worksheet = sys.argv[1]
reference_worksheet = sys.argv[2]
grading_worksheets = sys.argv[3:]
print ('Output worksheet : "' + output_worksheet + '"')
files = {}
for assignment in grading_worksheets:
  if not os.path.isfile(assignment):
    print ('ERROR: {} is not a valid file!'.format(assignment))
    sys.exit(3)

def get_fieldnames(file):
  return csv.DictReader(open(file, 'rt'),
                        delimiter=',', quotechar='"').fieldnames

def setup_output_writer(output_worksheet, grading_worksheets):
  header_list = ['First name', 'Last name','Email address']#get_fieldnames(grading_worksheets[0])
  for grading_worksheet in grading_worksheets:
    header_list.append(grading_worksheet + "_Late_Days")
    header_list.append(grading_worksheet + "_Grade")
  # print(header_list)
  header_list.append('Total Late Days')
  writer = csv.DictWriter(open(output_worksheet, 'wt'),
                        delimiter = ',',
                        quotechar = '"',
                        fieldnames = header_list)
  writer.writeheader()
  return writer

def setup_input_readers(grading_worksheets):
  readers = {}
  for grading_worksheet in grading_worksheets:
    files[grading_worksheet] = open(grading_worksheet, 'rt')
    readers[grading_worksheet] = csv.DictReader(files[grading_worksheet],
      delimiter=',',quotechar='"')
  return readers

def parse_status(status):
  if "No submission" in status:
    return 0
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
    leniency_amount = 20 / 24 / 60
    return int(math.ceil(days_used - leniency_amount))
  else:
    return 0

def get_student_score(readers, student_email):
  student_late_days = {}
  student_grades = {}
  for grading_worksheet in grading_worksheets:
    student_late_days[grading_worksheet+"_Late_Days"] = ""
    for row in readers[grading_worksheet]:
      if row['Email address'] == student_email:
        student_late_days[grading_worksheet+"_Late_Days"] = parse_status(row['Status'])
        student_grades[grading_worksheet + "_Grade"] = row['Grade']
        break
    files[grading_worksheet].seek(0)
  return student_late_days, student_grades

writer = setup_output_writer(output_worksheet, grading_worksheets)
readers = setup_input_readers(grading_worksheets)
late_days_used = {}
student_grades = {}
reference_file = open(reference_worksheet,'rt')
reference_reader = csv.DictReader(reference_file,
  delimiter=',',quotechar='"') 
first_names = {}
last_names = {}
for row in reference_reader:
  first_names[row['Email address']] = row['First name']
  last_names[row['Email address']] = row['Last name']
  late_days_used[row['Email address']] , \
  student_grades[row['Email address']]= get_student_score(readers, row['Email address'])
reference_file.seek(0);
for ref_row in reference_reader:
  if ref_row['Email address'] == 'Email address':
    continue  
  student_email = ref_row['Email address']
  student_late_days = late_days_used[student_email]
  row = {}
  row['First name'] = first_names[student_email]
  row['Last name'] = last_names[student_email]
  row['Total Late Days'] = 0
  row['Email address'] = student_email
  for assignment, grade in student_grades[student_email].items(): 
    row[assignment] = grade
  for assignment, late_day in student_late_days.items():
    row[assignment] = late_day
    row['Total Late Days'] = row['Total Late Days'] + late_day
  writer.writerow(row)