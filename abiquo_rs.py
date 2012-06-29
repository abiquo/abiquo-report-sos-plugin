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

import sos.plugintools


class abiquo_rs(sos.plugintools.PluginBase):
    """Abiquo remote service related information
    """

    optionList = [("full", "Get all the tomcat logs", "slow", False),
                  ("logsize", "max size (MiB) to collect per log file", "", 0)]

    def checkenabled(self):
        if self.cInfo["policy"].pkgByName("abiquo-remote-services") and not self.cInfo["policy"].pkgByName("abiquo-server"):
            return True
        return False

    def setup(self):
        # tomcat log
        if self.isOptionEnabled("full"):
            self.addCopySpecLimit("/opt/abiquo/tomcat/logs/", sizelimit=self.isOptionEnabled("logsize"))
        else:
            self.addCopySpecLimit("/opt/abiquo/tomcat/logs/*.log", sizelimit=self.isOptionEnabled("logsize"))

        #conf files
        self.addCopySpec("/opt/abiquo/config/")
        self.addCopySpec("/opt/abiquo/tomcat/conf/")

        # Abiquo remote service redis dump
        self.addCopySpec("/var/lib/redis/dump.rdb")

        # Abiquo version
        self.addCopySpec("/etc/abiquo-installer")
        self.addCopySpec("/etc/abiquo-release")

        return
