from optparse import OptionParser as Opt
import re
import sys
import time

GDOC_PATTERN = r"https://docs.google.com/document/d/(?P<DOC_ID>(\w|_|-|\d)+)(/\w*)?"
DOC_FORMATS = ["docx", "odt", "rtf", "pdf", "txt", "html"]
PPT_FORMATS = ["pptx", "pdf", "svg", "png", "jpg"]
DRW_FORMATS = ["pdf", "svg", "png", "jpg"]
GDOC_BASE_URL = "https://docs.google.com"
GDOC_DOC_BASE_URL = GDOC_BASE_URL + "/%s/d/%s/export?format=%s"

def get_gdoc_id(url):
    return re.match(GDOC_PATTERN, url).group('DOC_ID')

def get_download_link(g_id, d_format):
    if d_format in DOC_FORMATS:
        return GDOC_DOC_BASE_URL % ("document", g_id, d_format)
    elif d_format in PPT_FORMATS:
        return GDOC_DOC_BASE_URL % ("presentation", g_id, d_format)
    elif d_format in DRW_FORMATS:
        return GDOC_DOC_BASE_URL % ("drawings", g_id, d_format)
    else:
        return "%s/uc?id=%s&export=download" % (GDOC_BASE_URL, g_id)

def get_lines_from_file(file_path):
    arch = open(file_path.replace('\n',''))
    lines = arch.readlines()
    arch.close()
    return lines

def manage_parse_args(options, args):
    args = map(lambda x: x.replace('\n',''), args)
    #print options
    #print args
    if options['gen_id']:
        print get_gdoc_id(args[0])
    if not(options['t_format'] is None):
        g_id = get_gdoc_id(args[0])
        print get_download_link(g_id, options['t_format'])

#def main(sinput):
def main():
    # add pipe support
    # ##
    in_args = sys.argv[1:]
    parser = Opt(usage="Usage: %prog [options] arguments",
        version="%prog 1.0")
    parser.add_option("-g", "--get-id",
        action="store_true",
        dest="gen_id",
        default=False,
        help="Return the gdoc ID of url")
    parser.add_option("-f", "--from-file",
        dest="ifile",
        help="execute comands with specific flags from file")
    parser.add_option("-l", "--link",
        dest="t_format",
        default=None)
    parser.add_option("-p", "--pipe-enabled",
        action="store_true",
        default=False)
    (options_p, args) = parser.parse_args()
    options = eval(options_p.__str__())
    if options['pipe_enabled']:
        sinput = sys.stdin
        adpinput = map(lambda x: str(x) ,sinput)
        #sinput.close()
        #print "Input pipe: %s" % sinput
        a_input = adapt(adpinput)
        parse_in = in_args + a_input
        #print "Comand: %s" % parse_in
        (options_p, args) = parser.parse_args(parse_in)
        options = eval(options_p.__str__())
    if not(options['ifile'] is None):
        for parse_line in get_lines_from_file(options['ifile']):
            p_line = parse_line.split(' ')
            #print p_line
            op2, arg2 = parser.parse_args(p_line)
            execute_parse(op2, arg2)
    else:
        execute_parse(options_p, args)

def execute_parse(p_options, args):
    options = eval(p_options.__str__())
    manage_parse_args(options, args)

def adapt(lines):
    linput = []
    for line in lines:
        linput += line.split(' ')
    return linput

if __name__ == '__main__':
    #lines2 = []
    #while True:
    #    line = sys.stdin.readline()
    #    if not line:
    #        break
    #    else:
    #        lines2.append(line)
    #main(lines2)
    main()
