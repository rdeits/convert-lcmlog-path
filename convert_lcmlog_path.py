import struct
import argparse
import re

from drake import lcmt_viewer_load_robot

def replace_goem_string(msg, pattern, replace):
    for link_data in msg.link:
        for geom_data in link_data.geom:
            s = geom_data.string_data
            if s:
                geom_data.string_data = re.sub(pattern, replace, s)
    return msg

def rewrite_lcmlog_geom_string(fin, fout, pattern, replace):
    while True:
        header_bytes = fin.read(28)
        if len(header_bytes) < 28:
            break
        sync, evno, tstamp, clen, dlen = struct.unpack('>LqqLL', header_bytes)
        chan = fin.read(clen)
        data = fin.read(dlen)
        if str(chan) == 'DRAKE_VIEWER_LOAD_ROBOT':
            msg = lcmt_viewer_load_robot.decode(data)
            msg = replace_goem_string(msg, pattern, replace)
            data = msg.encode()
            dlen = len(data)
            header_bytes = struct.pack('>LqqLL', sync, evno, tstamp, clen, dlen)

        fout.write(header_bytes)
        fout.write(chan)
        fout.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rewrite an LCM log with all references to mesh files updated to point to a different directory')
    parser.add_argument('infile', type=str, help='the input LCM log filename')
    parser.add_argument('outfile', type=str, nargs='?', default='out.lcm', help='the output LCM log filename')
    parser.add_argument('pattern', type=str, help='the pattern to be replaced (regex is supported)')
    parser.add_argument('replace', type=str, help='the string to replace all occurrences of [pattern] with')
    args = parser.parse_args()
    with open(args.infile, 'rb') as fin:
        with open(args.outfile, 'wb') as fout:
            rewrite_lcmlog_geom_string(fin, fout, args.pattern, args.replace)

