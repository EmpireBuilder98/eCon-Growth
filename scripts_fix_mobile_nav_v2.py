import os
import re

def fix_mobile_nav():
    repo_dir = '/home/ubuntu/econ-growth'
    html_files = [f for f in os.listdir(repo_dir) if f.endswith('.html')]
    
    for filename in html_files:
        path = os.path.join(repo_dir, filename)
        with open(path, 'r') as f:
            content = f.read()
            
        # 1. Update CSS to hide the CTA button on mobile (max-width: 900px)
        # Look for the @media(max-width:900px) block
        if '@media(max-width:900px)' in content:
            # Check if .nav-actions .nav-cta is already hidden
            if '.nav-actions .nav-cta{display:none}' not in content:
                # Add it to the existing media query
                content = content.replace('@media(max-width:900px){', '@media(max-width:900px){.nav-actions .nav-cta{display:none};')
        
        # 2. Ensure the mobile menu script includes the CTA button
        # The script I added earlier should already be doing this, but let's make sure.
        # The script is usually at the end of the body.
        
        # Let's check the script block
        script_pattern = re.compile(r'// Mobile Menu Logic.*?const navToggle = document\.getElementById\(\'navToggle\'\);', re.DOTALL)
        if script_pattern.search(content):
            # The script is present. Let's ensure it adds the CTA button.
            if 'const ctaBtn = document.querySelector(\'.nav-actions .nav-cta\');' not in content:
                # Update the script to include the CTA button in the mobile menu
                new_script_logic = """
    // Mobile Menu Logic
    const navToggle = document.getElementById('navToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
    const mobileMenuLinks = document.getElementById('mobileMenuLinks');
    const navLinks = document.querySelectorAll('.nav-links a');
    const ctaBtn = document.querySelector('.nav-actions .nav-cta');

    if (navToggle && mobileMenu && mobileMenuLinks) {
        // Populate mobile menu
        mobileMenuLinks.innerHTML = '';
        navLinks.forEach(link => {
            const mobileLink = link.cloneNode(true);
            mobileMenuLinks.appendChild(mobileLink);
        });
        
        // Add CTA button to mobile menu
        if (ctaBtn) {
            const mobileCta = ctaBtn.cloneNode(true);
            mobileCta.classList.add('mobile-menu-cta');
            mobileMenuLinks.appendChild(mobileCta);
        }

        navToggle.addEventListener('click', () => {
            const isOpened = navToggle.getAttribute('aria-expanded') === 'true';
            navToggle.setAttribute('aria-expanded', !isOpened);
            document.body.classList.toggle('body-menu-open');
        });

        mobileMenuOverlay.addEventListener('click', () => {
            navToggle.setAttribute('aria-expanded', 'false');
            document.body.classList.remove('body-menu-open');
        });
    }
"""
                # Replace the old logic with the new one
                content = re.sub(r'// Mobile Menu Logic.*?mobileMenuOverlay\.addEventListener\(\'click\', \(\) => \{.*?\}\);', new_script_logic, content, flags=re.DOTALL)

        with open(path, 'w') as f:
            f.write(content)
            
    print("Mobile navigation fix applied to all HTML files.")

if __name__ == "__main__":
    fix_mobile_nav()
