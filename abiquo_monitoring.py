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

from sos.plugins import Plugin, RedHatPlugin


class abiquo_monitoring(Plugin, RedHatPlugin):
    """Abiquo monitoring appliance related information
    """
    option_list = [
        ("full", "Get all the tomcat logs", "slow", True),
        ("days", "Number of days to collect", "slow",7),
        ("logsize", "max size (MiB) to collect per log file", "", 0),
    ]

    def checkenabled(self):
        if self.cInfo["policy"].pkgByName("abiquo-delorean") and self.cInfo["policy"].pkgByName("abiquo-emmett"):
            return True
        return False

    def setup(self):
        # emmett/delorean, cassandra, kairosdb logs
        if self.get_option("full"):
            self.add_copy_spec("/logs/", sizelimit=self.get_option("logsize"))
            self.add_copy_spec("/var/log/cassandra/", sizelimit=self.get_option("logsize"))
            self.add_copy_spec("/opt/kairosdb/log/", sizelimit=self.get_option("logsize"))
        else:
            self.add_copy_spec("/logs/*.log", sizelimit=self.get_option("logsize"))
            self.add_copy_spec("/var/log/cassandra/*.log", sizelimit=self.get_option("logsize"))
            self.add_copy_spec("/opt/kairosdb/log/*.log", sizelimit=self.get_option("logsize"))

        #conf files
        self.add_copy_spec([
            "/etc/abiquo/watchtower/",
            "/opt/kairosdb/conf/",
            "/etc/cassandra/conf/cassandra.yaml",
        ])
 
        # History
        self.add_copy_spec("/root/.bash_history")

        return
