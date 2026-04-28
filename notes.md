# Notes 

## **requests**
2 fetch data from the internet - allows code to send a message to a server and ask for information.
in project -> 2 pull *JSON* data from the 3 APIs and download the raw HTML code from the 3 scraped websites.

response.status_code == **200** # 200 means success. anything else is an error.


## **beautifulsoup4** or **re**
2 extract specific data from messy HTMLs.
turns the HTML into a searchable tree.
in project -> 2 find every <div> with the class *course-title* and return the text inside it.

## **pandas**
data manipulation && storage -> introduces the *DataFrame*, a super-powered spreadsheet that lives inside the code.
in project -> handles the append mode to prevent data overwriting && finds the "3 best courses"

## **matplotlib**
takes arrays of numbers from pandas and converts to pixels.
in project -> 2 generate *Bar Charts, Pie Charts, Line Plots*.

## **tkinter**
2 build the gui.
in project -> buttons, 2 host filters for the recommendation egnine && display of results.

## **schedule**
2 keep a script alive in the backround && wake it up when needed.
in project -> 2 fulfill the *Extensions* requirement && keep data.csv fresh.
