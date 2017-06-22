# RedditSwitcharoo V2
What I've been workin' on for the last ~2 months

## Dependencies
 * wget
 * python
 * /bin/bash
 * A mysql server running on "localhost"
   * With the user "auto" (preferably requiring no password)
   * A database called "RedditData"
     * which contains a table called "RedditComments"
       * Must have correct columns
 * Other bash utilities like "cat", "basename", "find", ect...

 ## Files and Directories:
 - [D]Downloaded: Directory for newly downloaded reddit comment files
 - [F]Downloaded/get: A script which downloads the comment files and submission files (latter is currently unused)
 - [D]Downloaded/RS: Directory for submission files
 - [D]Decompressed: Where decompressed reddit comment files go
 - [F]convert.py: Python script which converts JSON files in Decompressed into csv files stored in FormatedConv
 - [F]decompress: Bash script which decompresses reddit comment files in Downloaded into Decompressed
 - [D]FormatedConv: Where csv files are stored
 - [F]convert: Bash script which calls multiple instances of convert.py in parallel
 - [F]upload: Bash script which inserts csv files into database
