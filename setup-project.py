import argparse
import subprocess
import os

parser = argparse.ArgumentParser(
    description="This sets up the project including setting up the ciprs-reader project as a prerequisite."
)
parser.add_argument(
    "ciprs_reader_path",
    help="The path to the base directory of the ciprs-reader project, which can be found on the Code For Durham GitHub",
)
parser.add_argument(
    "dear_petition_path",
    nargs="?",
    default=".",
    help="The path to the base directory of the dear-petition project, in case you are running the script from a different directory.",  # noqa
)

args = parser.parse_args()
ciprs_reader = args.ciprs_reader_path
ciprs_reader_setup = ciprs_reader + "/setup.py"
dear_petition = args.dear_petition_path
dear_petition_setup = dear_petition + "/setup.py"

os.chdir(dear_petition)
subprocess.call(["python", "setup.py", "install"])
os.chdir(ciprs_reader)
subprocess.call(["python", "setup.py", "install"])
