# FRSS

Date: 21/05/2023

### Tool used:

- Burpsuit
- https://webhook.site

Getting the website we get:

![Untitled](FRSS%20e1cf7dd7df834fdfb20ff35a729b9106/Untitled.png)

As the name of the ctf is FRSS maybe it is a hint of the type of vulnerability may be SSRF?

I analysed by the help of `ChatGPT` what is that code leak:

```markdown
The provided code is written in PHP and makes use of the `cURL` library to send HTTP requests. Here's a breakdown of what each line does:

`$x = curl_init($url);`  
This line initializes a new cURL session and sets the URL of the session to the value of `$url`. 

`curl_setopt($x, CURLOPT_REDIR_PROTOCOLS, CURLPROTO_HTTP);`  
This line sets an option for the cURL session. The option `CURLOPT_REDIR_PROTOCOLS` defines which protocols are allowed in a redirection. By setting this option to `CURLPROTO_HTTP`, it means that only HTTP redirections are allowed.

`curl_setopt($x, CURLOPT_PROTOCOLS, CURLPROTO_HTTP);`  
This line sets another option for the cURL session. The option `CURLOPT_PROTOCOLS` defines the protocols that libcurl may use in the transfer. By setting this option to `CURLPROTO_HTTP`, it means that only HTTP is allowed for the transfer.

`curl_setopt($x, CURLOPT_MAXREDIRS, 1);`  
This line sets yet another option for the cURL session. The option `CURLOPT_MAXREDIRS` sets the maximum amount of HTTP redirections to follow. By setting this to 1, it means that cURL will stop if it encounters more than one redirect.

`echo curl_exec($x);`  
Finally, this line executes the cURL session and outputs the result. The `curl_exec()` function will return the result of the transfer as a string on success, `FALSE` on failure.

In summary, this script is designed to initialize a cURL session to a given `$url`, allow only HTTP protocol and a maximum of one redirect, then execute the request and display the result.
```

Ok so it is an http client library for PHP and it is set to be used with one max redirect and it can use only http protocol (so no `file:///` or `gophere://`) then I tried to:

- find known vulnerability of cURL library (even if I don’t know the version used) → nothing interesting

As suggested by the webpage the flag is named `hehe.txt` so I tried to:

```
GET /hehe.txt HTTP/2
```

But I received a `403 Forbidden` status code, so we are not authorized to get that resource, the important is that we know it exists. 

Then I started to FUZZ the unique surface attack: `Enter URL` input.

First I tried to use a webhook using [`https://webhook.site/`](https://webhook.site/) just to know some headers used and other recon stuff, but I got this:

```html
HTTP/2 200 OK
Content-Type: text/html; charset=UTF-8
Date: Sun, 21 May 2023 03:07:26 GMT
Server: Apache/2.4.25 (Debian)
Vary: Accept-Encoding
X-Powered-By: PHP/7.0.33
Content-Length: 757

<!DOCTYPE html>
<html>
<head>
	<title>FRSS</title> 
</head>
<body>
	<form method="post">
		<label for="url">Enter URL:</label>
		<input type="text" id="url" name="url">
		<button type="submit">Submit</button>
	</form>

	<code>
        <pre style="font-family: monospace; font-size: 16px;">
        hmmm, I just got a code leak like this

            $x = curl_init($url);
            curl_setopt($x, CURLOPT_REDIR_PROTOCOLS, CURLPROTO_HTTP);
            curl_setopt($x, CURLOPT_PROTOCOLS, CURLPROTO_HTTP);
            curl_setopt($x, CURLOPT_MAXREDIRS, 1);

            echo curl_exec($x);
        </pre>
	</code>
</body>
</html>

<img src="https://i.pinimg.com/564x/3c/94/47/3c9447a09860e79e07e0b70928072f30.jpg">Oh no no, url is too long I can't handle it
```

I got this interesting message: `Oh no no, url is too long I can't handle it` so there is max string input, ok perfect I have to deal also with this. But I need to know the max chars that I can send and after some trials I found that the max number is `16`.

Then I tried some tests:

- I used a `short` link just to know what will return: I insert [http://x.com](http://x.com) and the output was as I expected the content of that webpage
- Then I tried to know if the schame section was needed if not this will help us giving us more chars to digit: I insert [x.com](http://x.com) and it worked

Now I have all the necessary I used [localhost](http://localhost) to try to get the file I hoped it used the `same port`:

- [`localhost/hehe.txt](http://localhost/hehe.txt)` → too long >16
- `0.0.0.0/hehe.txt` → it worked and I got the flag, which means the process was hosted on `all interfaces` at `port 80`.

**Flag** `dead{Ashiiiibaaa_you_hAv3_Pybass_chA11}`