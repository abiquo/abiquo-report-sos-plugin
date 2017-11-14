### This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

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
