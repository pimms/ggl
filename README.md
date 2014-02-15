ggl
===

Google Custom Search for the command line. The results are displayed 
with Curses.

### Usage
`./ggl.py i am now searching the web`

Unless you hate your life, place the script somewhere in your PATH.



### Dependencies
The dependencies for GGL can be installed via PIP. This may not be the extensive
list of external dependencies. 

`$ sudo pip install google-api-python-client curses`


GGL uses Google's Custom Search API which only gives you one hundred
free searches per day. You have to create a new application on the
Google Developer Console and enable the Custom Search API for this
application. 


### To create an API key
Creating your own API key is unfortunately absolutely required as there is a limit of 100
daily searches for free per API key, and I plan on using all of mine :) If you want more,
the price is $5 for every thousand searches beyond the initial 100. Creating the API key
takes roughly 3 minutes.

1. Go to https://cloud.google.com/console/project and create a new project
2. Click on your newly created project and in the left pane click "APIs and Auth"
3. Find the Custom Search API and click the button to enable it
4. In the left pane, click on the "Credentials" item
5. Click "Create New Key" under the Public API Access pane. Select "Browser Application" and leave the text field empty.
6. Your newly created API key can now be used with GGL (or anything else)


### To create a custom search engine
The default Search Engine ID is configured exactly as written above, but create
your own if you want to customize your results even more. 

1. Go to https://www.google.com/cse/ and click the "Add" button
2. In the "Sites to Search" field, enter any URL - YOU WILL REMOVE IT LATER!
3. Click "Create", and on the next page click the "Control Panel" button
4. Change the "Sites to Search" option to "Search the entire web..." and remove the URL you added in step 2
5. From the control panel, click the "Get Code" button. Your Search Engine ID can be found on line 3 of the JS snippet.

### Configure your stuff
The configuration file contains some fields which must, and some which should be configured by you.

#####[api] api_key (REQUIRED)
The API-key created in the Google Developer Console

#####[api] search_engine (REQUIRED)
The ID of the CSE created as described above, or use the default value (mine). 

#####[cmd] open_url_cmd (REQUIRED)
The command that will be used to open the URL retrieved from Google. Defaults go `gnome-open`. The URL
is passed as the sole parameter to the application.

#####[cmd] cmd_out_redirect
Where to redirect the output (STDOUT and STDERR) from `open_url_cmd` and `post_cmd`.

#####[cmd] post_cmd
Command that is executed after the URL has been opened. Should be used to give your browser focus. This option
is *extremely* awesome with the `i3 WM` if you always have your browser in the same workspace. If your browser
is opened in workspace 2: `post_cmd: i3 workspace2`.   
