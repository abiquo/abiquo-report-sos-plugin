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


class abiquo_xen_node(Plugin, RedHatPlugin):
    """Abiquo xen node related information
    """

    def checkenabled(self):
        if self.is_installed("abiquo-aim") and self.is_installed("xen"):
           return True
        return False

    def setup(self):
        if self.checkenabled():
            # Xen log
            self.add_copy_spec("/var/log/xen/")

            #Xen conf
            self.add_copy_spec("/etc/xen/")

        return
