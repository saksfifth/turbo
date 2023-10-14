# [Video](https://streamable.com/62pqi5) | [telegram](https://t.me/misinput) for more info
## How to use this tool

### 1. Install requirements
   - Install the requirements whether `python3 -m pip install -r requirements.txt` or `pip install -r requirements.txt`

### 2. Configuration
   - Edit the `data/configuration.json` file to something like this
```json
{
    "gamertagSystem": "old", // old = 15 char tags, new = 12 char tags
    "auth": "accounts", // accounts = account combolist (left@afra.id:lungesgoated)
    "accounts": "data/accounts.txt" // accounts path directory
}
```

### 2.1 Configuration - Webhooks
   - You can edit the \_\_init\_\_ method in `util/webhook.py` to send a message after you turboed the tag
```py
self.vars, self.webhooks = vars, [{"url":"https://discord.com/api/webhooks/Example/Example","method":"POST","headers":{},"params":{},"json":{"content":"@everyone","embeds":[{"title":"Successful Turbo!","color":None,"fields":[{"name":"`Gamertag`","value":f"`{vars['tag']}`","inline":True},{"name":"`XUID`","value":f"`{vars['new_account'][1]}`","inline":True},{"name":"`Requests`","value":f"`{vars['requests']}`","inline":True}]}],"attachments":[]},"sucess_code":204}]
```
  ^ Example

### 3. Run it
   - Run it either clicking on `main.py` or `python3 main.py` 

