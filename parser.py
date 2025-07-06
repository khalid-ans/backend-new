import re

def extract_medicines(text):
    lines = text.split('\n')
    medicines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Common keywords for identifying medicine lines
        medicine_keywords = r'(TAB|CAP|SYR|INJ|Tablet|Cap|Syrup|tab|cap|mg|ml)'
        dosage_pattern = r'\d+-\d+-\d+'
        duration_pattern = r'\d+\\s*days?'

        # Match lines with medicine name and dosage/duration
        if re.search(medicine_keywords, line) and (re.search(dosage_pattern, line) or re.search(duration_pattern, line)):
            # Optionally clean out instruction language or non-ascii
            cleaned_line = re.sub(r'[^\x00-\x7F]+',' ', line)
            medicines.append(cleaned_line)

    return medicines

