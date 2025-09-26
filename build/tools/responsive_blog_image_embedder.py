#!/usr/bin/env python3
"""
Responsive Base64 Image Embedder for My Website Blog
Generates device-responsive image tags with CSS styling
Based on your original script with responsive enhancements
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import base64
import sys
import pyperclip
import os

def get_file_size_mb(file_path):
    """Get file size in MB"""
    return os.path.getsize(file_path) / (1024 * 1024)

def create_responsive_img_tag(encoded_string, mime_type, size_option="responsive", alt_text="Blog image"):
    """Create responsive image tag with CSS styling options"""
    
    base_styles = 'max-width: 100%; height: auto; display: block; margin: 1rem auto;'
    
    size_options = {
        "responsive": {
            "style": base_styles,
            "description": "Full responsive - adapts to container width"
        },
        "mobile-first": {
            "style": base_styles + " width: 90vw; max-width: 600px;",
            "description": "Mobile-optimized with max 600px on desktop"
        },
        "desktop-first": {
            "style": base_styles + " width: 80%; max-width: 800px;",
            "description": "Desktop-focused with 80% width, max 800px"
        },
        "screenshot": {
            "style": base_styles + " width: 95%; max-width: 1000px; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);",
            "description": "Perfect for screenshots with border and shadow"
        },
        "small-diagram": {
            "style": base_styles + " width: 60%; max-width: 500px;",
            "description": "Smaller sizing for diagrams and icons"
        },
        "full-width": {
            "style": base_styles + " width: 100%;",
            "description": "Full container width (careful with large images)"
        }
    }
    
    selected_style = size_options.get(size_option, size_options["responsive"])["style"]
    
    return f'<img src="data:image/{mime_type};base64,{encoded_string}" alt="{alt_text}" style="{selected_style}">'

def show_size_selection_dialog():
    """Show dialog to select image sizing option"""
    
    # Create selection window
    selection_window = tk.Toplevel()
    selection_window.title("Choose Image Display Size")
    selection_window.geometry("500x400")
    selection_window.resizable(False, False)
    
    # Center the window
    selection_window.transient()
    selection_window.grab_set()
    
    selected_option = tk.StringVar(value="responsive")
    
    # Title
    title_label = tk.Label(selection_window, text="Select Image Display Style:", 
                          font=("Arial", 12, "bold"))
    title_label.pack(pady=(10, 20))
    
    # Size options with descriptions
    size_options = {
        "responsive": "📱💻 Full Responsive - Adapts to any screen size",
        "mobile-first": "📱 Mobile-First - Optimized for mobile, max 600px desktop", 
        "desktop-first": "💻 Desktop-First - 80% width, max 800px",
        "screenshot": "🖼️  Screenshot Style - Border, shadow, max 1000px",
        "small-diagram": "📊 Small Diagram - 60% width, max 500px", 
        "full-width": "📐 Full Width - Uses complete container width"
    }
    
    # Radio buttons for each option
    for option, description in size_options.items():
        radio = tk.Radiobutton(selection_window, 
                              text=description,
                              variable=selected_option,
                              value=option,
                              wraplength=450,
                              justify=tk.LEFT,
                              font=("Arial", 10),
                              pady=5)
        radio.pack(anchor=tk.W, padx=20, pady=2)
    
    # Alt text input
    alt_frame = tk.Frame(selection_window)
    alt_frame.pack(pady=(20, 10), padx=20, fill=tk.X)
    
    tk.Label(alt_frame, text="Alt Text (for accessibility):", font=("Arial", 10)).pack(anchor=tk.W)
    alt_entry = tk.Entry(alt_frame, font=("Arial", 10))
    alt_entry.insert(0, "Blog image")
    alt_entry.pack(fill=tk.X, pady=(5, 0))
    
    # Buttons
    button_frame = tk.Frame(selection_window)
    button_frame.pack(pady=20)
    
    result = {"option": None, "alt_text": "Blog image"}
    
    def on_ok():
        result["option"] = selected_option.get()
        result["alt_text"] = alt_entry.get() or "Blog image"
        selection_window.destroy()
    
    def on_cancel():
        result["option"] = None
        selection_window.destroy()
    
    tk.Button(button_frame, text="Generate Image Tag", command=on_ok, 
             bg="#3498db", fg="white", font=("Arial", 10, "bold"),
             padx=20, pady=5).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame, text="Cancel", command=on_cancel,
             font=("Arial", 10), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
    
    # Wait for user interaction
    selection_window.wait_window()
    
    return result["option"], result["alt_text"]

def main():
    # Create main GUI
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()

    # Select image file
    file_path = filedialog.askopenfilename(
        title="Select image for responsive blog embedding",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.gif *.webp"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("GIF files", "*.gif"),
            ("WebP files", "*.webp"),
            ("All files", "*.*")
        ]
    )
    
    if not file_path:
        print("No file selected, exiting.")
        return

    # Determine file extension and MIME type
    extension_map = {
        '.jpg': 'jpeg',
        '.jpeg': 'jpeg', 
        '.png': 'png',
        '.gif': 'gif',
        '.webp': 'webp'
    }
    
    file_ext = os.path.splitext(file_path.lower())[1]
    
    if file_ext not in extension_map:
        messagebox.showerror("Error", f"Unsupported image type: {file_ext}")
        print(f"❌ Unsupported image type: {file_ext}")
        return
    
    mime_type = extension_map[file_ext]
    
    # Check file size and warn if large
    file_size = get_file_size_mb(file_path)
    if file_size > 1.0:  # Warn if > 1MB
        result = messagebox.askyesno(
            "Large File Warning", 
            f"File size: {file_size:.2f}MB\n\n"
            "Large embedded images increase repository size and page load time.\n"
            "Consider:\n"
            "• Compressing the image first\n"
            "• Using /images/ folder for files > 1MB\n"
            "• Using external image hosting\n\n"
            "Continue with base64 embedding?"
        )
        if not result:
            print("❌ Cancelled due to large file size.")
            return

    # Show size selection dialog
    size_option, alt_text = show_size_selection_dialog()
    
    if not size_option:
        print("❌ Cancelled by user.")
        return

    # Encode image
    try:
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
        # Create responsive HTML tag
        html_tag = create_responsive_img_tag(encoded_string, mime_type, size_option, alt_text)
        
        # Copy to clipboard
        pyperclip.copy(html_tag)
        
        # Show success message
        filename = os.path.basename(file_path)
        print(f"✅ Responsive image tag for '{filename}' copied to clipboard!")
        print(f"📊 File size: {file_size:.2f}MB")
        print(f"🎨 Style: {size_option}")
        print(f"🏷️  Alt text: {alt_text}")
        print(f"📱💻 Ready to paste into your markdown blog post")
        
        # Show CSS info
        print(f"\n📋 Features included:")
        print(f"   • Responsive sizing for mobile/desktop")
        print(f"   • Accessibility alt text")
        print(f"   • Auto-centering and margins")
        print(f"   • Maintains aspect ratio")
        
        if size_option == "screenshot":
            print(f"   • Border and shadow styling")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process image: {str(e)}")
        print(f"❌ Error processing image: {str(e)}")

    # Clean up
    root.destroy()

if __name__ == "__main__":
    print("🚀 Responsive Blog Image Embedder for My Website Blog")
    print("📱💻 Generates device-adaptive HTML image tags\n")
    main()