### currencies

`Usage: currencies.py [-h] [-o [OUTPUT]] [-v]`<br/>

Create a csv of currencies from www.coinbase.<br/> 

Use:<br/>
`.import "| tail - n + 2 currencies.csv" mytable` to import in sqllite.

optional arguments:<br/>
  `-h, --help            show this help message and exit` <br/>
  `-o [OUTPUT], --output [OUTPUT]   Path and Name of a file to direct output.` <br/>
  `-v, --verbose         Print to stdout.` <br/>
