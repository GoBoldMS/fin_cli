# Fin CLI

## About
Fin CLI is a versatile command-line tool designed for financial analyses. It enables efficient stock data retrieval from Finzive.com. This tool stands out for its ease of use, comprehensive stock screening options, and simplified easy to use reports.

## Features
- Stock screening with full range of Finzive.com options.
- Fundainsight for in-depth stock analysis.
- Outputs results to a convenient CSV format.

## Quick Start
1. Run `./run.sh` on Linux or `run.bat` on Windows.
2. Select between `fincli` or `fundainsight` and follow the prompts.

## Dependencies
- Python version less than 3.10. (Specify why this version is necessary if applicable.)

## Installation and Running
Clone the repository and navigate to the project directory:
git clone [repository-link]
cd fin_cli
If the main script doesn't work, install the necessary libraries:
pip install -r requirements.txt

## Usage
### Fincli
- Use `--history` or `--hist` to apply filters from recent searches.
- `--debug` for detailed logging.

### Fundainsight
- Includes all Fincli flags.
- `--set-filters` to specify filters.
- `--scrape-link` to set the scrape link (must include all filters from Finzive).

## Contributing
We welcome contributions! Please refer to our contribution guidelines for more information on how you can contribute to the project.

## Authors
- Yonatan Levin - Initial work

## License
This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to customize and expand this template to fit the specific needs and nuances of your project.
