# | Function Name | Num. of calls | Total Time (ms) | Average Time (ms) |
# |---------------------------------------------------------------------|
# | add_cubes | 1 | 0.812 | 0.812 |
# | get_cube_power | 2 | 0.440 | 0.220 |
from datetime import datetime
import sys
import os

def get_time(start_t, stop_t):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    start_time = datetime.strptime(start_t, date_format)
    stop_time = datetime.strptime(stop_t, date_format)
    time_dif = (stop_time - start_time).total_seconds() * 1000
    return time_dif

def print_report(storage_dict, appearance):
    len_func_name, len_num_calls, len_tot_time, len_avg_time = 15, 15, 17, 19
    max_len = 15 if len(max(appearance, key=len)) + 2 < 15 else len(max(appearance, key=len)) + 2
    report = [("|" + " Function Name".ljust(max_len, " ")) + "| Num. of calls | Total Time (ms) | Average Time (ms) |"]
    report.append("-" * len(report[0]))
    rep = report
    for met in appearance:
        temp_l = []
        temp_l.append(("| " + met).ljust(max_len, " ") + " ")
        temp_l.append("|" + str(storage_dict[met][0]).center(len_num_calls))
        temp_l.append("|" + str(round(storage_dict[met][2], 2)).center(len_tot_time))
        temp_l.append("|" + str(round(storage_dict[met][3], 2)).center(len_avg_time) + "|")
        rep.append("".join(temp_l))
    for l in rep:
        print(str(l))

def reporting():
    assert len(sys.argv) == 2, "Usage: python reporting.py FILENAME"
    filename = sys.argv[1]
    report_matrix = []
    with open(os.getcwd() + r"\\" + filename, "r") as log_file:
        for line in log_file:
            report_matrix.append(list(line.split(",")))
    storage_dict = {}   #Dict where keys are method names and values are a list
                        #First element is func num of calls, second is start time, third is tot. time, fourth is avg time
    appearance = []
    for l in report_matrix[1:]:
        if l != report_matrix[-1]:
            l[-1] = l[-1][:-1] #Delete \n of the last list element
        if not l[1] in storage_dict:
            storage_dict[l[1]] = [1, [], 0, 0]
            storage_dict[l[1]][1].append(l[-1])
            appearance.append(l[1])
        else:
            if l[2] == "stop":
                #storage_dict[l[1]][1] = get_time(str(storage_dict[l[1]][1]), l[-1], l[1])
                start = storage_dict[l[1]][1].pop()
                end = l[-1]
                diff = get_time(start, end)
                storage_dict[l[1]][2] += diff

                storage_dict[l[1]][3] = storage_dict[l[1]][2] / storage_dict[l[1]][0]
            else:
                storage_dict[l[1]][0] += 1
                storage_dict[l[1]][1].append(l[-1])
    print_report(storage_dict, appearance)

 #Call this function with: python reporting.py FILENAME

if __name__ == "__main__":
    reporting()