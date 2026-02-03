import sys
import os

print(f"CWD: {os.getcwd()}")
sys.path.append(os.path.join(os.getcwd(), 'backend'))
import app.services.whatsapp as w
print(f"Module file: {w.__file__}")
