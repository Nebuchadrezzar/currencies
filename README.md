### currencies

`Usage: currencies.py [-h] [-o [OUTPUT]] [-v]`<br/>

Create a csv of currencies from www.coinbase.com<br/> 

To load these currencies into a sqlite database,
use the following syntax:<br/>
`.import "| tail - n + 2 currencies.csv" mytable`

optional arguments:<br/>
  `-h, --help            show this help message and exit` <br/>
  `-o [OUTPUT], --output [OUTPUT]   Path and Name of a file to direct output.` <br/>
  `-v, --verbose         Print to stdout.` <br/>
  
### rates

`Useage: rates.py [-h] [-s] [-b [CURRENCY CODE]]`<br/>

Create a csv of exchange rates for various currencies. Data drawn from www.fixer.io.<br/>

optional arguments:<br/>
`-s   suppress creating a csv, just print to stdout`<br/>
`-b   supply a base currency code. Default is EUR.` 

Note: You'll need API key in a file called APIKey.ini co-located with the script. 
A free API key affords you only pulling EUR daily rates. A paid account will allow you pass 
in other Base currencies without error.    


  
