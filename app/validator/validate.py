import os
from validator.log2prop import *
from validator.core.parser import PRISMResult

DEFAULT_PRISM_PATH = "prism"
PROP_EXTENSION = "prop"
RESULT_EXTENSION = "rlt"


def main(argv):
    prop_types = [prop.name.lower() for prop in PropertyType]
    try:
        opts, args = getopt.getopt(argv, "m:l:p:h", prop_types)
    except getopt.GetoptError:
        print(usage_string())
        sys.exit(2)

    log_path = None
    model_path = None
    prism_path = DEFAULT_PRISM_PATH
    prop_type = PropertyType.STRONG

    for opt, arg in opts:
        if opt == "-h":
            print(usage_string())
            sys.exit(1)
        elif opt == "-l":
            log_path = arg
        elif opt == "-m":
            model_path = arg
        elif opt == "-p":
            prism_path = arg
        elif opt[2:] in prop_types:
            prop_type = PropertyType(prop_types.index(opt[2:]))

    if model_path is None:
        print(usage_string())
        sys.exit(1)

    if model_path is None:
        print(usage_string())
        sys.exit(1)

    if log_path is None:
        print(usage_string())
        sys.exit(1)

    exit(validate(model_path, log_path, prism_path, prop_type))


def validate(model_path: str, log_path: str, prism_path: str, prop_type: PropertyType) -> int:
    name, ext = os.path.splitext(model_path)
    prop_path = "{}.{}".format(name, PROP_EXTENSION)
    result_path = "{}.{}".format(name, RESULT_EXTENSION)

    build_property(log_path, prop_path, prop_type)

    result = os.system("{} {} {} -exportresults {}".format(prism_path, model_path, prop_path, result_path))

    if result == 0:
        result = 1 - int(PRISMResult(result_path).success)

    if os.path.exists(prop_path):
        os.remove(prop_path)

    if os.path.exists(result_path):
        os.remove(result_path)

    return result


def usage_string() -> str:
    usage = "Usage: python taxi.py -m <model file path> -l <log file path> [-p <path to prism>] [--weak --strong] [-h]"
    usage = "{} \n\n -m\n Path to model file".format(usage)
    usage = "{} \n\n -s\n Path to log file".format(usage)
    usage = "{} \n\n -p\n Path to PRISM executable file".format(usage)
    usage = "{} \n\n --strong\n Force to use strong (EX) property generation (default)".format(usage)
    usage = "{} \n\n --weak\n Force to use weak (EF) property generation".format(usage)

    return usage

if __name__ == '__main__':
    main(sys.argv[1:])
