import os
import time

#choose only files from provided path which were modified < days
def abiquo_log_filter(path, days):
    now = time.time()
    file_list = [os.path.join(path,i) for i in os.listdir(path)]
    collect_list = []
    for i in file_list:
      modification_time = os.path.getmtime(i)
      if (now - modification_time) // (24*3600) < days:
        collect_list.append(i)
    return collect_list
