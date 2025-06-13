import webbrowser

# Open a website in the default browser
webbrowser.open('https://www.python.org')

# Open a website in a new tab
webbrowser.open_new_tab('https://www.github.com')

# Open a website in a new window
webbrowser.open_new('https://www.wikipedia.org')

# List available browsers (may not work on all OS)
print("Available browsers:")
for name in webbrowser._browsers:
    print("-", name)
# Open a website with a specific browser (if installed)
try:
    Safari = webbrowser.get('safari')
    Safari.open('https://www.stackoverflow.com')
except webbrowser.Error:
    print("Safari browser not found.")