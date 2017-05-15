#!/usr/bin/evn python

import os
import glob
import sys
import json
import optparse


TOTALS_FILE = "totals.json"
EXECUTIONS_FILE = "executions.json"
# ./beta_project/job/1d46f2ee-dc6e-402c-8211-8570d86c52c3/logs/8.state.json or 8.rdlog
JOBS_PATTERN = "{LOGS}/*/*/*/*/*{SUFFIX}"
# ./beta_project/run/logs/13.state.json or 13.rdlog
RUNS_PATTERN = "{LOGS}/*/*/*/*{SUFFIX}"
USERS = []
EXEC_PER_DAY = {}
TOTALS = {"TOTAL": 0,
          "SUCCEEDED": 0,
          "FAILED": 0,
          "UNIQUE_USERS": 0
         }


def get_log_files(glob_pattern):
    return glob.glob(glob_pattern)


def calculate_executions(glob_pattern):
    for exec_file in get_log_files(glob_pattern):
        with open(exec_file) as ef:
            efj = json.load(ef)
        day = efj["startTime"].split("T")[0]
        if day not in EXEC_PER_DAY:
            EXEC_PER_DAY[day] = {"SUCCEEDED": 0, "FAILED": 0}
        if efj["executionState"] == "SUCCEEDED":
            TOTALS["SUCCEEDED"] += 1
            EXEC_PER_DAY[day]["SUCCEEDED"] += 1
        elif efj["executionState"] == "FAILED":
            TOTALS["FAILED"] += 1
            EXEC_PER_DAY[day]["FAILED"] += 1
        TOTALS["TOTAL"] += 1


def _update_users(log_line):
    # example line: "^2017-05-14T18:11:42Z|stepbegin||{node=localhost|step=1|stepctx=1|user=admin}|^"
    user = log_line.split("|")[-2].strip("}").split("=")[1]
    if user not in USERS:
        USERS.append(user)


def calculate_unique_users(glob_pattern):
    for rdlog_file in get_log_files(glob_pattern):
        with open(rdlog_file) as rdlf:
            for line_n,text in enumerate(rdlf):
                if line_n == 1:
                    _update_users(text)
                    break
        TOTALS["UNIQUE_USERS"] = len(USERS)


def normalize_executions():
   return [{"Day":day, "Succeeded": executions["SUCCEEDED"], "Failed": executions["FAILED"]} for day,executions in EXEC_PER_DAY.iteritems()]


def main():
    optparser = optparse.OptionParser()
    optparser.add_option("-l",
                         "--logs-path",
                         action="store",
                         dest="LOGS_PATH",
                        help="Rundeck logs directory",
                        default="/var/lib/rundeck/logs/rundeck")
    opt, args = optparser.parse_args()

    if not os.path.exists(opt.LOGS_PATH):
        print "{PATH} not found. Script will exit.".format(PATH=opt.LOGS_PATH)
        sys.exit(1)

    LOGS_PATH = opt.LOGS_PATH

    calculate_executions(RUNS_PATTERN.format(LOGS=LOGS_PATH,SUFFIX=".json"))
    calculate_executions(JOBS_PATTERN.format(LOGS=LOGS_PATH,SUFFIX=".json"))
    calculate_unique_users(RUNS_PATTERN.format(LOGS=LOGS_PATH,SUFFIX=".rdlog"))
    calculate_unique_users(JOBS_PATTERN.format(LOGS=LOGS_PATH,SUFFIX=".rdlog"))
    EXECUTIONS_NORMALIZED = normalize_executions()
    with open(TOTALS_FILE, 'w') as tf:
        json.dump(TOTALS, tf)
    with open(EXECUTIONS_FILE,'w') as ef:
        json.dump(EXECUTIONS_NORMALIZED, ef)


if __name__ == "__main__":
    main()
