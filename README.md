# Micro Currency Converter
An easy to use currency converter, uses ECB data as source, able to convert from\to EUR.

#### Installation

Requires docker:

Available on DockerHub:
```bash
docker pull gdassori/mcc:latest
docker run -t -p=8080:8080 gdassori/mcc
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

