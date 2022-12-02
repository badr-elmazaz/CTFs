# DebugModeHackerino

Link: [https://training13.webhack.it/](https://training13.webhack.it/)

After inspecting the webpage source html (ctrl+u) I found an interesting part:

```tsx
<div>
      <!-- debug mode credentials: demo:base64(demo) -->
      <input type="text" class="form-control" id="user" name="user" placeholder="username">
      <input type="password" class="form-control" id="pass" name="pass" placeholder="password">
      <!--
      <input type="hidden" class="form-control" id="debug_mode" name="debug_mode" placeholder="1" value="0">
      -->
    </div>
```

The developers left the debug credentials commented in the code and the credentials are:

Username: **demo**

Password: base64(demo) ⇒ `echo demo | base64` ⇒ **ZGVtbwo==**

But the input type of this mode is hidden so I **intercepted** the request with **burpsuite** and then set the `debug_mode=1` as following:

```tsx
user=demo&pass=ZGVtbw==&debug_mode=1
```

Then I got the **flag**: `WIT{9c7c3c8afc5df9a7c38bc9ab5b414c10}`

**Notice:**

Firstly I had some troubles with base64(demo), using the CLI to generate the base64 I obtained **ZGVtbwo=** but the server didn’t accept it (maybe there is a direct control without reversing it) using the burpsuite shortcut (ctrl+b) I got **ZGVtbwo==** the correct one that the server accepts. There is no difference fro the two versions in fact **=** is used for **padding**.