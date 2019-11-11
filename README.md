# Micro Currency Converter
An easy to use currency converter, uses ECB data as source, able to convert from\to EUR.

####Installation

Requires docker:

With Docker, from Dockerhub
```
docker pull gdassori/currencyconverter:latest
docker run gdassori/currencyconverter
```

Without Docker, in a dedicated Python virtual environment

```bash
git clone https://github.com/gdassori/currencyconverter.git
cd currencyconverter
virtualenv -p python3.6 venv
. venv/bin/activate
pip install -r requirements.txt
python -m mcc.app
```

####Run tests
```bash
. venv/bin/activate
bash coverage.sh
```

####Usage example

Arguments
- amount: float
- src_currency: str
- dest_currency: str
- reference_date: YYYY-MM-DD

An example call with curl:

```bash
curl http://localhost:8080/convert?amount=10&dest_currency=USD&src_currency=EUR&reference_date=2019-11-08
```

would return:

```bash
{"amount": "11.03", "currency": "USD"}
```

