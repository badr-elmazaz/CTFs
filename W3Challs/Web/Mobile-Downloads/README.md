# Mobile-Downloads

Looking at the webpage, only few link were not dead, one of them return a php code, `/contact.php`

```php
<div class="contenttop">
    <div class="contenttitle">Contact form</div>
</div>
<div class="contentfill">
    <div class="contentinfo">
        <?php
            $host = 'mobile-downloads.hax.w3challs.com';
            $subject = '';
            $message = '';
            $from = '';

            if (isset($_SERVER['HTTP_HOST']))
                $host = htmlentities($_SERVER['HTTP_HOST'], ENT_QUOTES, 'UTF-8');

            $to = 'admin@'.$host;

            if (isset($_POST) &&
                !empty($_POST['mail_from']) &&
                !empty($_POST['mail_subject']) &&
                !empty($_POST['mail_content']) &&
                is_string($_POST['mail_from']) &&
                is_string($_POST['mail_subject']) &&
                is_string($_POST['mail_content']))
            {
                $subject = $_POST['mail_subject'];
                $message = $_POST['mail_content'];
                $from    = $_POST['mail_from'];

                define('message_prefix', 'Mail sent from %s:'."\n".str_repeat('-', 64)."\n");
                $msg = sprintf(message_prefix, $host) . $message;

                $headers = 'From: '.$from."\r\n".
                           'Reply-To: '.$from."\r\n".
                           'X-Mailer: PHP/'.phpversion();

                if (mail($to, $subject, $msg, $headers) === TRUE)
                {
                    printf('<div class="success">The message was sent</div><br />');
                    $subject = '';
                    $message = '';
                    $from = '';
                }
                else
                    printf('<div class="error">The message cannot be sent</div><br />');
            }

            $subject = htmlentities($subject, ENT_QUOTES, 'UTF-8');
            $message = htmlentities($message, ENT_QUOTES, 'UTF-8');
            $from = htmlentities($from, ENT_QUOTES, 'UTF-8');
        ?>

        To contact us, please use the form below and indicate your e-mail address:
        <br /><br />
        <form method="POST" action="">
            <strong>Recipient:</strong><br />
            <?php echo '<span class="spaced">'.$to.'</span>'; ?><br /><br />
            <strong>Your e-mail address:</strong><br />
            <input type="text" size="40" name="mail_from" class="spaced" value="<?php echo $from; ?>" /><br /><br />
            <strong>Subject:</strong><br />
            <input type="text" size="50" name="mail_subject" class="spaced" value="<?php echo $subject; ?>" /><br /><br />
            <strong>Message:</strong><br />
            <textarea name="mail_content" cols="53" rows="15" class="spaced"><?php echo $message; ?></textarea><br /><br />
            <div style="text-align: center"><input type="submit" value="Send" /></div>
        </form>
        <div style="text-align: right">Mail powered by W3Corp™<br /><a href="/mail_src.php">Sources</a></div>
    </div>
</div>
1
```

Analyzing the code first I thought to make some `Host` header **hijacking** without success so after some searches I found that we can **inject** some extra code in the `From` field. In fact studying the mail php function I found that I can inject the **BCC** and **CC** fields to send emails to other people. So I just added at the end of the email the **newline** character and `BCC:other_email`.

```
mail_from=test@example.com%0ABCC:test@test.com&mail_subject=test&mail_content=test
```

Flag: `W3C{3v1l_Sp4m_1s_3v1l}`