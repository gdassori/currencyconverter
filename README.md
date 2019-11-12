# Micro Currency Converter
An easy to use currency converter, uses ECB data as source, able to convert from\to EUR.



![Build Status](https://travis-ci.org/gdassori/currencyconverter.svg?branch=master)
![Coverage Status](https://coveralls.io/repos/github/gdassori/currencyconverter/badge.svg?branch=master)

#### Installation

Available on DockerHub:
```bash
docker pull gdassori/mcc:latest
docker run -t -p=8080:8080 gdassori/mcc
```

Or can be executed from sources, requires Python >= 3.6 and pip. Virtualenv is optional.
```bash
git clone https://github.com/gdassori/currencyconverter.git
cd currencyconverter
virtualenv -p python3.6 venv  # optional
. venv/bin/activate  # optional
pip install -r requirements.txt
python -m src.app
```

#### Usage example

- Method: `GET`
- Endpoint: `/convert`
- Arguments:
    - `amount`: 10
    - `src_currency`: EUR
    - `dest_currency`: USD
    - `reference_date`: 2019-11-08

With curl

```bash
curl "http://localhost:8080/convert?amount=10&\
&dest_currency=USD&src_currency=EUR&reference_date=2019-11-08"
```

would return:

```bash
{"amount": "11.03", "currency": "USD"}
```
