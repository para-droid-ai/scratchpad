cd /app
# sanity view
ls -la

# if there is no compose file here, skip docker; otherwise ensure daemon access
# Linux: fix docker socket perms (requires re-login for group to apply)
sudo usermod -aG docker "$USER" && newgrp docker
# or run docker commands with sudo:
# sudo docker ps

# If you're inside a container and need host docker: mount /var/run/docker.sock or skip docker tasks.

# Use the guarded script and capture logs
bash scripts/remedial_v2.sh | tee error.log