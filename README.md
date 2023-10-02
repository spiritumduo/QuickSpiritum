# QuickSpiritum
A collection of functionality to speed up daily clinical admin tasks

## How to use
1. Place docx with placeholders into a locations folder eg 'Salisbury' in the **/requests/templates/** folder


## Quick Story

Hello fellow clinicians-who-code,

Having just moved to a new trust that has a lot of paper based request forms, that need to be printed off, stored, found, filled in, posted or emailed, I thought I would build a work around (something I seem to do often in the NHS!). Hence Quick Spiritum 2.0 was born (still in the neonatal stage). Quick Spiritum 1.0 (which I have spoken about before, see QS 1.0) was built with the open source robotic process automation (RPA) scripting language AutoHotKey.

As I am in a new trust, and QS 1.0 would not be interacting with the same digital systems in the new trust (and I could not install AutoHotKey without admin rights), I thought I would build QS 2.0 to be even more “open source” (if that is possible). So, I borrowed some NHS Digital HTML, CSS and javascript, threw together a Flask web app and a python backend to digitise the paper forms for clincial requests. It works a charm, for myself, on my desktop.
Here are some screen shots from the web app.

Index page
![Alt text](<images/image 1 - index.png>)

2364×1380 168 KB
Data collection page (top)
Screenshot 2023-09-19 at 19.55.04
Screenshot 2023-09-19 at 19.55.04
2314×1380 175 KB
Data collection page (bottom)
Screenshot 2023-09-19 at 19.55.17
Screenshot 2023-09-19 at 19.55.17
2344×1286 203 KB
Submitted page
Screenshot 2023-09-19 at 19.55.26
Screenshot 2023-09-19 at 19.55.26
2336×1112 152 KB
The code can be viewed on GitHub 1. It is in no way finished, but I thought I would share what I have so far, and see if anyone else wanted to have this functionality. If I was to run this as a service, I still need to do:

Unit testing
Integration testing
Documentation
DCB0129 and DCB160 (I am actually looking forward to using @pacharanero’s Cookie Cutter 1 on this one)
Build an web server (eg NGINX)
Host on a server
It might even need Medical Device sign off it it was used across more than one site (I might be opening up a huge debate here).
All of the above is very doable, but I am doing this all in my own time, so it will take some time to complete (having only just started 1.5 weeks ago, hence neonatal stage). I have however been wet running QS 2.0 today to create lung function requests for my clinic patients, all looking good.

Now what is so interesting about this new app I hear you say? Well I think it is the fact that you can ask anyone to just hand you a word document (in .docx format) with some placeholders in the places that you want data filled in, and then it creates a PDF for you with the data you input on the web app and then emails it to the department that then carriers out the clinical request. So a low code functionality for he end user for when ever they want to add a new request form or update an old one. The web app front end reads the docx file and creates the webpage from it, so no need to recode the web app for new request forms!

“template” for Lung Function Requests
Screenshot 2023-09-19 at 20.05.21
Screenshot 2023-09-19 at 20.05.21
1462×1368 262 KB
PDF output
Screenshot 2023-09-19 at 20.13.39
Screenshot 2023-09-19 at 20.13.39
1182×1384 126 KB
One major component with this system that is not complete is that I have not figured out yet how to automate sending emails via an NHS mail account. I have previously used the python exchangelib to send emails via NHS mail, but this was around 3 years ago. I think this was before OAuth was introduced. I can no longer get pass checking credentials. I think I need to get some OAuth credentials, and I have asked my local digital team for this, but I have not heard any thing back yet. I have read from NHS Digital as well that you might have to get an application email account, with a 20 character password, and then you can use SMTP.

I would appreciate help from anyone that has automated the sending of emails via NHS mail, especially via a python script. If not python, then something command line based (Quick Spiritum runs in a docker container, and I have decided to stay away from Graphical User Interfaces).

Also, if anyone wants to use, or get involved with the build of QS 2.0, it could be an interesting collaboration.

