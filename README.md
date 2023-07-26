# Version: [Python 3.8](https://www.python.org/downloads/release/python-380/)
# [Preview of turbo](https://streamable.com/nfqpgv) | Contact: [telegram](https://t.me/misinput) for more info
## How to use this tool
### 1. Get accounts
  - This is the most obvious step
### 2. Configuration
   - Edit the data/configuration.json file to something like this
```json
{
    "gamertagSystem": "old",
    "auth": "accounts",
    "accounts": "accounts.txt"
}
```
   - gamertagSystem decides whether you use the classic gamertag system which is `old` or the new one which is `new` 
   - auth decides whether you're using account credentials which is `accounts` or jwt `tokens`
   - accounts decides what path the accounts are in Example: `C:\Users\Mike\turbo\data\accounts.txt`
### 2.1 Configuration - Webhooks
   - You can edit the \_\_init\_\_ method in `util/webhook.py` to send a message after you turboed the tag
```py
self.vars, self.webhooks = vars, [{"url":"https://discord.com/api/webhooks/Example/Example","method":"POST","headers":{},"params":{},"json":{"content":"@everyone","embeds":[{"title":"Successful Turbo!","color":None,"fields":[{"name":"`Gamertag`","value":f"`{vars['tag']}`","inline":True},{"name":"`XUID`","value":f"`{vars['new_account'][1]}`","inline":True},{"name":"`Requests`","value":f"`{vars['requests']}`","inline":True}]}],"attachments":[]},"sucess_code":204}]
```
  ^ Example
### 3. Install requirements
   - Install the requirements whether `python3 -m pip install -r requirements.txt` or `pip install -r requirements.txt`
### 4. Run it
   - Run it either clicking on main.py or `python3 main.py`
   - Type the gamertag you want to turbo and the amount of threads you want to use
