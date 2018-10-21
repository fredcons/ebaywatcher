# Ebaywatcher

A simple CLI tool to send you a daily digest of your favourite ebay searches.

## Prerequisites

You should have : 
- a working Python environment
- an Ebay app id (get it [there](https://developer.ebay.com/))
- a Sendgrid API key (get it [there](https://app.sendgrid.com/)) 

## Usage

First install dependencies with : 

```
pip install -r requirement.txt
```

Then check the script arguments with : 

```
./ebaywatcher.py --help
Usage: ebaywatcher.py [OPTIONS]

Options:
  --config_path TEXT              The path to the config file
  --search_definitions_path TEXT  The path to the search definitions file
  --num_days INTEGER              The number of days to get back in time
  --mail / --no-mail              Whether to send an email or not. If not,
                                  results wil be printed to the console
  --help                          Show this message and exit.

```

Example executions : 

```
# Run searches defined in config/search_definitions.yaml, configured with config/config.yaml, 1 day back in time, and sends you an email
./ebaywatcher.py
# Run searches defined in /etc/search_definitions.yaml, configured with /etc/my_config.yaml, 3 days back in time, and prettyprints the result in the console
./ebaywatcher.py --config_path=/etc/my_config.yaml --search_definitions_path=/etc/search_definitions.yaml --num_days=3 --no-mail
```

## How to configure it

### Configuring the app

Check the sample file in `config/config_template.yaml':

```
---
!model.Config
# The email to send emails from
email_from: foo@gmail.com
# The email to send email to
email_to: foo@gmail.com
# The email title
email_title: Vos alertes Ebay
# The default category to aply to search definition. Handy if all your search run on a single category
search_default_category: 176985
# The defaut Ebay sites to search in. Items available in different sites are deduplicated by their id. 
search_default_sites:
- EBAY-FR
- EBAY-US
- EBAY-IT
- EBAY-GB
```

### Configuring searches 

Check the sample file in `config/search_definitions_sample.yaml':

```
---
!model.SearchDefinition
# the text to search for
text: my query
# whether to also search for it in the description (default behaviour)
include_description: True
# whether to search for the exact string (default behaviour)
use_exact_match: True
# whether to search for auctions only (default), or auction + buy it now items
auction_only: True
# the category to search in (not required, will default to the default category defined in config.yaml. At least one of them must be defined)
category: 175
# ebay sites to search in (not required, will default to the default sites defined in config.yaml. At least one site should be defined)
sites:
- EBAY-FR
- EBAY-US
```

You can have many blocks like this, one per search, thus building a list of SearchDefinitions.

## Todo

Some nice things that could be done (but probably won't):
- Use a pluggable email implementation
- Use a tag on each SearchDefinition, and then group results by tag in the email

