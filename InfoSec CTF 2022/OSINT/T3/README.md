# T3

**Photo link**:

**Description**: After this photo, we lost him in the park. What is the name of the park? flag{park_name}. For example, if it is Verkių Park the flag will be flag{park_verkių}

The first thing I did is to extract the image metadata using an `exif tool` online.

`Exif`  is a standard for some file **metadata** (camera settings, geolocation etc…) such as images.

For this I used this tool: [https://jimpl.com/](https://jimpl.com/)

The only interesting medata was the date: `December 02, 2022 14:50` so the photo is recent (can find more information)

Then I zoomed the and analyzed well the image searching for signals with street names and so on (the photo is with a good quality). 

I found these interesting information:

1. Name of a signal near a tram stop: **krasickiego** 
2. Name of a store: **bresno**

Then I googled this information and I got this:

![Untitled](T3%20670d7dde0ff04ee0897b4721136d6e15/Untitled.png)

It seemed it was the right park because of the parking the bresno store and the big green park so to check I used Google Street View:

![Untitled](T3%20670d7dde0ff04ee0897b4721136d6e15/Untitled%201.png)

It was the right park.

Got the **flag**: `flag{park_Brzeźnieński}`