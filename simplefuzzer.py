#! /usr/bin/env Python3

import requests
import logging

# Create logger (not neccessary but it's nice to have organized output)
# Logger will be created if this is the main file executed
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

# Create a log file handler
# Log file will show even more detailed statements that you don't want to see in STDOUT
handler = logging.FileHandler('fuzzer.log')
handler.setLevel(logging.DEBUG)

# Create a logging stream handler
# STDOUT will display INFO and ERROR messages
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)
logger.addHandler(console_handler)

# example log message
logger.info('starting fuzzer')

# open file containing list of sites
with open('sitelist.txt') as f:

    # interate over lines in file
    for line in f:

        # remove accidental whitespace
        site = line.strip()
        
        # fuzz site
        logger.info('fuzzing site: %s' % site)

        # read suffixes from file
        with open('suffixes.txt') as sf:
            for suffix in sf:
                suffix = suffix.strip()

                fuzz_result = requests.get(site+suffix)
                if fuzz_result.status_code == 200:
                    logger.info("Match! - %s" % fuzz_result.url)

                    with open('results.txt', 'a') as output:
                        output.write(site)
                        output.write('\n==============================\n')
                        output.write(fuzz_result.text)
                        output.write('\n\n')

                else:
                    logger.debug("Not found = %s" % fuzz_result.url)
