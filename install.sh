pip install -r requirements.txt

%%capture
pip install unsloth
pip uninstall unsloth -y && pip install --upgrade --no-cache-dir --no-deps git+https://github.com/unslothai/unsloth.git
