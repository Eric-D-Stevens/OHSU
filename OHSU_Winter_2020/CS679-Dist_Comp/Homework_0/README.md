# CS 679 - Homework 0: Getting Set Up
### Eric Stevens

## 1) Logging In

I was able to set up ssh keys so I can log directly into bigbird without a password:

```bash
bash 20:04:11 ~/Desktop/OHSU/OHSU_Winter_2020/CS679-Dist_Comp  (master *) $: 
    ssh bigbird
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-93-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

 * Overheard at KubeCon: "microk8s.status just blew my mind".

     https://microk8s.io/docs/commands#microk8s.status

18 packages can be updated.
17 updates are security updates.

New release '18.04.3 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


*** System restart required ***
Last login: Thu Jan  9 18:59:49 2020 from 10.95.40.35
stevener@bigbird0:~$ 
```

### Question:
**How long has bigbird0 been running since its last?**

To answer this question I ran the `uptime` command:

```bash
stevener@bigbird0:~$ uptime
 20:15:08 up 251 days, 10:57,  2 users,  load average: 0.02, 0.01, 0.00
```

So it appears the system has been running for **251 days, 10 hours and 57 minutes**.


## 2) Finding Data
### Question:
**How many different LDC corpora do we have in** `/l2/corpora/ldc`**?**

Listing the contents of the `/ld/corpora/LDC` directory we get the output:

```bash
stevener@bigbird0:/l2/corpora/LDC$ ls -l
total 524
drwxr-sr-x  3     5009   60029  4096 Sep 10  2008 2004L02
drwxr-sr-x  2 bayesteh student  4096 Jul 28  2016 CHiME
drwxr-sr-x  8     5009   60029  4096 Oct 17  2012 English_Gigaword.v3_proc
-rw-r--r--  1    10962 student 34078 Jan 24  2018 grec
-rw-r--r--  1    10962 student 34078 Jan 24  2018 grep
drwxr-sr-x  2     5009   60029  4096 Oct 17  2012 hub4-awol
drwxr-sr-x  4     5009   60029  4096 Oct  7  2010 LDC1998T31
drwxr-sr-x  6     5009   60029  4096 Oct 17  2012 LDC2000S86
drwxr-sr-x  4     5009   60029  4096 Apr 24  2008 LDC2000S92
drwxr-sr-x  3     5009   60029  4096 Jun  9  2009 LDC2000T44
drwxr-sr-x  6     5009   60029  4096 Oct 17  2012 LDC2000T46
drwxr-sr-x  4     5009   60029  4096 Oct 17  2012 LDC2000T48
drwxr-sr-x  3     5009   60029  4096 Oct 17  2012 LDC2000T50
drwxr-sr-x  5     5009   60029  4096 Apr 24  2008 LDC2001S13
drwxr-sr-x  5     5009   60029  4096 Apr 24  2008 LDC2001S15

...

dr-xr-xr-x 26     5009   60029  4096 Oct 30  2013 LDC97S62
drwxr-sr-x  4    10865 student  4096 Jan 28  2016 LDC97T14
drwxr-sr-x 14     5009   60029  4096 Oct 17  2012 LDC97T22
drwxr-sr-x  5     5009   60029  4096 Apr 24  2008 LDC98S71
drwxr-sr-x  4     5009   60029  4096 Apr 24  2008 LDC98T28
drwxr-x--- 34     5009   60029  4096 Jul 31  2009 LDC99S79
drwxr-sr-x  9     5009   60029  4096 Apr 24  2008 LDC99S82
drwxr-sr-x  2     5009   60029  4096 Oct 17  2012 links_kmh
drwxr-xr-x  4     5009   60029  4096 Oct 26  2010 macrophone
drwxr-sr-x  7     5009   60029  4096 Feb 18  2010 MALACH_ENG
drwxr-sr-x  4     5009   60029  4096 Feb 25  2013 old
-rwxr-xr-x  1     5009   60029  1808 Mar 26  2014 readme
drwxr-sr-x  2     5009   60029  4096 Oct 17  2012 swb-awol
drwxr-sr-x  2     5009   60029  4096 Apr 17  2013 tarfiles
```

Assuming that the directories that are prepended with `LDC` are the corpora, then we can use the `grep` with a count option to get the number of corpora:

```bash
stevener@bigbird0:/l2/corpora/LDC$ ls -l | grep -c LDC
102
```

So it appears that **there are 102 LDC corpora** in the `/l2/corpora/ldc` directory.

### Question: Pack any corpus

I stumbled across a folder containing some video files that intrigued me. The directory is located at:

```
bigbird0:/l2/corpora/IDS/IntuitiveTrip2007/videos
``` 
The contents of this video directory looked like this:

```
-rwxr-xr-x 1 5009 60029 3667562 Apr 25  2008 B_Suturing_1_capture1.avi
-rwxr-xr-x 1 5009 60029 3519102 Apr 25  2008 B_Suturing_1_capture2.avi
-rwxr-xr-x 1 5009 60029 2074932 Apr 25  2008 B_Suturing_2_capture1.avi
-rwxr-xr-x 1 5009 60029 1987516 Apr 25  2008 B_Suturing_2_capture2.avi
-rwxr-xr-x 1 5009 60029 2042886 Apr 25  2008 B_Suturing_3_capture1.avi
-rwxr-xr-x 1 5009 60029 1954368 Apr 25  2008 B_Suturing_3_capture2.avi
-rwxr-xr-x 1 5009 60029 2087098 Apr 25  2008 B_Suturing_4_capture1.avi
-rwxr-xr-x 1 5009 60029 1969368 Apr 25  2008 B_Suturing_4_capture2.avi
-rwxr-xr-x 1 5009 60029 1976614 Apr 25  2008 B_Suturing_5_capture1.avi
...

```

I needed to discover what these video files contained. I was delighted to find that `ffmpeg` was installed on the bigbird, but when using `ffplay` it was very interesting to see how `ffmpeg` attempted to produce the video on the command line using mono-spaced color characters and backgrounds. While I found this impressive, and didn’t know `ffmpeg` would do this, it was impossible to make out the video.

<img src=FFPLAY.png>

![](FFPLAY.png)


#### 1) What kind of data does it contain?



