import os, re, sys, optparse, multifile
from error import Error




def process_file(file, command, file_transform, opts):
    if not os.path.isfile(file):
        raise Error("file not found: %s" % file)
    if opts.output and os.path.isdir(opts.output):
        outfile = os.path.join(opts.output, file_transform(os.path.basename(file)))
    elif opts.output:
        outfile = opts.output
    else:
        outfile = file_transform(file)
    command(file, outfile, opts)

def process_dir(dir, command, file_filter, file_transform, opts):
    for file in os.listdir(dir):
        if file_filter(file):
            process_file(os.path.join(dir,file), command, file_transform, opts)

def create_parser(doc):
    parser = optparse.OptionParser(doc)
    parser.add_option("-o", "--output",
                      help="name of output file, or directory",
                      dest="output", type="string")
    parser.add_option("-q", '--quiet',
                      help='supress normal progress message(s)',
                      dest='quiet', default=False, action='store_true')
    return parser

def main(parser, command, file_filter, file_transform, args, opts):
    # if we don't have at least one arg, error
    if len(args) < 1:
        parser.print_help()
        sys.exit(-1)

    # if there's only one arg, it might be a file or a dir
    if len(args) == 1:
        arg = args[0]
        if os.path.isdir(arg):
           process_dir(arg, command, file_filter, file_transform, opts)
        else:
            process_file(arg, command, file_transform, opts)
    # we have multiple args
    else:
        # deal with --output option
        if opts.output:
            if os.path.isdir(opts.output):
                outdir = opts.output
            else:
                raise Error(("%s is not a directory, or does not exist (with directory arg, "
                                 + "or multiple args, -o/--output must be a directory)") % opts.output)
        # loop over each file arg
        for file in args:
            process_file(file, command, file_transform, opts)
