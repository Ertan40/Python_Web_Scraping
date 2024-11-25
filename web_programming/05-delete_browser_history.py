import sqlite3
import shutil
import os
import re

source_path = r'C:\Users\ertan\AppData\Local\Google\Chrome\User Data\Default\History'

### just checked whether works due to "database is locked" error
# destination_path = r'C:\Users\ertan\AppData\Local\Temp\History_copy'
# shutil.copy2(source_path, destination_path)
# Connect to the copied database
# conn = sqlite3.connect(destination_path)

conn = sqlite3.connect(source_path)
cursor = conn.cursor()

# Execute the query
history_length = cursor.execute('SELECT count(1) FROM urls').fetchone()[0]
print('history length', history_length)

domain_pattern = re.compile(r"https?://([^/]+)/")
domains = {}
result = True
id = 0

while result:
    result = False
    ids = []
    for row in cursor.execute('''SELECT id, url, title FROM urls
                                 WHERE id > ?
                                 LIMIT 1000 
                              ''', (id,)):
        result = True
        match = domain_pattern.search(row[1])
        id = row[0]
        if match:
            domain = match.group(1)
            domains[domain] = domains.get(domain, 0) + 1
            if 'imgur' in domain:
                ids.append((id,))
    if ids:
        cursor.executemany('''DELETE FROM urls WHERE id=?''', ids)
        conn.commit()


conn.close()

# In order to remove the copied file after checked
# os.remove(destination_path)
