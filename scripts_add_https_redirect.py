import os

def add_https_redirect():
    redirect_script = """
<script>
if (window.location.protocol === 'http:' && !window.location.hostname.includes('localhost') && !window.location.hostname.includes('127.0.0.1')) {
    window.location.href = 'https:' + window.location.href.substring(window.location.protocol.length);
}
</script>
"""
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    content = f.read()
                
                if "window.location.protocol === 'http:'" not in content:
                    if "<head>" in content:
                        new_content = content.replace("<head>", "<head>" + redirect_script)
                        with open(path, "w") as f:
                            f.write(new_content)
                        print(f"Added HTTPS redirect to {path}")

if __name__ == "__main__":
    add_https_redirect()
