#!/usr/bin/env python3
"""
Simple Responsive Image Embedder - Enhanced version of your original script
Keeps the same workflow but adds responsive CSS styling
"""

import tkinter as tk
from tkinter import filedialog
import base64
import sys
import pyperclip

# Create GUI (same as your original)
root = tk.Tk()
root.withdraw()
root.clipboard_clear()

# Select file (same as your original)
file_path = filedialog.askopenfilename()

# Determine extension (enhanced to support more formats)
extension = ""
mime_type = ""

if file_path.endswith(('.jpg', '.jpeg')):
    extension = "jpeg"
    mime_type = "jpeg"
elif file_path.endswith('.png'):
    extension = "png" 
    mime_type = "png"
elif file_path.endswith('.gif'):
    extension = "gif"
    mime_type = "gif"
elif file_path.endswith('.webp'):
    extension = "webp"
    mime_type = "webp"
else:
    print("Incompatible image type, exiting!")
    sys.exit()

# Encode image (same as your original)
with open(file_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    
    # ENHANCED: Responsive image tag with CSS styling
    responsive_img_tag = f'''<img src="data:image/{mime_type};base64,{encoded_string.decode('utf-8')}" alt="Blog image" style="max-width: 100%; height: auto; display: block; margin: 1rem auto;">'''
    
    # Copy to clipboard
    pyperclip.copy(responsive_img_tag)
    
    print("✅ Responsive base64 encoded image tag copied to clipboard!")
    print("📱💻 Features: Auto-sizing for mobile/desktop, centered, maintains aspect ratio")