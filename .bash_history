python3 --version
sudo apt update
sudo apt install git curl python3-pip python3-venv -y
git --version
python3 --version
pip3 --version
python3.11 --version
sudo apt update
sudo apt install software-properties-common -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y
cat /etc/os-release
apt-cache policy python3.11
apt-cache search python3.11
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
apt-cache search python3.1
apt-cache search python3.12
apt-cache search python3.13
sudo apt install python3.11 python3.11-venv python3.11-dev python3.11-full -y
python3.11 --version
sudo apt install mariadb-server redis-server redis-tools build-essential gcc g++ make libffi-dev libssl-dev libjpeg-dev zlib1g-dev xvfb wkhtmltopdf curl git -y
sudo apt install mariadb-server redis-server redis-tools build-essential gcc g++ make libffi-dev libssl-dev libjpeg-dev zlib1g-dev curl git -y
mysql --version
redis-server --version
sudo apt install npm -y
sudo npm install -g yarn
yarn --version
python3.11 -m pip install --upgrade pip
python3.11 -m pip install frappe-bench
bench --version
echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
bench --version
mkdir -p ~/frappe
cd ~/frappe
bench init frappe-bench --frappe-branch version-15 --python python3.11
bench --version
~/.local/bin/bench --version
sudo service mariadb status
sudo service redis-server status
sudo mysql
mysql -u frappe -p
cd ~/frappe/frappe-bench
pwd
bench new-site crm.local
Set Administrator password:
history | tail -20
cd ~/frappe/frappe-bench
bench new-site crm.local
cd ~/frappe/frappe-bench
bench --site crm.local list-apps
cd ~/frappe/frappe-bench
cat sites/crm.local/site_config.json
sudo mysql
cd ~/frappe/frappe-bench
rm -rf sites/crm.local
ls sites
bench new-site crm.local
sudo mysql
mysql -u frappe -p
sudo mysql
mysql -u frappe -p
pwd
rm -rf sites/crm.local
bench new-site crm.local --db-root-username frappe
[200~sudo mysql~
sudo mysql
mysql -u frappe -p
sudo mysql
mysql -u frappe -p
cd ~/frappe/frappe-bench
rm -rf sites/crm.local
bench new-site crm.local --db-root-username frappe
bench --site crm.local list-apps
bench start
curl -H "Host: crm.local" http://127.0.0.1:8000/login
cd ~/frappe/frappe-bench
bench start
cd ~/frappe/frappe-bench
bench --site crm.local set-admin-password NewPassword123
bench --site crm.local set-admin-password admin123
Username: Administrator
Password: admin123
cd ~/frappe/frappe-bench
bench --site crm.local execute frappe.db.get_single_value --args "['System Settings','setup_complete']"
bench --site crm.local console
cd ~/frappe/frappe-bench
bench --site crm.local migrate
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
bench start
bench --site crm.local list-apps
cd ~/frappe/frappe-bench
ls apps
cd ~/frappe/frappe-bench
ls apps
bench version
cd ~
mkdir leadcrm_import
unzip /mnt/data/Leadscrm\(3\).zip -d leadcrm_import
ls apps
cd ~/frappe/frappe-bench
ls
ls apps
find ~ -name "*.zip"
ls /mnt/c/Users/acer/Downloads | grep -i Leads
find /mnt/c/Users/acer/Downloads -name "*.zip"
sudo apt install unzip -y
mkdir ~/leadcrm_import
unzip "/mnt/c/Users/acer/Downloads/Leadscrm(3).zip" -d ~/leadcrm_import
mkdir -p ~/leadcrm_import
unzip "/mnt/c/Users/acer/Downloads/Leadscrm.zip" -d ~/leadcrm_import
which unzip
/usr/bin/unzip
ls -lh "/mnt/c/Users/acer/Downloads/Leadscrm.zip"
which unzip
ls -lh "/mnt/c/Users/acer/Downloads/Leadscrm.zip"
mkdir -p ~/leadcrm_import
python3 - <<'PY'
import zipfile
zip_path = "/mnt/c/Users/acer/Downloads/Leadscrm.zip"
extract_path = "/home/acer/leadcrm_import"

with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_path)

print("Extracted to:", extract_path)
PY

ls ~/leadcrm_import
find ~/leadcrm_import -maxdepth 3 -type f | head -50
find ~/leadcrm_import/Leadscrm -maxdepth 2 -type d
find ~/leadcrm_import/Leadscrm/Leadscrm/Leads -maxdepth 2 -type d
find ~/leadcrm_import/Leadscrm/Leadscrm/Leads -name hooks.py
cat ~/leadcrm_import/Leadscrm/Leadscrm/Leads/leads_crm/pyproject.toml 2>/dev/null | head -20
cat ~/leadcrm_import/Leadscrm/Leadscrm/Leads/crm_pro/pyproject.toml 2>/dev/null | head -20
cat ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/pyproject.toml 2>/dev/null | head -20
cd ~/frappe/frappe-bench
bench get-app ~/leadcrm_import/Leadscrm/Leadscrm/Leads/crm_pro
ls ~/leadcrm_import/Leadscrm/Leadscrm/Leads/crm_pro
cd ~/frappe/frappe-bench
pip install -e ~/leadcrm_import/Leadscrm/Leadscrm/Leads/crm_pro
cd ~/leadcrm_import/Leadscrm/Leadscrm/Leads/crm_pro
find . -maxdepth 2 -type f | head -50
cat pyproject.toml
cd ~/leadcrm_import/Leadscrm/Leadscrm/Leads
find leads_crm -name "*.json" | grep doctype | head -30
find crm_pro -name "*.json" | grep doctype | head -30
find precision_crm -name "*.json" | grep doctype | head -30
find leads_crm -maxdepth 2 -type f | head -30
find precision_crm -maxdepth 2 -type f | head -30
cd ~/frappe/frappe-bench
pip install -e ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm
ln -s ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm apps/precision_crm
ls apps
bench --site crm.local install-app precision_crm
cd ~/frappe/frappe-bench
pwd
./env/bin/pip list | grep precision
cat ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/setup.py
cd ~/frappe/frappe-bench
./env/bin/pip list | grep precision
cd ~/frappe/frappe-bench
./env/bin/pip install -e ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm
./env/bin/python -c "import precision_crm; print(precision_crm.__file__)"
bench --site crm.local install-app precision_crm
cd ~/frappe/frappe-bench
cat sites/apps.txt
ls apps
cd ~/frappe/frappe-bench
cp -r ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm apps/
ls apps
cd ~/frappe/frappe-bench
./env/bin/pip install -e apps/precision_crm
echo "precision_crm" >> sites/apps.txt
cat sites/apps.txt
bench clear-cache
cd ~/frappe/frappe-bench
cat -n sites/apps.txt
printf "frappe\nprecision_crm\n" > sites/apps.txt
cat -n sites/apps.txt
ls apps
cd ~/frappe/frappe-bench
./env/bin/python -c "import frappe; print('frappe ok')"
./env/bin/python -c "import precision_crm; print('precision_crm ok')"
bench clear-cache
bench --site crm.local install-app precision_crm
create_custom_field({...})
cd ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm
cat precision_crm/install.py
sed -n '1,200p' ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
nano ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
from frappe.custom.doctype.custom_field.custom_field import create_custom_field
create_custom_field("User", {
})
cd ~/frappe/frappe-bench
bench start
nano ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
grep -n "create_custom_field" ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
nano ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
sed -n '1,30p' ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
cd ~/frappe/frappe-bench
bench --site crm.local install-app precision_crm
nano ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
cd ~/frappe/frappe-bench
bench --site crm.local console
bench --site crm.local install-app precision_crm
cd ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm
tree -L 2
find . -maxdepth 2 -type f
precision_crm.precision_crm
cat ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/modules.txt
head -40 ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/hooks.py
grep -n "app_name" ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/hooks.py
ls -la ~/frappe/frappe-bench/apps
app_name = "precision_crm"
cd ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm
cat precision_crm/modules.txt
ls precision_crm
cd ~/frappe/frappe-bench
cat sites/apps.txt
cat sites/crm.local/apps.txt
cd ~/frappe/frappe-bench
python -c "import precision_crm; print(precision_crm.__file__)"
cd ~/frappe/frappe-bench
python3 -c "import precision_crm; print(precision_crm.__file__)"
cd ~/frappe/frappe-bench
./env/bin/pip list | grep precision
cd ~/frappe/frappe-bench
./env/bin/python -c "import precision_crm; print(precision_crm.__file__)"
cd ~/frappe/frappe-bench
./env/bin/python -c "import precision_crm.hooks; print('HOOKS OK')"
./env/bin/python -c "import precision_crm.install; print('INSTALL OK')"
cat ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/modules.txt
bench version
find ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm -maxdepth 2 -type d
nano ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/__init__.py
echo '__version__ = "0.0.1"' >> ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/__init__.py
cd ~/frappe/frappe-bench
bench version
cd ~/frappe/frappe-bench
bench --site crm.local install-app precision_crm
cd ~/frappe/frappe-bench
./env/bin/python -c "import precision_crm.precision_crm"
cat ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/modules.txt
find ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/doctype -name "*.json" | head -20
cd ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm
sed -n '1,80p' precision_crm/doctype/lead/lead.json
sed -n '1,40p' precision_crm/hooks.py
nano ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/modules.txt
cat ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/modules.txt
cd ~/frappe/frappe-bench
bench clear-cache
bench clear-website-cache
bench --site crm.local install-app precision_crm
grep -R "\"module\"" ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/doctype | head -20
cat ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/modules.txt
nano ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/modules.txt
cd ~/frappe/frappe-bench
bench clear-cache
bench setup requirements
bench build
cd ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm
cat setup.py
cat pyproject.toml
cat precision_crm/__init__.py
cat ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/modules.txt
ls -la ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm
grep -R "module_name" ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm -n
grep -R "\"module\"" ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm -n | head -50
find ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm -name "*.json" | grep module
find ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm -name "module.txt"
cd ~/frappe/frappe-bench
bench console
find ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm -maxdepth 1 -type d
mkdir -p ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/precision_crm
touch ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/precision_crm/__init__.py
cd ~/frappe/frappe-bench
./env/bin/python -c "import precision_crm.precision_crm; print('OK')"
bench --site crm.local install-app precision_crm
./env/bin/python -c "import precision_crm.precision_crm"
nano ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
cat ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
def after_install():
nano ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
cd ~/frappe/frappe-bench
bench --site crm.local install-app precision_crm --force
sed -i '/def after_install()/,$c\def after_install():\n    pass' ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
cd ~/frappe/frappe-bench
bench --site crm.local install-app precision_crm --force
cd ~/frappe/frappe-bench
bench --site crm.local install-app precision_crm --force
nano ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
sed -n '1,50p' ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
nano ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
cat > ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py << 'EOF'
import frappe

def before_install():
    pass

def after_install():
    pass
EOF

cat ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/install.py
cd ~/frappe/frappe-bench
bench clear-cache
bench restart
bench --site crm.local install-app precision_crm --force
cd ~/frappe/frappe-bench
bench --site crm.local list-apps
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm
find precision_crm -name "*.json" | wc -l
find precision_crm/doctype -maxdepth 2 -name "*.json" | head -20
cat precision_crm/modules.txt
cd ~/frappe/frappe-bench
bench --site crm.local migrate
bench --site crm.local console
bench --site crm.local migrate
ls -la ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/doctype/lead
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/frappe/frappe-bench
./env/bin/python -c "
import precision_crm
print(precision_crm.__file__)
"
./env/bin/python -c "
import precision_crm.doctype.lead.lead
print('OK')
"
find ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm -name modules.txt
find ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm -type d -name doctype
cd ~/frappe/frappe-bench
bench --site crm.local console
grep -R '"doctype": "DocType"' ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm
{   "doctype": "Lead",;   "module": "Precision CRM"; }
{   "doctype": "DocType",;   "name": "Lead",;   "module": "Precision CRM"; }
"doctype": "Lead"
"doctype": "DocType"
head -20 ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/doctype/lead/lead.json
{   "doctype": "Lead",; {   "doctype": "DocType",;   "name": "Lead",; precision_crm 0.0.1; frappe.db.exists("DocType","Lead")
head -20 ~/leadcrm_import/Leadscrm/Leadscrm/Leads/precision_crm/precision_crm/doctype/lead/lead.json
crm_pro
cd ~/leadcrm_import/Leadscrm/Leadscrm/Leads
ls
find ~/leadcrm_import/Leadscrm/Leadscrm/Leads -name hooks.py | grep crm_pro
cd ~/frappe/frappe-bench
bench list-apps
cd ~/frappe/frappe-bench/apps
cp -r ~/leadcrm_import/Leadscrm/Leadscrm/Leads/crm_pro .
cd ~/frappe/frappe-bench
./env/bin/pip install -e apps/crm_pro
bench list-apps
bench --site crm.local install-app crm_pro
bench --site crm.local migrate
cd ~/frappe/frappe-bench/apps/crm_pro
ls -la
find . -maxdepth 2 -type d | sort
rm -rf docker
mv crm_pro/* .
cd ~/frappe/frappe-bench/apps/crm_pro
ls -la
find . -maxdepth 2 -type f | sort | head -50
cd ~/frappe/frappe-bench/apps/crm_pro
cat pyproject.toml
find crm_pro -type f | head -20
name = "crm_pro"
cd ~/frappe/frappe-bench/apps/crm_pro
cat pyproject.toml
ls -la crm_pro
mv crm_pro/* .
cd ~/frappe/frappe-bench/apps/crm_pro
mv __init__.py crm_pro/
mv hooks.py crm_pro/
mv install.py crm_pro/
mv ai.py crm_pro/
mv api.py crm_pro/
mv jobs.py crm_pro/
mv meta.py crm_pro/
mv doctype crm_pro/
mv tests crm_pro/
find crm_pro -maxdepth 2 | head -30
cd ~/frappe/frappe-bench
./env/bin/pip install -e apps/crm_pro
bench list-apps
bench setup requirements
bench --site crm.local install-app crm_pro
./env/bin/pip install -e apps/crm_pro
cd ~/frappe/frappe-bench
echo "crm_pro" >> sites/apps.txt
bench --site crm.local install-app crm_pro
nano ~/frappe/frappe-bench/sites/apps.txt
cat ~/frappe/frappe-bench/sites/apps.txt
bench --site crm.local migrate
bench --site crm.local install-app crm_pro
cat ~/frappe/frappe-bench/sites/apps.txt
cat ~/frappe/frappe-bench/sites/crm.local/apps.txt
crm_pro.crm_pro.install.after_install
crm_pro.crm_pro.api.lead_on_update
crm_pro.crm_pro.jobs.process_pending_reminders
cat ~/frappe/frappe-bench/apps/crm_pro/hooks.py
crm_pro.crm_pro.
crm_pro.
sed -i 's/crm_pro\.crm_pro\./crm_pro\./g' ~/frappe/frappe-bench/apps/crm_pro/hooks.pysed -i 's/crm_pro\.crm_pro\./crm_pro\./g' ~/frappe/frappe-bench/apps/crm_pro/hooks.py
sed -i 's/crm_pro\.crm_pro\./crm_pro\./g' ~/frappe/frappe-bench/apps/crm_pro/hooks.py
after_install = "crm_pro.install.after_install"
"crm_pro.api.lead_on_update"
"crm_pro.jobs.process_pending_reminders"
cd ~/frappe/frappe-bench
bench clear-cache
bench restart
bench console
bench --site crm.local install-app crm_pro
cat ~/frappe/frappe-bench/apps/crm_pro/hooks.py
import crm_pro
import crm_pro.hooks
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/frappe/frappe-bench
find apps/crm_pro -path "*doctype*" -type d | head -100
find apps/crm_pro -name "*.json" | head -100
tree -L 3 apps/crm_pro
sudo apt install tree -y
find apps/crm_pro -path "*doctype*" -type d
find apps/crm_pro -name "*.json"
ls -R apps/crm_pro
mv crm_pro/* .
ls -R apps/crm_pro
cd ~/frappe/frappe-bench
bench --site crm.local migrate
bench --site crm.local install-app crm_pro
bench --site crm.local migrate
bench --site crm.local console
frappe.get_all(
)
cd ~/frappe/frappe-bench
cat apps/crm_pro/crm_pro/hooks.py
head -50 apps/crm_pro/crm_pro/doctype/crm_lead/crm_lead.json
head -50 apps/crm_pro/crm_pro/doctype/crm_deal/crm_deal.json
bench --site crm.local console
bench --site crm.local migrate
grep -R "module_name" apps/crm_pro/crm_pro/doctype/*/*.json | head
find apps/crm_pro -name modules.txt -type f
cat apps/crm_pro/modules.txt
cat apps/crm_pro/crm_pro/modules.txt
bench new-app crm_pro
find apps/crm_pro -name modules.txt
cat apps/crm_pro/crm_pro/modules.txt
cd ~/frappe/frappe-bench
find apps/crm_pro -type f | sort | head -100
find apps/crm_pro -type f | sort | grep -E "hooks.py|modules.txt|pyproject.toml|__init__.py"
cd ~/frappe/frappe-bench
python3 - <<'PY'
import os

for root, dirs, files in os.walk("apps/crm_pro"):
    if "hooks.py" in files:
        print("HOOKS:", os.path.join(root,"hooks.py"))
    if "__init__.py" in files:
        print("PACKAGE:", root)
PY

import crm_pro
import crm_pro.hooks
frappe.db.exists("DocType","CRM Lead")
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/frappe/frappe-bench
find apps/crm_pro -type f | sort | grep -E "hooks.py|modules.txt|__init__.py|pyproject.toml"
cd ~/frappe/frappe-bench/apps/crm_pro/crm_pro
echo "CRM Pro" > modules.txt
cat modules.txt
cd ~/frappe/frappe-bench
bench --site crm.local migrate
bench --site crm.local reload-doc crm_pro doctype crm_lead
bench --site crm.local reload-doc crm_pro doctype crm_deal
cd ~/frappe/frappe-bench/apps/crm_pro/crm_pro
echo "CRM Pro" > modules.txt
cd ~/frappe/frappe-bench
bench clear-cache
bench migrate
bench restart
bench --site crm.local console
echo "CRM Pro" > ~/frappe/frappe-bench/apps/crm_pro/crm_pro/modules.txt
bench --site crm.local migrate
crm_pro.crm_pro
cd ~/frappe/frappe-bench
grep -R "crm_pro\.crm_pro" apps/crm_pro
cd ~/frappe/frappe-bench
grep -RIl "crm_pro\.crm_pro" apps/crm_pro | xargs sed -i 's/crm_pro\.crm_pro/crm_pro/g'
grep -R "crm_pro\.crm_pro" apps/crm_pro
cd ~/frappe/frappe-bench
find apps/crm_pro -name "__pycache__" -type d -exec rm -rf {} +
bench clear-cache
bench restart
bench --site crm.local migrate
bench --site crm.local migrate 2>&1 | tail -50
cat ~/frappe/frappe-bench/apps/crm_pro/crm_pro/modules.txt
cd ~/frappe/frappe-bench
python3 - <<'PY'
import crm_pro
print("PACKAGE:", crm_pro.__file__)
PY

python3 - <<'PY'
import crm_pro
PY

cd ~/frappe/frappe-bench
./env/bin/python - <<'PY'
import crm_pro
print("PACKAGE:", crm_pro.__file__)
PY

import crm_pro
print(crm_pro.__file__)
cd ~/frappe/frappe-bench
grep -R "crm_pro\.crm_pro" apps/crm_pro sites config --exclude-dir=__pycache__ --exclude="*.pyc"
cd ~/frappe/frappe-bench
grep -R "crm_pro\.crm_pro" apps/crm_pro sites config --exclude-dir=__pycache__ --exclude="*.pyc"
cd ~/frappe/frappe-bench
bench --site crm.local console
get_module_app("CRM Pro")
# returns crm_pro
cd ~/frappe/frappe-bench
ls -la apps/crm_pro/crm_pro
cat apps/crm_pro/crm_pro/modules.txt
find apps/crm_pro/crm_pro -maxdepth 2 -type d | sort
cd ~/frappe/frappe-bench
cat apps/crm_pro/crm_pro/modules.txt
acer@Z14-55N:~/frappe/frappe-bench$ cd ~/frappe/frappe-bench
cat apps/crm_pro/crm_pro/modules.txt
CRM Pro
bench --site crm.local console
import crm_pro.<module_name>
bench --site crm.local execute frappe.db.sql --kwargs '{"query":"select name, app_name from `tabModule Def`"}'
cd ~/frappe/frappe-bench
grep -R "crm_pro.crm_pro" apps/crm_pro sites/crm.local --exclude-dir=__pycache__ --exclude="*.pyc"
cd ~/frappe/frappe-bench
grep -R "crm_pro.crm_pro" apps/crm_pro sites/crm.local --exclude-dir=__pycache__ --exclude="*.pyc"
cd ~/frappe/frappe-bench
grep -R "crm_pro.crm_pro" apps/crm_pro sites/crm.local --exclude-dir=__pycache__ --exclude="*.pyc"
import frappe
frappe.db.sql("""
select name,module
from `tabDocType`
where module='CRM Pro'
""", as_dict=True)
import frappe
frappe.db.sql("""
select *
from `tabInstalled Applications`
where app_name='crm_pro'
""", as_dict=True)
bench --site crm.local uninstall-app crm_pro --force
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/frappe/frappe-bench
./env/bin/python - <<'PY'
import crm_pro
import crm_pro.doctype.crm_lead.crm_lead

print("APP OK")
print("DOCTYPE OK")
PY

cd ~/frappe/frappe-bench
grep -R "crm_pro\.crm_pro" apps/crm_pro
find apps/crm_pro -type d -name "__pycache__" -exec rm -rf {} +
bench --site crm.local console
bench clear-cache
bench clear-website-cache
bench build
bench restart
bench --site crm.local remove-from-installed-apps crm_pro
bench --site crm.local migrate --verbose
bench --site crm.local migrate > migrate.log 2>&1
grep -n "crm_pro.crm_pro" migrate.log
bench --site crm.local console
cd ~/frappe/frappe-bench
bench --site crm.local install-app crm_pro
bench --site crm.local console
./env/bin/python - <<'PY'
import crm_pro
import crm_pro.doctype.crm_lead.crm_lead
print("APP OK")
print("DOCTYPE OK")
PY

bench --site crm.local backup
bench --site crm.local mariadb
DELETE FROM `tabModule Def`
WHERE name='CRM Pro';
./env/bin/python - <<'PY'
import crm_pro
import crm_pro.doctype.crm_lead.crm_lead
print("APP OK")
print("DOCTYPE OK")
PY

frappe.db.exists("Module Def", "CRM Pro")
cd ~/frappe/frappe-bench
bench --site crm.local mariadb
bench --site crm.local clear-cache
bench restart
bench --site crm.local install-app crm_pro
bench --site crm.local mariadb -e "
SELECT name
FROM \`tabModule Def\`
WHERE name='CRM Pro';
"
bench --site crm.local install-app crm_pro > install.log 2>&1
tail -100 install.log
./env/bin/python -c "import crm_pro; import crm_pro.doctype.crm_lead.crm_lead"
frappe.db.exists("Module Def", "CRM Pro")
frappe.db.exists("DocType", "CRM Lead")
# None
frappe.db.exists("DocType", "CRM Lead")
# None
frappe.get_installed_apps()
exit
bench --site crm.local mariadb
bench --site crm.local mariadb -e "
SELECT name
FROM \`tabModule Def\`
WHERE name='CRM Pro';
"
bench --site crm.local clear-cache
bench --site crm.local install-app crm_pro
cd ~/frappe/frappe-bench
mkdir -p apps/crm_pro/crm_pro/crm_pro
touch apps/crm_pro/crm_pro/crm_pro/__init__.py
mv apps/crm_pro/crm_pro/doctype    apps/crm_pro/crm_pro/crm_pro/
find apps/crm_pro/crm_pro -maxdepth 3 -type d | sort
./env/bin/python - <<'PY'
import crm_pro.crm_pro
print("crm_pro.crm_pro OK")
PY

bench --site crm.local clear-cache
bench restart
bench --site crm.local install-app crm_pro
cd ~/frappe/frappe-bench
find apps/crm_pro -type d | grep role
bench --site crm.local console
cat apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_config/crm_role_config.json | head -20
mv apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_config apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration
bench --site crm.local migrate
grep -R '"name": "CRM' apps/crm_pro/crm_pro/crm_pro/doctype/*/*.json
cd ~/frappe/frappe-bench
for d in apps/crm_pro/crm_pro/crm_pro/doctype/*; do     folder=$(basename "$d");      json=$(find "$d" -name "*.json" | head -1);      if [ -n "$json" ]; then         file=$(basename "$json" .json);          if [ "$folder" != "$file" ]; then             echo "MISMATCH:";             echo " Folder: $folder";             echo " File  : $file";             echo;         fi;     fi; done
ls -la apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration
cd ~/frappe/frappe-bench
mv apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/crm_role_config.py apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/crm_role_configuration.py
mv apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/crm_role_config.json apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/crm_role_configuration.json
./env/bin/python
bench --site crm.local reload-doc crm_pro doctype crm_role_configuration
bench --site crm.local migrate
cd ~/frappe/frappe-bench
find apps/crm_pro/crm_pro/crm_pro/doctype -mindepth 1 -maxdepth 1 -type d | while read d; do     folder=$(basename "$d");      json=$(find "$d" -name "*.json" | head -1);      if [ -z "$json" ]; then         echo "NO JSON: $folder";         continue;     fi;      file=$(basename "$json" .json);      if [ "$folder" != "$file" ]; then         echo "BROKEN:";         echo " Folder = $folder";         echo " JSON   = $file";         echo;     fi; done
bench --site crm.local migrate
bench --site crm.local list-apps
bench --site crm.local install-app crm_pro > install.log 2>&1
tail -100 install.log
bench --site crm.local console
import frappe
frappe.db.exists(
)
import frappe
frappe.delete_doc(
)
frappe.db.commit() print("Deleted")
frappe.db.exists(
)
cd ~/frappe/frappe-bench
pwd
bench --site crm.local console
cd ~/frappe/frappe-bench
bench --site crm.local mariadb
cat apps/crm_pro/crm_pro/modules.txt
cd ~/frappe/frappe-bench
bench --site crm.local console
find apps/crm_pro -type d | grep doctype
cd ~/frappe/frappe-bench
find apps/crm_pro -name modules.txt -exec echo "===" {} "===" \; -exec cat {} \;
cd ~/frappe/frappe-bench
grep -R "CRM Pro" apps/crm_pro | head -50
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/frappe/frappe-bench
find apps/crm_pro -name "*.pyc" -delete
find apps/crm_pro -name "__pycache__" -type d -exec rm -rf {} +
bench clear-cache
bench restart
bench --site crm.local install-app crm_pro --force
tail -50 logs/web.error.log
bench --site crm.local list-apps
bench --site crm.local console
bench --site crm.local migrate
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
bench restart
bench --site crm.local execute frappe.get_installed_apps
cd ~/frappe/frappe-bench
ls -la apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration
crm_role_config.json
mv apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/crm_role_config.json apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/crm_role_configuration.json
bench --site crm.local reload-doc crm_pro doctype crm_role_configuration
bench --site crm.local migrate
bench --site crm.local reload-doc crm_pro doctype crm_role_configuration
bench --site crm.local migrate
bench --site crm.local console
cd ~/frappe/frappe-bench
ls -la apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration
find apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration -name "*.json"
grep '"name"' apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/*.json
ls -la apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration
find apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration -name "*.json"
grep '"name"' apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/*.json
python3 -m json.tool apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/crm_role_configuration.json
grep '"module"' apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/crm_role_configuration.json
cat apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/crm_role_configuration.py
cat apps/crm_pro/crm_pro/crm_pro/doctype/crm_lead/crm_lead.py
"doctype": "DocType"
cat apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/crm_role_configuration.json
cd ~/frappe/frappe-bench
grep -R "CRM Role Configuration" apps/crm_pro
rm -rf apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration
bench --site crm.local migrate
bench restart
bench --site crm.local console
bench --site crm.local export-fixtures
rm -rf apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration
bench --site crm.local migrate
bench restart
nano sites/crm.local/site_config.json
bench restart
bench --site crm.local console
import frappe
print(frappe.conf.developer_mode)
cat sites/crm.local/site_config.json
{   "developer_mode": 1; }
{   "db_name": "_1195e485d233df44"; }
{   "developer_mode": 1; }
{   "db_name": "_1195e485d233df44"; }
ls sites/crm.local/
cp sites/crm.local/site_config.json.bak sites/crm.local/site_config.json
python3 -m json.tool sites/crm.local/site_config.json
cd ~/frappe/frappe-bench
pwd
ls -la sites/
cat sites/crm.local/site_config.json
{   "db_name": "_1195e485d233df44",;   "developer_mode": 1; }
nano sites/crm.local/site_config.json
cd ~/frappe/frappe-bench
ls apps/crm_pro/crm_pro/doctype
ls apps/crm_pro/crm_pro/crm_pro/doctype
cd ~/frappe/frappe-bench
ls apps/crm_pro/crm_pro/crm_pro/doctype | grep role
crm_role_configuration
cd ~/frappe/frappe-bench
find apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration -type f
cd ~/frappe/frappe-bench
find apps/crm_pro -iname "*role*"
mkdir -p apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration
touch apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/__init__.py
nano apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/crm_role_configuration.py
nano apps/crm_pro/crm_pro/crm_pro/doctype/crm_role_configuration/crm_role_configuration.json
bench --site crm.local reload-doc crm_pro doctype crm_role_configuration
bench --site crm.local migrate
~/frappe/frappe-bench
cd ~/frappe/frappe-bench
cat sites/crm.local/site_config.json
nano sites/crm.local/site_config.json
cd ~/frappe/frappe-bench
bench --site crm.local migrate
redis-server --version
sudo systemctl status redis
bench doctor
bench --site crm.local list-apps
bench browse
bench --site crm.local show-config
bench show-pending-jobs
bench --site crm.local execute frappe.get_installed_apps
whoami
bench doctor
bench --site crm.local list-apps
bench show-pending-jobs
bench --site crm.local execute frappe.get_installed_apps
bench --site crm.local execute "import frappe; print(frappe.get_all('DocType', filters={'module':'CRM Pro'}, pluck='name'))"
bench --site crm.local execute "import frappe; print('Deals:', frappe.db.count('CRM Deal'))"
bench --site crm.local execute "import frappe; print('Contacts:', frappe.db.count('CRM Contact'))"
bench --site crm.local execute "import frappe; print('Companies:', frappe.db.count('CRM Company'))"
bench start
bench --site crm.local execute "import frappe; print(...)"
bench --site crm.local execute frappe.utils.now
bench --site crm.local console
bench start
ps aux | grep redis
ss -lntp | grep 13000
ss -lntp | grep 11000
pkill -f redis
pkill -f frappe
pkill -f node
pkill -f rq
ps aux | grep redis
cd ~/frappe/frappe-bench
bench start
sudo sysctl vm.overcommit_memory=1
bench --site crm.local console
grep -R "@frappe.whitelist" apps/crm_pro
frappe.get_single("CRM Settings")
npm run build
sudo sysctl vm.overcommit_memory=1
whoami
groups
find ~/frappe/frappe-bench/apps -name package.json
grep -n "def " apps/crm_pro/crm_pro/ai.py
grep -n "def " apps/crm_pro/crm_pro/api.py
grep -n "def " apps/crm_pro/crm_pro/meta.py
find apps/crm_pro -name package.json
tree -L 3 apps/crm_pro
find apps/crm_pro -maxdepth 3 -type d
ls -la apps
ls -R apps/crm_pro | head -100
find apps/crm_pro -name package.json
bench --site crm.local migrate
bench restart
bench --site crm.local console
grep -n "@frappe.whitelist" apps/crm_pro/crm_pro/api.py
bench execute crm_pro.crm_pro.api.get_dashboard_metrics --site crm.local
bench doctor
sudo service redis-server status
bench doctor
bench --site crm.local migrate
cd ~/frappe/frappe-bench
bench doctor
bench list-apps
bench --site crm.local migrate
bench --site crm.local execute crm_pro.api.get_dashboard_metrics
bench --site crm.local run-tests
cd ~/frappe/frappe-bench
source env/bin/activate
pip install responses
python -c "import responses; print(responses.__version__)"
bench --site crm.local run-tests
cd ~/frappe/frappe-bench
source env/bin/activate
pip install responses
pip show responses
apps/crm_pro/pyproject.toml
dependencies = [
]
cat apps/crm_pro/pyproject.toml
nano apps/crm_pro/pyproject.toml
vim apps/crm_pro/pyproject.toml
nano apps/crm_pro/pyproject.toml
bench doctor
bench --site crm.local migrate
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
\bench doctor
bench --site crm.local migrate
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
bench doctor
bench --site crm.local migrate
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
bench doctor
bench worker
bench schedule
cd ~/frappe/frappe-bench
pwd
bench version
bench list-apps
bench --site crm.local migrate
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
bench --site crm.local show-config
bench --site crm.local execute frappe.utils.scheduler.is_scheduler_inactive
bench --site crm.local list-apps
bench --site crm.local execute "print(frappe.db.exists('DocType','CRM Role Configuration'))"
bench --site crm.local execute "import frappe; print(frappe.utils.background_jobs.get_jobs())"
cd ~/frappe/frappe-bench
bench version
bench --help
bench --site crm.local migrate
cd ~/frappe/frappe-bench
bench start
cd ~/frappe/frappe-bench
bench start
ls apps/crm_pro
cd ~/frappe/frappe-bench
pwd
ls apps
ls apps/crm_pro
~/frappe/frappe-bench
env/bin/python -c "import responses; print('OK')"
bench --site crm.local run-tests --app crm_pro
bench --site crm.local execute crm_pro.api.get_dashboard_metrics
bench --site crm.local execute crm_pro.jobs.process_due_reminders
bench --site crm.local execute crm_pro.jobs.update_dashboard_metrics
bench --site crm.local execute crm_pro.verify_all.run
bench --site crm.local console
bench --site crm.local execute crm_pro.jobs.process_due_reminders
bench --site crm.local execute crm_pro.jobs.process_pending_reminders
bench --site crm.local execute crm_pro.jobs.update_dashboard_metrics
bench --site crm.local execute crm_pro.jobs.recalculate_dashboard_metrics
bench --site crm.local execute crm_pro.verify_all.run
import crm_pro.verify_all
dir(crm_pro.verify_all)
bench --site crm.local execute crm_pro.verify_all.setup_webhook_settings
bench --site crm.local execute crm_pro.verify_all.restore_webhook_settings
bench doctor
bench --site crm.local scheduler status
bench --site crm.local show-pending-jobs
bench --site crm.local execute crm_pro.jobs.process_pending_reminders
bench --site crm.local console
bench --site crm.local enable-scheduler
bench --site crm.local scheduler resume
bench doctor
bench --site crm.local scheduler status
import crm_pro.verify_all
bench --site crm.local console
env/bin/python
bench doctor
bench --site crm.local scheduler status
bench --site crm.local execute crm_pro.api.get_dashboard_metrics
bench --site crm.local execute crm_pro.verify_all.setup_webhook_settings
bench --site crm.local execute crm_pro.verify_all.restore_webhook_settings
dir(crm_pro.verify_all)
bench --site crm.local execute crm_pro.verify_all.run
cd ~/frappe/frappe-bench
cat apps/crm_pro/crm_pro/verify_all.py
sed -n '1,200p' apps/crm_pro/crm_pro/verify_all.py
nano apps/crm_pro/crm_pro/verify_all.py
bench --site crm.local execute crm_pro.verify_all.setup_webhook_settings
bench --site crm.local execute crm_pro.verify_all.restore_webhook_settings
grep -R "^def " apps/crm_pro/crm_pro
bench --site crm.local execute module.function_name
bench doctor
bench --site crm.local scheduler status
bench --site crm.local execute crm_pro.api.get_dashboard_metrics
bench --site crm.local execute crm_pro.jobs.recalculate_dashboard_metrics
bench --site crm.local execute crm_pro.jobs.process_pending_reminders
bench --site crm.local run-tests --app crm_pro
cat ~/frappe/frappe-bench/apps/crm_pro/crm_pro/verify_all.py
bench --site crm.local execute crm_pro.verify_all.run
nano ~/frappe/frappe-bench/apps/crm_pro/crm_pro/verify_all.py
bench --site crm.local execute crm_pro.verify_all.run
apps/crm_pro/crm_pro/verify_all.py
def run()
nano ~/frappe/frappe-bench/apps/crm_pro/crm_pro/verify_all.py
bench restart
bench clear-cache
bench --site crm.local execute crm_pro.verify_all.run
bench doctor
bench --site crm.local scheduler status
bench --site crm.local execute crm_pro.api.get_dashboard_metrics
bench --site crm.local execute crm_pro.jobs.recalculate_dashboard_metrics
bench --site crm.local execute crm_pro.jobs.process_pending_reminders
bench --site crm.local run-tests --app crm_pro
bench doctor
bench --site crm.local scheduler status
bench --site crm.local execute crm_pro.api.get_dashboard_metrics
bench --site crm.local execute crm_pro.jobs.recalculate_dashboard_metrics
bench --site crm.local execute crm_pro.jobs.process_pending_reminders
bench --site crm.local run-tests --app crm_pro
~/frappe/frappe-bench
bench --site crm.local mariadb
show tables like '%CRM%';
show tables like '%Lead%';
select count(*) from `tabCRM Lead`;
bench --site crm.local mariadb
select count(*) from `tabCRM Lead`;
select * from `tabCRM Lead`;
select name, lead_name, email, mobile_no from `tabCRM Lead`;
cd ~/frappe/frappe-bench
bench --site crm.local mariadb
cd ~/frappe/frappe-bench
bench --site crm.local console
bench doctor
bench --site crm.local scheduler status
bench --site crm.local execute crm_pro.api.get_dashboard_metrics
bench --site crm.local run-tests --app crm_pro
frappe.get_all("Workspace", pluck="name")
bench --site crm.local console
bench doctor
bench restart
bench --site crm.local mariadb
bench --site crm.local console
bench --site crm.local execute crm_pro.api.get_dashboard_metrics
bench --site crm.local mariadb
frappe.get_all("Workspace", pluck="name")
cd ~/frappe/frappe-bench
bench --site crm.local mariadb
bench --site crm.local console
bench --site crm.local clear-cache
bench restart
bench --site crm.local console
meta = frappe.get_meta("CRM Lead")
[f.fieldname for f in meta.fields]
[(f.fieldname, f.label) for f in frappe.get_meta("CRM Lead").fields]
frappe.get_all(
)
bench --site crm.local console
meta
bench
ls
cd
cat
nano
bench --site crm.local console
[(f.fieldname, f.label) for f in frappe.get_meta("CRM Lead").fields]
cd ~/frappe/frappe-bench
pwd
bench --site crm.local console
bench --site crm.local execute frappe.client.get_value --kwargs "{'doctype':'CRM Lead','filters':{'name':'6gklho2n9a'},'fieldname':['*']}"
bench --site crm.local mariadb
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/frappe/frappe-bench
find . -name "production_readiness_report.md"
find . -name "security_audit.md"
find . -name "openapi.yaml"
grep -n "retry" apps/crm_pro/crm_pro/meta.py
grep -n "backoff" apps/crm_pro/crm_pro/meta.py
head -40 audit_reports/openapi.yaml
grep -R "scheduler_events" apps/crm_pro
bench --site crm.local list-apps
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/frappe/frappe-bench/apps/crm_pro/crm_pro
ls
nano api.py
cd ~/frappe/frappe-bench
bench --site crm.local mariadb
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/frappe/frappe-bench
bench --site crm.local console
bench --site crm.local migrate
bench restart
frappe.db.count("CRM Lead")
cd ~/frappe/frappe-bench
bench --site crm.local migrate
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
cd ~/frappe/frappe-bench
bench --site crm.local console
bench doctor
bench migrate
{   "total_leads":1; }
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/frappe/frappe-bench
bench start
cd ~/frappe/frappe-bench
bench start
ps aux | grep redis
ps aux | grep bench
pkill -f redis-server
pkill -f bench
pkill -f frappe
pkill -f node
ps aux | grep redis
sudo lsof -i :11000
sudo lsof -i :13000
bench start
hostname -I
ps -ef | grep frappe
ss -tulpn | grep 8000
curl http://127.0.0.1:8000
cd ~/frappe/frappe-bench
bench --site crm.local console
CRM Lead
CRM Deal
CRM Note
CRM Settings
CRM WhatsApp Log
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/frappe/frappe-bench
bench --site crm.local console
nano ~/frappe/frappe-bench/apps/crm_pro/crm_pro/doctype/crm_deal/crm_deal.py
cd ~/frappe/frappe-bench
bench --site crm.local migrate
bench --site crm.local clear-cache
bench --site crm.local console
nano ~/frappe/frappe-bench/apps/crm_pro/crm_pro/doctype/crm_deal/crm_deal.py
cd ~/frappe/frappe-bench
bench --site crm.local migrate
bench restart
bench clear-cache
bench clear-website-cache
bench --site crm.local console
nano ~/frappe/frappe-bench/apps/crm_pro/crm_pro/doctype/crm_deal/crm_deal.py
cd ~/frappe/frappe-bench
bench --site crm.local migrate
bench --site crm.local clear-cache
bench --site crm.local console
cd ~/frappe/frappe-bench
bench serve
bench start
cd ~/frappe/frappe-bench
ls sites
cat sites/currentsite.txt
bench --site crm.local list-apps
sites/currentsite.txt
crm.local
bench --site crm.local list-apps
bench serve
sudo lsof -i :8000
lsof -i :8000
curl http://127.0.0.1:8000
cat sites/currentsite.txt
whoami
wsl -u root
passwd YOUR_USERNAME
whoami
ss -tulpn | grep 8000
curl http://127.0.0.1:8000
curl -I http://127.0.0.1:8000
bench --site crm.local console
CRM Pro Workspace
Customize Workspace
cd ~/frappe/frappe-bench
bench --site crm.local console
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
bench --site crm.local console
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/frappe/frappe-bench
bench --site crm.local console
bench --site crm.local clear-cache
bench start
bench --site crm.local console
CRM Lead
CRM Deal
CRM Contact
CRM Company
CRM Task
CRM Settings
cd ~/frappe/frappe-bench
bench --site crm.local console
bench --site crm.local clear-cache
bench start
cd ~/frappe/frappe-bench
bench --site crm.local console
cat apps/crm_pro/crm_pro/workspace/crm_pro/crm_pro.json
ws.links
ws.shortcuts
crm_pro.json
bench --site crm.local console
bench --site crm.local clear-cache
bench start
bench --site crm.local console
bench start
cd ~/frappe/frappe-bench
bench --site crm.local console
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
bench start
bench --site crm.local console
cd ~/frappe/frappe-bench
bench --site crm.local console
/api/method/crm_pro.api.create_lead
/api/method/crm_pro.api.get_deals
/api/method/crm_pro.api.create_deal
bench --site crm.local console
curl -X POST http://127.0.0.1:8000/api/method/crm_pro.api.create_lead -H "Content-Type: application/json" -d '{
"name":"Test Lead",
"email":"test@example.com",
"phone":"9876543210"
}'
grep -n "@frappe.whitelist" apps/crm_pro/crm_pro/api.py
cat apps/crm_pro/crm_pro/api.py
frappe.db.count("CRM Lead")
frappe.db.count("CRM Deal")
frappe.get_all(
)
frappe.get_all(
)
bench --site crm.local console
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
bench build
bench restart
ws = frappe.get_doc("Workspace","CRM Pro")
print("Links:",len(ws.links))
print("Cards:",len(ws.number_cards))
print("Charts:",len(ws.charts))
print("Shortcuts:",len(ws.shortcuts))
ws = frappe.get_doc("Workspace","CRM Pro")
print("Links:",len(ws.links))
bench --site crm.local console
nano apps/crm_pro/crm_pro/workspace/leads_workspace/leads_workspace.json
ws = frappe.get_doc("Workspace", "Leads Workspace")
print(ws.content)
bench --site crm.local console
/app/workspace/Leads Workspace
[
]
frappe.get_doc("Number Card", "Total Leads")
frappe.get_doc("Dashboard Chart", "Lead Sources")
frappe.get_doc("Workspace", "Leads Workspace").content
cd ~/frappe/frappe-bench
bench --site crm.local console
chart = frappe.get_doc("Dashboard Chart", "Lead Sources")
chart.chart_type
chart.document_type
chart.group_by_based_on
chart.filters_json
document_type = CRM Lead
function = Count
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
bench migrate
bench build
bench restart
ws = frappe.get_doc("Workspace", "Leads Workspace")
print(ws.content)
ws = frappe.get_doc("Workspace", "Leads Workspace")
print(ws.content)
frappe.get_doc("Dashboard Chart", "Lead Sources").as_dict()
frappe.get_doc("Workspace", "Leads Workspace")
bench --site crm.local console
bench doctor
bench status
bench --site crm.local console
cd ~/Downloads/Leadscrm/Leadscrm/Leads/docs/database
ls
cat ER_Diagram.md
cd /mnt/c/Users/acer/Downloads/Leadscrm/Leadscrm/Leads/docs/database
ls
find /mnt/c/Users/acer/Downloads/Leadscrm -name "*.md"
bench --site crm.local console
cd ~/frappe/frappe-bench
bench --site crm.local console
cd ~/Downloads/Leadscrm/Leadscrm/Leads/docs/database
cd ~/frappe/frappe-bench
bench --site crm.local console
find ~/ -name "ER_Diagram.md"
find /mnt/c -name "ER_Diagram.md" 2>/dev/null
cd ~/frappe/frappe-bench
find /mnt/c -name "ER_Diagram.md" 2>/dev/null
find ~/ -name "ER_Diagram.md"
cat ER_Diagram.md
find ~/ -name "ER_Diagram.md"
bench --site crm.local console
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
bench migrate
bench restart
deal = frappe.get_doc({
})
deal.insert(ignore_permissions=True)
frappe.db.commit() frappe.db.count("CRM Deal")
bench --site crm.local console
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
bench restart
bench --site crm.local console
cd ~/frappe/frappe-bench
find . -name "*.md"
cd /mnt/c/Users/acer/Downloads/Leadscrm/Leadscrm/Leads/crm_pro/docs/database
ls -lah
head -20 ER_Diagram.md
cd /mnt/c/Users/acer/Downloads/Leadscrm/Leadscrm/Leads/crm_pro/docs/database
ls -lah
cd ~/frappe/frappe-bench
ls ~/frappe/frappe-bench/apps/crm_pro/docs
find ~/frappe/frappe-bench/apps/crm_pro/docs -type f
bench --site crm.local console
grep -R "@frappe.whitelist" apps/crm_pro
frappe.get_single("System Settings").as_dict()
frappe.db.exists("DocType", "Two Factor Authentication")
bench init frappe-bench
sudo apt update
sudo apt install pkg-config -y
pwd
uname -a
git --version
which git
git --version
where git
git --version
pkg-config --version
bench --version
sudo apt install pkgconf -y
winget install ...
pkg-config --version
bench version
bench doctor
bench migrate
bench build
bench run-tests --app crm_pro
cd ~/frappe/frappe-bench
bench version
bench doctor
bench list-apps
bench --site all list-apps
ls sites
bench --site crm.local migrate
bench --site crm.local console
grep validate_password crm_pro/hooks.py
bench --site crm.local console
bench start
bench doctor
bench migrate
bench build
bench run-tests --app crm_pro
cd ~/frappe/frappe-bench
bench doctor
bench list-apps
ls sites
bench --site crm.local migrate
bench --site crm.local console
bench --site crm.local run-tests --app crm_pro
git status
cd ~/frappe/frappe-bench
find apps/crm_pro -name "*.json"
grep -L '"name"' $(find apps/crm_pro -name "*.json")
python3 - <<'EOF'
import json, os

for root, dirs, files in os.walk("apps/crm_pro"):
    for f in files:
        if f.endswith(".json"):
            path=os.path.join(root,f)
            try:
                data=json.load(open(path))
                if isinstance(data,dict):
                    if "doctype" in data and "name" not in data:
                        print("BROKEN:",path)
            except:
                pass
EOF

pkill redis
pkill node
pkill python
bench start
git status
fatal: not a git repository
cd apps/crm_pro
git status
python3 - <<'EOF'
import json, os

for root, dirs, files in os.walk("apps/crm_pro"):
    for f in files:
        if f.endswith(".json"):
            path=os.path.join(root,f)
            try:
                data=json.load(open(path))
                if isinstance(data,dict):
                    if "doctype" in data and "name" not in data:
                        print("BROKEN:",path)
            except Exception as e:
                print("INVALID:",path,e)
EOF

~/frappe/frappe-bench
python3 - <<'EOF'
import json, os

for root, dirs, files in os.walk("apps/crm_pro"):
    for f in files:
        if f.endswith(".json"):
            path=os.path.join(root,f)

            try:
                data=json.load(open(path))

                if isinstance(data,dict):
                    if "doctype" in data and "name" not in data:
                        print("MISSING NAME:",path)

                elif isinstance(data,list):
                    for row in data:
                        if isinstance(row,dict):
                            if "doctype" in row and "name" not in row:
                                print("MISSING NAME IN LIST:",path)

            except Exception as e:
                print("INVALID JSON:",path)
                print(e)

EOF

find apps/crm_pro -path "*fixtures*" -name "*.json"
bench --site crm.local console
cd ~/frappe/frappe-bench
find apps/crm_pro -path "*fixtures*" -name "*.json"
bench --site crm.local console
cd ~/frappe/frappe-bench
python3 - <<'EOF'
import json, os

for app in ["apps/crm_pro", "apps/precision_crm"]:
    print("\nCHECKING:", app)

    for root, dirs, files in os.walk(app):
        for f in files:
            if f.endswith(".json"):
                path=os.path.join(root,f)

                try:
                    data=json.load(open(path))

                    if isinstance(data,dict):
                        if "doctype" in data and "name" not in data:
                            print("BROKEN:",path)

                    elif isinstance(data,list):
                        for row in data:
                            if isinstance(row,dict):
                                if "doctype" in row and "name" not in row:
                                    print("BROKEN LIST:",path)

                except Exception:
                    pass
EOF

find apps/precision_crm -name "*.json" | wc -l
find apps/precision_crm -path "*fixtures*" -name "*.json"
bench --site crm.local migrate --skip-search-index
cd ~/frappe/frappe-bench
bench start
cd ~/frappe/frappe-bench
find apps/crm_pro apps/precision_crm -name "*.json" | while read f; do     python3 -c "
import json
try:
    d=json.load(open('$f'))
    if isinstance(d,dict) and d.get('doctype')!='DocType':
        pass
except Exception as e:
    print('$f',e)
"; done
bench --site crm.local migrate
cat apps/crm_pro/crm_pro/doctype/auth_audit_log/auth_audit_log.json | head -20
cat apps/crm_pro/crm_pro/doctype/mfa_settings/mfa_settings.json | head -20
cat apps/crm_pro/crm_pro/doctype/password_history/password_history.json | head -20
cat apps/crm_pro/crm_pro/doctype/user_session/user_session.json | head -20
bench run-tests --app crm_pro
frappe.get_doc("DocType", "Auth Audit Log")
cd ~/frappe/frappe-bench
mkdir -p backup_broken_doctypes
mv apps/crm_pro/crm_pro/doctype/auth_audit_log backup_broken_doctypes/
mv apps/crm_pro/crm_pro/doctype/mfa_settings backup_broken_doctypes/
mv apps/crm_pro/crm_pro/doctype/password_history backup_broken_doctypes/
mv apps/crm_pro/crm_pro/doctype/user_session backup_broken_doctypes/
bench --site crm.local migrate
bench build
bench clear-cache
bench restart
bench --site crm.local run-tests --app crm_pro
grep -R "Auth Audit Log" apps/crm_pro
grep -R "MFA Settings" apps/crm_pro
grep -R "Password History" apps/crm_pro
grep -R "User Session" apps/crm_pro
bench --site crm.local console
find apps/crm_pro -name "*.py" | xargs grep -n "@frappe.whitelist"
grep -R "Auth Audit Log" apps/crm_pro
grep -R "MFA Settings" apps/crm_pro
grep -R "Password History" apps/crm_pro
grep -R "User Session" apps/crm_pro
grep -R "whatsapp" apps/crm_pro
grep -R "facebook" apps/crm_pro
Facebook Lead Form
Webhook
CRM Lead Creation
grep -R "allow_guest=True" apps/crm_pro
grep -R "frappe.db.sql(" apps/crm_pro
bench backup
cd apps/crm_pro
git init
git add .
git commit -m "stable crm build"
grep -R "Auth Audit Log" apps/crm_pro
grep -R "MFA Settings" apps/crm_pro
grep -R "Password History" apps/crm_pro
grep -R "User Session" apps/crm_pro
find apps/crm_pro -name "*.py" | xargs grep -n "@frappe.whitelist"
nano apps/crm_pro/crm_pro/api_auth.py
@frappe.whitelist(allow_guest=True)
grep -R "allow_guest=True" apps/crm_pro
grep -n "@frappe.whitelist" apps/crm_pro/crm_pro/api_auth.py
grep -n "@frappe.whitelist" apps/crm_pro/crm_pro/meta.py
bench --site crm.local console
cd ~/frappe/frappe-bench
@frappe.whitelist(allow_guest=True)
grep -R "allow_guest=True" apps/crm_pro
grep -n "@frappe.whitelist" apps/crm_pro/crm_pro/api_auth.py
grep -n "@frappe.whitelist" apps/crm_pro/crm_pro/meta.py
bench --site crm.local console
grep -R "@frappe.whitelist" apps/crm_pro > crm_api_inventory.txt
git config --global user.name "Acer"
git config --global user.email "acer@example.com"
cd ~/frappe/frappe-bench/apps/crm_pro
git init
git add .
git commit -m "stable crm build"
cd ~/frappe/frappe-bench
bench --site crm.local console
grep -R "@frappe.whitelist" apps/crm_pro > crm_api_inventory.txt
cat crm_api_inventory.txt
grep -R "allow_guest=True" apps/crm_pro
grep -R "frappe.db.sql(" apps/crm_pro
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete
cat crm_api_inventory.txt
grep -n "def " apps/crm_pro/crm_pro/api_auth.py
grep -n "def " apps/crm_pro/crm_pro/api.py
frappe.db.sql(
)
git init
git add .
git commit -m "stable crm build"
git rm -r --cached .
git add .
git commit -m "cleanup repository"
grep -n "def " apps/crm_pro/crm_pro/api.py
grep -n "def " apps/crm_pro/crm_pro/api_auth.py
grep -n "def " apps/crm_pro/crm_pro/ai.py
grep -n "def " apps/crm_pro/crm_pro/meta.py
~/frappe/frappe-bench
git status
rm -rf .git
cd apps/crm_pro
git init
git add .
git commit -m "stable crm build"
bench --site crm.local list-apps
cd ~/frappe/frappe-bench
bench --site crm.local list-apps
bench --site crm.local migrate
bench --site crm.local clear-cache
bench --site crm.local clear-website-cache
bench --site crm.local console
bench build
bench start
Register
Login
Forgot Password
Reset Password
MFA
API Keys
bench setup production frappe
bench --site crm.local migrate
bench build
bench start
bench setup production frappe
ps aux | grep redis
sudo lsof -i :11000
sudo lsof -i :13000
pkill redis
cd ~/frappe/frappe-bench
bench start
ps aux | grep redis
cd ~/frappe/frappe-bench
bench start
bench --site crm.local set-admin-password admin123
