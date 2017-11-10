from abiquo_log_time import abiquo_log_filter
from sos.plugins import Plugin, RedHatPlugin

class abiquo_cloud_node(Plugin, RedHatPlugin):
    """Abiquo remote service related information
    """

    option_list = [
        ("full", "Get all the tomcat logs", "slow", True),
        ("days", "Number of days to collect", "slow", 7),
        ("logsize", "max size (MiB) to collect per log file", "", 0),
    ]
 
    def checkenabled(self):
        if self.cInfo["policy"].pkgByName("abiquo-public-cloud") and not self.cInfo["policy"].pkgByName("abiquo-server"):
            return True
        return False

    def setup(self):
        #tomcat logs, default 7 days
        filestocollect = abiquo_log_filter("/opt/abiquo/tomcat/logs/", self.get_option("days"))
        if self.get_option("full"):
           for a in filestocollect:
               self.add_copy_spec(a, sizelimit=self.get_option("logsize"))
        else:
            self.add_copy_spec("/opt/abiquo/tomcat/logs/*.log", sizelimit=self.get_option("logsize"))
            self.add_copy_spec("/opt/abiquo/tomcat/logs/*.out", sizelimit=self.get_option("logsize"))

        #conf files
        self.add_copy_spec("/opt/abiquo/config/")
        self.add_copy_spec("/opt/abiquo/tomcat/conf/")

        # Abiquo remote service redis dump
        self.add_copy_spec("/var/lib/redis/dump.rdb")

        # History
        self.add_copy_spec("/root/.bash_history")
