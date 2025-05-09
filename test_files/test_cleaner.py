# test_files/test_cleaner.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#from asthra_mailgaurd import cleaner
from asthra_mailguard.cleaner import clean_email

sample_email = """
    <html><body>
    Hello Avinash,<br><br>
    Your payment of $39.99 was successful. Click <a href="http://pay.example.com">here</a> for receipt.
    Regards,<br>
    Finance Team
    </body></html>
"""

cleaned = clean_email(sample_email)
print("CLEANED OUTPUT:\n", cleaned)
