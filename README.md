# $PROJ

> $PROJ_DESC

## Links

- [Github]($REPO_URL)

## Prod Setup

### First

```shell
ssh-keygen
# example pub
# paste it to https://github.com/settings/keys
cat .ssh/id_ed25519.pub

ssh -l $USER $IP
# e.g. git@github.com:potykion/wine-wish.git
git clone $REPO_URL_SSH

cd $PROJ
python3 -m venv ".venv"
source ./.venv/bin/activate
pip install -r requirements.txt
# fill env w FLASK_APP=main & FLASK_SECRET=...
nano .env

sudo cp ./example.service /etc/systemd/system/example.service
sudo chmod 644 /etc/systemd/system/example.service
sudo systemctl enable --now example.service

```

### Update

```shell
ssh -l $USER $IP
cd $PROJ
git pull
sudo systemctl restart example.service
```