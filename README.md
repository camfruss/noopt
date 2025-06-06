# noopt

## About The Project

`noopt` (pronounced: no-opt) is intended to identified profitable option plays using current market data provided by
Schwab's API using a variety of metrics as discussed in the book Options as a Strategic Investment. 

## Getting Started

### Prerequisites

1. Safari / MacOS is currently required, as 2FA requires a manual login 
2. A Schwab Developer API account + approved app
3. Python 3.12 (removing annotations in `my_parser` relaxes this requirement) 

### Installation

```bash
git clone --depth=1 git@github.com:camfruss/noopt.git; cd noopt
uv sync
```

Afterwords, update the `.env.example` file provided.  

## Usage

The primary usecase is currently report generation and option chain analysis. 

```
client = Client()
client.authorize()
```

Log files are written in json-line format in the `/logs` directory. 

Data files are written to `/data` in the format `/{ISO 8601}.csv`

### Schwab API Endpoints

The documentation provided by Schwab is poor and only available to users with an approved API application. Please open
an issue if you'd like more detailed documentation on a specific endpoint. 

Each of the following endpoints has been fully implemented and can be accessed by a call to their same name (i.e.,
`/quotes -> client.quotes(...)`)

Market Data API
- `/quotes`
- `/chains`
- `/expirationchain`


## Roadmap

- [ ] Complete covered call analysis
- [ ] Add additional data endpoints 
- [ ] Account for dividends
- [ ] Add alternative option strategies (spreads, butterflys, iron condor, etc.)
- [ ] Convert project into package to allow for single import
- [ ] Create a testing suite with `pytest`
- [ ] Integrate Trader API to allow for automated trades
- [ ] and more ...

## Resources

- [Schwabdev](https://github.com/tylerebowers/Schwabdev)

