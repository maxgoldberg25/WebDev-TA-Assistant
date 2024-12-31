import os
import webbrowser

def open_html_files(directory):
    # Get a list of all HTML files in the specified directory
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    
    if not html_files:
        print("No HTML files found in the specified directory.")
        return
    
    for html_file in html_files:
        # Create the full path to the file
        file_path = os.path.join(directory, html_file)
        
        # Open the HTML file in the default web browser
        print(f"Opening: {html_file}")
        webbrowser.open(f"file://{file_path}")
        
        # Wait for user input to proceed
        input("Press Enter to close and open the next file...")
    
    print("All files have been opened.")

# Specify the directory containing the HTML files
html_directory = input("Enter the path to the directory with HTML files: ").strip()
if os.path.isdir(html_directory):
    open_html_files(html_directory)
else:
    print("The specified path is not a directory.")