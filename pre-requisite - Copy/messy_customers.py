"""
Reads the file
Strips whitespace from all fields
Normalizes names to Title Case
Cleans phone numbers → format +15551234567 (remove everything except digits and leading +)
Standardizes date to YYYY-MM-DD
Writes clean version to clean_customers.csv
Writes a separate invalid_rows.csv for any row missing email AND phone

"""
import csv
import re
from datetime import datetime

clean_rows = []
invalid_rows = []

def std_date(d):
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y", "%Y/%m/%d", "%m/%d/%y", "%m-%d-%y"):
        try:
            return datetime.strptime(d, fmt).strftime("%Y%-%m-%d")
        except ValueError:
            pass

with  open("messy_cust.csv", 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row = {k: v.strip() for k, v in row.items()}
        # Normalize name to Title Case
        row["name"] =   row["name"].title()

        #phone
        phone = row["phone"]

        if phone:
            keep_pls = phone.startswith('+')
            digits = "". join(ch for ch in phone if ch.isdigit())
            row["phone"] = ("+" if keep_pls else "") + digits
        else:
            row["phone"] = ""

        #date
        row["signup_date"] = std_date(row["signup_date"])

        if row["phone"] =="" and row["email"] =="":
            invalid_rows.append(row)
        else:
            clean_rows.append(row)

print(clean_rows)