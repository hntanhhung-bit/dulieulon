import os
import subprocess

out = subprocess.check_output(['tasklist', '/v', '/fo', 'csv'], text=True)
found = False
for line in out.strip().splitlines()[1:]:
    parts = [p.strip('"') for p in line.split('","')]
    if len(parts) > 8:
        pname, pid, title = parts[0], parts[1], parts[8]
        if any(k in title.lower() or k in pname.lower() for k in ['baocao', 'word', 'office', 'wps', 'winword']):
            print(f"Found: {pname} (PID: {pid}) - Title: {title}")
            found = True

if not found:
    print("No obvious GUI window found matching document name.")
