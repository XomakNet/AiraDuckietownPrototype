import sys
import getopt
from validator.core.parser import LogParser
from validator.core.properties import StrongPropertyCompiler, WeakPropertyCompiler
from enum import Enum


class PropertyType(Enum):
    STRONG = 0
    WEAK = 1


def main(argv):
    prop_types =  ['strong', 'weak']

    try:
        opts, args = getopt.getopt(argv, "l:p:h", prop_types)
    except getopt.GetoptError:
        print(usage_string())
        sys.exit(2)

    log_path = None
    prop_path = None
    prop_type = PropertyType.STRONG

    for opt, arg in opts:
        if opt == "-h":
            print(usage_string())
            sys.exit(1)
        elif opt == "-l":
            log_path = arg
        elif opt == "-p":
            prop_path = arg
        elif opt[2:] in prop_types:
            prop_type = PropertyType(prop_types.index(opt[2:]))

    if log_path is None:
        print(usage_string())
        sys.exit(1)

    if prop_path is None:
        print(usage_string())
        sys.exit(1)

    build_property(log_path, prop_path, prop_type)


def build_property(log_path: str, prop_path: str, prop_type: PropertyType):
    parser = LogParser(path=log_path)

    if prop_type == PropertyType.STRONG:
        compiler = StrongPropertyCompiler(parser.log_specification)
    else:
        compiler = WeakPropertyCompiler(parser.log_specification)

    expr_builder = compiler.compile()
    with open(prop_path, "w") as out_file:
        out_file.writelines(expr_builder.build())


def usage_string() -> str:
    usage = "Usage: python log2prop.py -l <log file path> -p <output path> [--weak --strong] [-h]"
    usage = "{} \n\n -h\n Optional flag that prints usage of the script".format(usage)
    usage = "{} \n\n -l\n Path to log file".format(usage)
    usage = "{} \n\n -p\n Path to result property file".format(usage)
    usage = "{} \n\n --strong\n Force to use strong (EX) property generation (default)".format(usage)
    usage = "{} \n\n --weak\n Force to use weak (EF) property generation".format(usage)

    return usage

if __name__ == '__main__':
    main(sys.argv[1:])
