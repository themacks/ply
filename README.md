# Ply
Ply is an HLS server for the [HDHomeRun Plus](http://www.silicondust.com/products/hdhomerun/hdhomerun/), also known as the HDTV-2US. 
It is specifically designed for streaming to the Roku 3 using the [roku-hdhomerun](https://github.com/computmaxer/roku-hdhomerun) app.

## Dependencies
 * [hdhomerun_config](http://www.silicondust.com/support/hdhomerun/downloads/) SiliconDust utility for finding devices on network
 * [web.py](http://webpy.org/) python webserver
 * ffmpeg

## Setup
 * Checkout ply to directory of your choice
 * Checkout web.py to ply/webpy or install system wide
 * Start ply with 'python ply.py [port]'
 * Navigate to 'localhost:[port]/setup' to initialize the database
 * Navigate to 'localhost:[port]' and select channel icons
 * Point roku-hdhomerun to ply as a wallop server