import re

file_path = r'frontend\templates\student-dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix single quotes around ${API_BASE_URL} to backticks
# Pattern: '${API_BASE_URL}/...'  ->  `${API_BASE_URL}/...`
content = re.sub(r"'(\$\{API_BASE_URL\}/[^']+)'", r'`\1`', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed API URLs in student-dashboard.html!")
print("Changed single quotes to backticks for template literals")
