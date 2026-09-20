# Interactive Prototyping: The Clock of Pi
**NAMES OF COLLABORATORS HERE**


**Jindi Chai & Yilin Wu**

Does it feel like time is moving strangely during this semester?

For our first Pi project, we will pay homage to the [timekeeping devices of old](https://en.wikipedia.org/wiki/History_of_timekeeping_devices) by making simple clocks.

It is worth spending a little time thinking about how you mark time, and what would be useful in a clock of your own design.

**Please indicate anyone you collaborated with on this Lab here.**
Be generous in acknowledging their contributions! And also recognizing any other influences (e.g. from YouTube, Github, Twitter) that informed your design. 

## Prep

1. ### Set up your Lab 2 Github

At the start of lab Wednesday, ensure you have the latest lab content by updating your forked repository. 

**📖 [Follow the step-by-step guide for safely updating your fork](pull_updates/README.md)**

This guide covers how to pull updates without overwriting your completed work, handle merge conflicts, and recover if something goes wrong.


2. ### Get Kit and Inventory Parts
Take inventory of the kit parts that you have, and note anything that is missing:

***Update your [parts list inventory](partslist.md)***

3. ### Prepare your Pi for lab this week
[Follow these instructions](prep.md) to download and burn the image for your Raspberry Pi before lab Wednesday.




## Overview
For this assignment, you are going to 

A) [Connect to your Pi](#part-a)  

B) [Try out cli_clock.py](#part-b) 

C) [Set up your RGB display](#part-c)

D) [Try out clock_display_demo](#part-d) 

E) [Modify the code to make the display your own](#part-e)

F) [Make a short video of your modified barebones PiClock](#part-f)

G) [Sketch and brainstorm further interactions and features you would like for your clock for Part 2.](#part-g)

## The Report
This readme.md page in your own repository should be edited to include the work you have done. You can delete everything but the headers and the sections between the \*\*\***stars**\*\*\*. Write the answers to the questions under the starred sentences. Include any material that explains what you did in this lab hub folder, and link it in the readme.

Labs are due on Sunday midnight. Make sure this page is linked to on your main class hub page.

## Part A. 
### Connect to your Pi
Just like you did in the lab prep, ssh on to your pi. Once you get there, create a Python environment (named venv) by typing the following commands.

```
ssh pi@<your Pi's IP address>
...
pi@raspberrypi:~ $ python -m venv venv
pi@raspberrypi:~ $ source venv/bin/activate
(venv) pi@raspberrypi:~ $ 

```
### Setup Personal Access Tokens on GitHub
Set your git name and email so that commits appear under your name.
```
git config --global user.name "Your Name"
git config --global user.email "yourNetID@cornell.edu"
```

The support for password authentication of GitHub was removed on August 13, 2021. That is, in order to link and sync your own lab-hub repo with your Pi, you will have to set up a "Personal Access Tokens" to act as the password for your GitHub account on your Pi when using git command, such as `git clone` and `git push`.

Following the steps listed [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) from GitHub to set up a token. Depends on your preference, you can set up and select the scopes, or permissions, you would like to grant the token. This token will act as your GitHub password later when you use the terminal on your Pi to sync files with your lab-hub repo.


## Part B. 
### Try out the Command Line Clock
Clone your own lab-hub repo for this assignment to your Pi and change the directory to Lab 2 folder (remember to replace the following command line with your own GitHub ID):

```
(venv) pi@raspberrypi:~$ git clone https://github.com/<YOURGITID>/Interactive-Lab-Hub.git
(venv) pi@raspberrypi:~$ cd Interactive-Lab-Hub/Lab\ 2/
```
Depends on the setting, you might be asked to provide your GitHub user name and password. Remember to use the "Personal Access Tokens" you just set up as the password instead of your account one!

Check if the directory has clone sucessfully, you should see the Interactive-Lab-Hub under the home directory listed:
```
(venv) pi@raspberrypi:~ $ ls
Bookshelf      Documents            Music     Public                 venv
create_img.sh  Downloads            pi-apps   screen_boot_script.py  Videos
Desktop        Interactive-Lab-Hub  Pictures  Templates
(venv) pi@raspberrypi:~ $
```


Install the packages from the requirements.txt and run the example script `cli_clock.py`:

```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ pip install -r requirements.txt
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ python cli_clock.py 
02/24/2021 11:20:49
```

The terminal should show the time, you can press `ctrl-c` to exit the script.
If you are unfamiliar with the Python code in `cli_clock.py`, have a look at [this Python refresher](https://hackernoon.com/intermediate-python-refresher-tutorial-project-ideas-and-tips-i28s320p). If you are still concerned, please reach out to the teaching staff!


## Part C. 
### Set up your RGB Display
We have asked you to equip the [Adafruit MiniPiTFT](https://www.adafruit.com/product/4393) on your Pi in the Lab 2 prep already. Here, we will introduce you to the MiniPiTFT and Python scripts on the Pi with more details.

<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="200" />

The Raspberry Pi 5 has a variety of interfacing options. When you plug the pi in the red power LED turns on. Any time the SD card is accessed the green LED flashes. It has standard USB ports and HDMI ports. Less familiar it has a set of 20x2 pin headers that allow you to connect a various peripherals.

<img src="https://maker.pro/storage/g9KLAxU/g9KLAxUiJb9e4Zp1xcxrMhbCDyc3QWPdSunYAoew.png" height="400" />

To learn more about any individual pin and what it is for go to [pinout.xyz](https://pinout.xyz/pinout/3v3_power) and click on the pin. Some terms may be unfamiliar but we will go over the relevant ones as they come up.

### Hardware (you have already done this in the prep)

From your kit take out the display and the [Raspberry Pi 5](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.raspberrypi.com%2Fproducts%2Fraspberry-pi-5%2F&psig=AOvVaw330s4wIQWfHou2Vk3-0jUN&ust=1757611779758000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCPi1-5_czo8DFQAAAAAdAAAAABAE)

Line up the screen and press it on the headers. The hole in the screen should match up with the hole on the raspberry pi.

<p float="left">
<img src="https://cdn-learn.adafruit.com/assets/assets/000/087/539/medium640/adafruit_products_4393_quarter_ORIG_2019_10.jpg?1579991932" height="200" />
<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/861/original/adafruit_products_image.png" height="200">
</p>

### Testing your Screen

The display uses a communication protocol called [SPI](https://www.circuitbasics.com/basics-of-the-spi-communication-protocol/) to speak with the raspberry pi. We won't go in depth in this course over how SPI works. The port on the bottom of the display connects to the SDA and SCL pins used for the I2C communication protocol which we will cover later. GPIO (General Purpose Input/Output) pins 23 and 24 are connected to the two buttons on the left. GPIO 22 controls the display backlight.

To show you the IP and Mac address of the Pi to allow connecting remotely we created a service that launches a python script that runs on boot. For the following steps stop the service by typing ``` sudo systemctl stop piscreen.service --now```. Othwerise two scripts will try to use the screen at once. You may start it again by typing ``` sudo systemctl start piscreen.service --now```

We can test it by typing 
```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ python screen_test.py
```

You can type the name of a color then press either of the buttons on the MiniPiTFT to see what happens on the display! You can press `ctrl-c` to exit the script. Take a look at the code with
```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ cat screen_test.py
```

#### Displaying Info with Texts
You can look in `screen_boot_script.py` for how to display text on the screen!

#### Displaying an image

You can look in `image.py` for an example of how to display an image on the screen. Can you make it switch to another image when you push one of the buttons?

\*\*\***Include a picture of your own Raspberry Pi displaying the piscreen.service with your unique MAC address. Additionally, please provide another picture showing the successful completion of the screen test.**\*\*\*
<img width="2645" height="1843" alt="e6de645b25aa4a8320fba6bc3b0bba7c" src="https://github.com/user-attachments/assets/572a2b2e-6b00-41b4-99a7-94da4ed19a3f" />


<img width="2557" height="1624" alt="4fea6521147cb249e7227f6c6aab865b" src="https://github.com/user-attachments/assets/495dbdfd-f58e-4145-9a3d-b0c575920b4a" />


<img width="2383" height="1750" alt="c8b62dea9fd200708c77305ffa7b5823" src="https://github.com/user-attachments/assets/e70b1679-0854-4d72-9922-b1635d295edf" />


<img width="2613" height="1592" alt="b7b6420a83795f2cba0a3dd014d23283" src="https://github.com/user-attachments/assets/bd5a7d0d-91c9-40d7-ab21-5fb5f42d2fc5" />


<img width="2291" height="1659" alt="3704973567fc5eda053c05b3dcc4b13f" src="https://github.com/user-attachments/assets/d46d3679-75ce-4c42-99b1-3dda1f18e18f" />



## Part D. 
### Set up the Display Clock Demo
Work on `screen_clock.py`, try to show the time by filling in the while loop (at the bottom of the script where we noted "TODO" for you). You can use the code in `cli_clock.py` and `stats.py` to figure this out.

### How to Edit Scripts on Pi
Option 1. One of the ways for you to edit scripts on Pi through terminal is using [`nano`](https://linuxize.com/post/how-to-use-nano-text-editor/) command. You can go into the `screen_clock.py` by typing the follow command line:
```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ nano screen_clock.py
```
You can make changes to the script this way, remember to save the changes by pressing `ctrl-o` and press enter again. You can press `ctrl-x` to exit the nano mode. There are more options listed down in the terminal you can use in nano.

Option 2. Another way for you to edit scripts is to use VNC on your laptop to remotely connect your Pi. Try to open the files directly like what you will do with your laptop and edit them. Since the default OS we have for you does not come up a python programmer, you will have to install one yourself otherwise you will have to edit the codes with text editor. [Thonny IDE](https://thonny.org/) is a good option for you to install, try run the following command lines in your Pi's ternimal:

  ```
  pi@raspberrypi:~ $ sudo apt install thonny
  pi@raspberrypi:~ $ sudo apt update && sudo apt upgrade -y
  ```

Now you should be able to edit python scripts with Thonny on your Pi.

Option 3. A nowadays often preferred method is to use Microsoft [VS code to remote connect to the Pi](https://www.raspberrypi.com/news/coding-on-raspberry-pi-remotely-with-visual-studio-code/). This gives you access to a fullly equipped and responsive code editor with terminal and file browser.  

Pro Tip: Using tools like [code-server](https://coder.com/docs/code-server/latest) you can even setup a VS Code coding environment hosted on your raspberry pi and code through a web browser on your tablet or smartphone! 


<img width="2835" height="1964" alt="a09051c5ef35e71c45f99326d01335e7" src="https://github.com/user-attachments/assets/ff1a3005-ddf4-4057-9249-25a73a03bc7e" />



## Part E. Read Part 2. Sketch and brainstorm further interactions and features you would like for your clock.

One potential source of ideas might be thinking about other clocks and timekeeping devices for inspiration.

Another might be novel units of time. How do you measure a year? [In daylights? In midnights? In cups of coffee?](https://www.youtube.com/watch?v=wsj15wPpjLY)

We strongly discourage literal digital or analog clock display: Be creative.


** Insert ideas, sketches, [Verplank diagrams](https://ccrma.stanford.edu/courses/250a-fall-2004/IDSketchbok.pdf)), storyboards for your ideas **


I want to create a clock related to dogs and dog walking. Since I have a dog myself, walking and playing with my dog have always been a very important part of our daily routine. I don’t want to use the traditional hour-and-minute format; instead, I want the current time to be reflected through changes in the dog’s activity levels throughout the day. When there’s still a long time until the next walk, the dog on the screen will be sleeping or resting; as walk time gradually approaches, the dog will wake up and start paying attention to its surroundings; when it’s almost time for a walk, it will become excited, and paw prints will appear; if it’s past the usual walk time, the dog will appear to be waiting or getting anxious. The specific visual presentation still needs to be tested, as I’m not sure whether the Raspberry Pi’s LED screen can display images or emojis, or if it’s limited to text. I may make adjustments based on the results of future testing. Since the LED display has two interactive buttons, I plan to add several different interfaces. Users can use one button to log a completed walk, while the other button allows them to switch between viewing data at different scales—such as how many times they’ve walked the dog today, how many walks have been completed this year, and the total distance the owner and dog have walked together over the past year.


**Sketches & Storyboard**
<img width="947" height="718" alt="截屏2026-09-13 16 20 39" src="https://github.com/user-attachments/assets/76ef7972-78d2-4ec4-917e-7519ec54ce36" />


**Verplank Diagrams**
<img width="1004" height="483" alt="截屏2026-09-13 16 21 14" src="https://github.com/user-attachments/assets/5abc1472-745f-4ccc-bae1-e65847957f2b" />



**Put the names of the people you gave feedback to here. (Even better, add links to their repos here!)**
https://github.com/SinaL0123/Interactive-Lab-Hub/tree/Fall2026/Lab%202


https://github.com/zg375/Interactive-Lab-Hub/tree/86dc14dd4b592afbeb4f4187617a6ae88da5ad3f/Lab%202


https://github.com/bh654-dev/Interactive-Lab-Hub/blob/Fall2026/Lab%202/README.md


https://github.com/Afrozaktar/Interactive-Lab-Hub/blob/Fall2026/Lab%202/README.md



# Lab 2 Part 2

## Prep 

1. Pick up remaining parts for kit on Wednesday lab class. Check the updated [parts list inventory](partslist.md) and let the TA know if there is any part missing.

2. Look at and give feedback on the Part E. for at least 3 other people in the class and get 3 people to comment on your Part E!)
**Put the feedback for your ideas here.**



(1) I really like your idea of showing time through the dog’s behavior! I was wondering what would happen in special situations though—like if the dog is sick, the weather is bad, or you just can’t go for a walk that day. Maybe there could be an option to skip or postpone the walk, so the dog doesn’t keep looking anxious 😭 Also, are the usual walking times preset by the user? I feel like weekday and weekend schedules could be different, since people might walk their dog at different times when they don’t have work.



(2) I really like the dog walking clock idea because it connects time with a real daily routine instead of just showing hours and minutes. The different dog behaviors, like sleeping, waking up, and getting excited, make it easy to understand how close it is to walk time. I also think using the buttons to log walks and check walking data is a nice way to make the clock more interactive. One suggestion would be to make the dog’s different states visually very clear, maybe by using simple icons or different background colors, so users can quickly understand what each state means.



(3) I really like the dog walking clock idea because it connects time with a real daily routine instead of just showing hours and minutes. The different dog behaviors, like sleeping, waking up, and getting excited, make it easy to understand how close it is to walk time. I also think using the buttons to log walks and check walking data is a nice way to make the clock more interactive. One suggestion would be to make the dog’s different states visually very clear, maybe by using simple icons or different background colors, so users can quickly understand what each state means.



(4) Your dog walking clock idea is really creative. Tying the display to your dog's behavior states instead of a literal hour minute readout is very creative. It's also grounded in something personal and real (your own routine with your dog), which makes it more meaningful.
Since you mentioned uncertainty about whether the screen can show images/emojis vs. just text, it might help to do a quick screen capability test early so your concept doesn't have to change last-minute.
## Update your Lab Hub

[Update your Lab Hub](pull_updates/README.md) to get the latest content and requirements for Part 2.

## Modify the barebones clock to make it your own

Start small, pick just one element of your overall idea, just to show you have a handle on the code and components.

\*\*\***Put a copy of your code in your Lab 2 Github repo.**\*\*\*

## Make a short video of your modified barebones PiClock

\*\*\***Take a video of your barely modified PiClock.**\*\*\*

After you edit and work on the scripts for Lab 2, the files should be upload back to your own GitHub repo! You can push to your personal github repo by adding the files here, commiting and pushing.

```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ git add .
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ git commit -m 'your commit message here'
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ git push
```

After that, Git will ask you to login to your GitHub account to push the updates online, you will be asked to provide your GitHub user name and password. Remember to use the "Personal Access Tokens" you set up in Part A as the password instead of your account one! Go on your GitHub repo with your laptop, you should be able to see the updated files from your Pi!

## Now, make your own PiClock

Do take advantage of having done the previous iteration to refine and simplify your design.

** Insert any updates ideas, sketches, [Verplank diagrams](https://ccrma.stanford.edu/courses/250a-fall-2004/IDSketchbok.pdf))!, storyboards for your ideas **


### Ideas

After listening to our classmates’ comments and suggestions, we decided to keep improving our Dog Walk Clock. Based on our original demo, we added some new features to solve problems we noticed in the current design. Different dogs can have different walking routines. Some dogs may need several walks every day, while others may only need one or two. We added a customizable walk schedule, so users can change the clock settings through the computer. They can reduce the number of walks or set different walking times for weekdays and weekends based on their daily routine.

We also added a speaker to the clock. When it reaches a scheduled walking time, the dog will make a barking sound to remind the owner that it is time for a walk. Compared with the silent visual reminder on the LED screen, the sound can work more clearly like an alarm. We also slightly changed the visual environment on the screen. The background color changes at different times of the day to represent changes in the environment. Finally, we added a missed-walk correction feature. If the user cannot walk the dog on time, or forgets to press the button after the walk, they can correct it later without affecting the rest of the clock.


### Sketches & Storyboard
<img width="1079" height="714" alt="截屏2026-09-20 14 59 55" src="https://github.com/user-attachments/assets/aff6ee62-a817-47f1-976d-3fe34e8be1d0" />


<img width="1076" height="458" alt="截屏2026-09-20 15 00 07" src="https://github.com/user-attachments/assets/50680d3b-c203-44c5-96e0-267f0992587d" />


### Verplank Diagram
<img width="1040" height="479" alt="截屏2026-09-20 15 02 53" src="https://github.com/user-attachments/assets/fcbbf419-6ab4-4111-a10f-1c56e74c979c" />




\*\*\***Put a copy of your code in your Lab 2 Github repo.**\*\*\*

\*\*\***Take a video of your PiClock.**\*\*\*


As always, make sure you document contributions and ideas from others (and AI) explicitly in your writeup.

You are permitted (but not required) to work in groups and share a turn in; you are expected to make equal contribution on any group work you do, and N people's group project should look like N times the work of a single person's lab.  Make sure the page for the group turn in is linked to your personal Interactive Lab Hub page. 


