ggl
===

Google Custom Search for the command line.

Usage:
`./ggl.py i am now searching the web`
Unless you hate your life, place the script somewhere in your PATH.



Dependencies:

The dependencies for GGL can be installed via PIP. This may not be the extensive
list of external dependencies. 
`$ sudo pip install google-api-python-client curses`

GGL uses Google's Custom Search API which only gives you one hundred
free searches per day. You have to create a new application on the
Google Developer Console and enable the Custom Search API for this
application. 


To create an API key

1. Go to https://cloud.google.com/console/project and create a new project
2. Click on your newly created project and in the left pane click "APIs and Auth"
3. Find the Custom Search API and click the button to enable it
4. In the left pane, click on the "Credentials" item
5. Click "Create New Key" under the Public API Access pane. Select "Browser Application" and leave the text field empty.
6. Your newly created API key can now be used with GGL (or anything else)


To create a custom search engine

1. Go to https://www.google.com/cse/ and click the "Add" button
2. In the "Sites to Search" field, enter any URL - YOU WILL REMOVE IT LATER!
3. Click "Create", and on the next page click the "Control Panel" button
4. Change the "Sites to Search" option to "Search the entire web..." and remove the URL you added in step 2
5. From the control panel, click the "Get Code" button. Your Search Engine ID can be found on line 3 of the JS snippet.


The default Search Engine ID is configured exactly as written above, but use
your own if you want to customize your results even more. :-) 