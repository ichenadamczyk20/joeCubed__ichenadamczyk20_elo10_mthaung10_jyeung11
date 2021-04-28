Collected Knowledge & Wisdom on
# Media Wiki API
---
## Provides:
This API provides read access, write access, searching, etc. for any Wikimedia wiki (including Wikipedia).


### Pain factor: 4
(0=ezpz...5=nightmare)

### Key Provisioning:     
- For read-only requests, you do not need a key.
- For data-modifying requests, you first need an account with MediaWiki. You then use that account to register a username and password for your bot at https://www.mediawiki.org/wiki/Special:BotPasswords. In your Python code, you request a login token from the api endpoint, and then send another request with Python to login with that login token and with the username and password for your bot. (See https://www.mediawiki.org/wiki/API:Login for more detailed information and code snippets.)

### Quotas:
- Generally, there is no quota for read-only requests, though it is understood that your access might be terminated if you send too many requests at once.
- There are quotas for actions that aren't read-only — the quotas for such actions on Wikipedia can be viewed here: https://en.wikipedia.org/w/api.php?action=query&format=json&meta=userinfo&uiprop=ratelimits

---

## The Good:
- Documentation provides code snippets and response examples for the actions!
- Access to Wikipedia!
## The Bad:
- Nothing really...
## The Ugly:
- The documentation can be long and confusing to scroll through at times. Kinda daunting to use an API that accesses all of Wikipedia, though actually it's not as bad as one might think.
- The returned data can also be complicated because of the nesting dictionaries and lists, though the documentation provides nicely-formatted example responses.
- The code snippets in the documentation use the `requests` module instead of the `urllib` module.


**Location:** Documentation and table of major Wikimedia Wiki Endpoints can be viewed here: https://www.mediawiki.org/wiki/API:Main_page  
The English Wikipedia API endpoint is https://en.wikipedia.org/w/api.php

---

Accurate as of (last update):    2021-04-27

Contributors:

Ian Chen-Adamczyk, pd1  