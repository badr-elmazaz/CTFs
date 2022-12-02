# HttpPingPong

Link: [https://training12.webhack.it/](https://training12.webhack.it/)

I just create with python a small **webserver** using `flask` that returns at `/` endpoint the string **`cG9uZ2FsZnJpLmxpcGFyaUBnbWFpbC5jb20=`** (*base64* encoded). See [`exploit.py`](http://exploit.py) file.

After that I used ngrok to create an **http tunnel** on [localhost](http://localhost) port 6969:

```tsx
ngrok http 6969
```

then I pasted the https link and got the **flag**: `WIT{5949cc987ceb2998f9edeb0f3ebce783}`