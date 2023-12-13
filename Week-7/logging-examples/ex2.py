import logging
import sys

# Logging level set to WARNING, so any message of level WARNING or higher will
# be displayed 
logging.basicConfig(level=logging.WARNING, format="%(levelname)s - %(message)s")

num1, num2 = int(sys.argv[1]), int(sys.argv[2])

if num2 > 0:
    logging.debug(f"Division {num1}/{num2} is possible")
else:
    logging.critical("FATAL\nDivision by zero is not possible")
