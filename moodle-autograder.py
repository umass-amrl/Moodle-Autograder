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
import shutil
import subprocess
import sys
import tempfile
import zipfile

if len(sys.argv) < 3:
  print 'Usage: moodle-autograder grading_worksheet.csv submissions.zip [output_worksheet.csv]'
  sys.exit(1)
grading_worksheet = sys.argv[1]
submissions_zip = sys.argv[2]
output_worksheet = 'grades.csv'
if len(sys.argv) > 3:
  output_worksheet = sys.argv[3]
print 'Grading worksheet : "' + grading_worksheet + '"'
print 'Output worksheet : "' + output_worksheet + '"'
print '\n\n'

if not os.path.isfile(grading_worksheet):
  print 'ERROR: grader worksheet not a valid file!'
  sys.exit(2)

if not os.path.isfile(submissions_zip):
  print 'ERROR: submissions.zip is not a valid file!'
  sys.exit(3)

submissions_file = zipfile.ZipFile(submissions_zip, 'r')
temp_all_submissions = tempfile.mkdtemp()
submissions_file.extractall(temp_all_submissions)
submissions_file.close()

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
  identifier = (row['\xef\xbb\xbfIdentifier'])[-7:]
  # print "Identifier: " + identifier
  path_query = os.path.join(temp_all_submissions, '*' + identifier + '*')
  # print path_query
  submissions = glob.glob(path_query)
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
  submission_folder = submission.replace(temp_all_submissions,"")
  # print submission_folder

  # Set up test directory.
  temp_submission = tempfile.mkdtemp()
  shutil.copy('grader.sh', temp_submission + '/grader.sh');
  shutil.copytree(submission, temp_submission + '/' + submission_folder);

  # Assign grade here.
  try:
    grader_process = subprocess.Popen(['./grader.sh', row['Email address']], cwd=temp_submission)
    grader_process.wait()
    # Expects that a file named score.txt will be created in the temp
    # directory.
    f = open(temp_submission + '/score.txt', 'r')
    grade = float(f.read());
    f.close()
    f = open(temp_submission + '/feedback.txt', 'r')
    feedback = f.read();
    f.close()
  except Exception as e:
    print "Exception occurred: " + str(e)
    grade = 0
    feedback = "Failed to open grader. This is probably an infrastructure issue."

  # Cleanup.
  shutil.rmtree(temp_submission)
  print "Grade: ", grade
  row['Grade'] = grade
  row['Feedback comments'] = feedback
  writer.writerow(row)

shutil.rmtree(temp_all_submissions)
grader_input.close()
grader_output.close()
