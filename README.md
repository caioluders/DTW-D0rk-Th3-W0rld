#DTW - D0rk Th3 W0rld

<pre>_____ _________          __
|  __ \__   __\ \        / /
| |  | | | |   \ \  /\  / / 
| |  | | | |    \ \/  \/ /  
| |__| | | |     \  /\  /   
|_____/  |_|      \/  \/</pre>

##What it is ?

An tool that make google dorks available to all command-line programs .

##Why is useful ?

The possibilities are unlimited : you can test an exploit with the dork ; automate attacks ; check which server is up ; etcetera ...

##How it works ?

First the DTW will catch an list of sites with the dork you passed , in Google , after he will execute an command that you specified looping through the list of URLs .

##Example :

`$ python dtw.py --dork="site:.com.br filetype:php intext:Warning:" --cmd="ping -c 1 ^URL^"`

Note that in the parameter "cmd" he will change the "^URL^" to the site n-times .

##Usage :

| Parameters        | Explanation
|-------------------|:----------------------------------:|
|-d, --help         |   show this help message and exit       
|--d DORK, --dork DORK  | The dork to search         
|--cmd CMD |   Command to execute with the URL/IP. Example : --dork="ping -c 5 ^URL^"
|-p PAGES, --pages PAGES |   Number of pages to get from Google
|--delay DELAY    |   Delay time in secs ( Default = 1 s )
|--type TYPE | Determinate the type of the URL output ( url , ip or path )
|--proxy_on | Turn on the proxy list ( dtw_proxy_list.txt )

##Upcoming in next versions :

1. Making the Google Parser better and more efficient , Google Ajax obtains less results and ban easily
2. Working in the Proxies ( identify which was banned , etc )



