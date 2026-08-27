#!/usr/bin/env bash
# Render build command. Runs on every deploy.
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Tailwind's standalone binary needs no Node toolchain. Downloading it at build
# time rather than committing the compiled CSS means the stylesheet can never
# be stale relative to the templates.
TAILWIND_VERSION="${TAILWIND_VERSION:-latest}"
if [ "$TAILWIND_VERSION" = "latest" ]; then
  TAILWIND_URL="https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64"
else
  TAILWIND_URL="https://github.com/tailwindlabs/tailwindcss/releases/download/${TAILWIND_VERSION}/tailwindcss-linux-x64"
fi

curl -sSL -o ./tailwindcss "$TAILWIND_URL"
chmod +x ./tailwindcss
./tailwindcss -i ./static/src/input.css -o ./static/css/site.css --minify
rm -f ./tailwindcss   # ~110 MB; keep it out of the deployed image

python manage.py collectstatic --no-input
python manage.py migrate
