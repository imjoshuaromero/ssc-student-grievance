import re

file_path = r'frontend\templates\admin-dashboard.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern 1: Simple GET requests without auth
# fetch('http://localhost:5000/api/...')  ->  fetch(`${API_BASE_URL}/...`, {headers:{'Authorization':`Bearer ${localStorage.getItem('token')}`}})
pattern1 = r"fetch\('http://localhost:5000/api/([\w/{}$]+)'\)"
replacement1 = r"fetch(`${API_BASE_URL}/\1`, {headers:{'Authorization':`Bearer ${localStorage.getItem('token')}`}})"

# Pattern 2: Template literal GET requests without auth  
# fetch(`http://localhost:5000/api/...`)  ->  fetch(`${API_BASE_URL}/...`, {headers:{'Authorization':`Bearer ${localStorage.getItem('token')}`}})
pattern2 = r"fetch\(`http://localhost:5000/api/([\w/{}$]+)`\)"
replacement2 = r"fetch(`${API_BASE_URL}/\1`, {headers:{'Authorization':`Bearer ${localStorage.getItem('token')}`}})"

# Pattern 3: Just URL replacements (for URLs that already have options objects)
# 'http://localhost:5000/api/...'  ->  `${API_BASE_URL}/...`
pattern3 = r"'http://localhost:5000/api/([\w/{}$]+)'"
replacement3 = r"`${API_BASE_URL}/\1`"

# Pattern 4: Template literal URLs
# `http://localhost:5000/api/...`  ->  `${API_BASE_URL}/...`
pattern4 = r"`http://localhost:5000/api/([\w/{}$]+)`"
replacement4 = r"`${API_BASE_URL}/\1`"

# Apply replacements
content = re.sub(pattern1, replacement1, content)
content = re.sub(pattern2, replacement2, content)
content = re.sub(pattern3, replacement3, content)
content = re.sub(pattern4, replacement4, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("API URLs fixed!")
print("Remaining hardcoded URLs:")
remaining = re.findall(r'http://localhost:5000/api', content)
print(f"Found {len(remaining)} remaining")
