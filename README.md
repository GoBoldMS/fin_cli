# Fin CLI
A simple cli tool for getting stock data from Finzive.com.

Featuring:
  - fincli for stock screening based on all finzive.com options.
  - fundainsight calcutalting and screening stocks based on price/assets ratio

## Quick start

1. ./run.sh for linux or run.bat
2. choose the fincli/fundainsight and fallow the steps.

All outputs are saved to csv file.

### Dependencies

* Python <3.10


### Installing and Running

* If main script is not working run pip install to all the lib in pyproject.toml. 

### Usage

Flags:
  Fincli
    -  '--history','--hist' for using filters of recent search.
    -  '--debug' Display details logging.
  Fundainsight
    -  '--history','--hist' for using filters of recent search.
    -  '--debug' Display details logging.
    -  '--set-filters' Set filters to be used.
    -  '--scrape-link' Set the scrape link to be used. (scrpe link must include all the filters from finzive)

Fundainsight works automaticly.
Fincli will prompt a quarry builder if --history flag is not used.
  
## Contributing

Guidelines for how to contribute to this project.

## Authors

* [GoBoldMS](https://github.com/GoBoldMS) - Initial work

## License

This project is open-source and available under MIT license.
