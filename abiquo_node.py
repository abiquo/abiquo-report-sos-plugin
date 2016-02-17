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


class abiquo_node(Plugin, RedHatPlugin):
    """Abiquo cloud node related information
    """

    def checkenabled(self):
        if self.cInfo["policy"].pkgByName("libvirt") and self.cInfo["policy"].pkgByName("abiquo-aim"):
            return True
        return False

    def setup(self):
        # libvirt logs
        self.add_copy_spec("/var/log/libvirt/")

        # aim conf
        self.add_copy_spec("/etc/abiquo-aim.ini")

        # libvirt conf
        self.add_copy_spec("/etc/libvirt/")

        self.add_cmd_output("virsh capabilities")
        self.add_cmd_output("virsh list --all")

        # History
        self.add_copy_spec("/root/.bash_history")
        
        return
