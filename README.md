plenty_taxhub_generator
_________________

## Description

Create a Tax Hub Report with sales order and refunds from PlentyMarkets.
Tax Hub is a report used by [DutyPay](https://www.dutypay.eu/de/).

## Installation

`poetry install plenty_taxhub_generator`

or

`python3 -m pip install plenty_taxhub_generator --user --upgrade`

## Usage

Prepare a configuration file with the following format:

```
[General]
base_url=https://{your-plenty-cloud}.plentymarkets-cloud01.com

[Mappings]
referrer_id={IDs of the order origins}
country_id=AT=2,CZ=6,ES=8,FR=10,GB=12,IT=15,PL=23 # list of countries where VAT is charged

[fixed_values]
source_zone=DE
market_zone_currency=EUR
```

And place the config at:
- `/home/user/.plenty_taxhub_generator_config.ini` for Linux systems
- `C:\\Users\user\.plenty_taxhub_generator_config.ini` for Windows systems

Create a API user on PlentyMarkets:
Setup-> Settings-> User-> Accounts-> New-> Access: REST-API

Then just run the program:
`python3 -m plenty_taxhub_generator --from 2020-09-01 --to 2020-09-30`

Please provide the date in one of the following formats:
* YYYY-MM-DDTHH:MM:SS+UTC-OFFSET
* YYYY-MM-DDTHH:MM
* YYYY-MM-DD

You will be asked to provide your API credentials from Plentymarkets. Afterwards these will be saved into your Keyring (system intern password storage) for a certain amount of time.

The report will be placed by default at your current working directory. But you can provide a different location with the `-o/--out` option.  
You can view the mappings in your config with the `-m/--mappings` option.
And you can change the base URL of your PlentyMarkets system with `-c/--url/--change_url`.
