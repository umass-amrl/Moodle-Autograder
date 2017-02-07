#!/usr/bin/python

# Copyright 2017 Joydeep Biswas (joydeepb@cs.umass.edu)
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
import sys

if len(sys.argv) < 2:
  print 'Usage: moodle-autograder grading_worksheet.csv [output_worksheet.csv]'
  sys.exit(1)
grading_worksheet = sys.argv[1]

output_worksheet = 'grades.csv'
if len(sys.argv) > 2:
  output_worksheet = sys.argv[2]
print 'Grading worksheet : "' + grading_worksheet + '"'
print 'Output worksheet : "' + output_worksheet + '"'
print '\n\n'

if not os.path.isfile(grading_worksheet):
  print 'ERROR: grader worksheet not a valid file!'
  sys.exit(2)

grader_output = open(output_worksheet, 'wb')
grader_input = open(grading_worksheet, 'rb')
reader = csv.DictReader(grader_input, delimiter=',', quotechar='"')
fieldnames = reader.fieldnames
writer = csv.DictWriter(grader_output, 
                       delimiter = ',', 
                       quotechar = '"', 
                       fieldnames = fieldnames)
writer.writeheader()

for row in reader:
  #print row
  identifier = (row['Identifier'])[-7:]
  # print identifier
  submissions = glob.glob('*' + identifier + '*')
  if len(submissions) == 0:
    print 'ERROR: ' + row['Full name'] + ' (' + row['Email address'] + \
        ') has no submission'
    continue
  elif len(submissions) > 1:
    print 'ERROR: ' + identifier + ' has multiple submissions' + \
        submissions
    continue
  submission = submissions[0]
  print submission
  
  # Assign grade here.
  grade = 42
  
  row['Grade'] = grade
  writer.writerow(row)
    

grader_input.close()
grader_output.close()
