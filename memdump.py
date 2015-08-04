#!/usr/bin/python
# author: deadc0de6
# contact: https://github.com/deadc0de6
#
# read process memory and dump to file
#   vdso: kernel call handlers
#   lib*: the libs
#   stack: the stack
#   heap: the heap
#
# Copyright (C) 2014 deadc0de6
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

from docopt import docopt

USAGE = '''
Memory dumping

Usage:
  memdump.py <pid> [--region=<reg>] [--folder=<out>]

OPTIONS:
  --region=<reg>    region name to dump
                    [default: [stack],[heap]]

'''

VERSION = '0.1'

def dump_reg(opath, fmem, start, end):
  fmem.seek(start)
  try:
    data = fmem.read(end-start)
    fout = open(opath, 'wb')
    fout.write(data)
    fout.close()
  except:
    pass

def get_offset(line):
  memrng = line.split(' ')[0]
  start = int(memrng.split('-')[0], 16)
  end = int(memrng.split('-')[1], 16)
  return start, end

def dump(pid, regions):
  fmaps = open('/proc/%s/maps' % (pid), 'rb')
  fmem = open('/proc/%s/mem' % (pid), 'rb')
  for line in fmaps:
    line = ' '.join(line.rstrip().split())
    name = line.split(' ')[-1]
    if 'lib' in name or len(name) < 2:
      # don't care
      continue
    if name in regions:
      start, end = get_offset(line)
      opath = '%s.data' % (name.strip('[').strip(']'))
      print 'dumping \"%s\" from 0x%x to 0x%x (%u bytes) to %s' % (name,
        start, end, end-start, opath)
      dump_reg(opath, fmem, start, end)

  fmem.close()
  fmaps.close()

if __name__ == '__main__':
  args = docopt(USAGE, version=VERSION)
  pid = args['<pid>']
  regions = args['--region'].split(',')
  dump(pid, regions)

