convert-lcmlog-path
===================

Look through the log, find all messages on the DRAKE_VIEWER_LOAD_ROBOT channel, and run a regex on all of the link_data.geom_data.string_data values contained in those messages. All other messages are untouched. The resulting data is written to a new lcmlog file [fout].
    
    usage: convert_lcmlog_path.py [-h] infile [outfile] pattern replace
