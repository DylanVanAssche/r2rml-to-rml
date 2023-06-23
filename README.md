# r2rml-to-rml converter

## Installation

```
pip install -r requirements.txt
```

## Usage

Convert a R2RML mapping (`mapping.r2rml.ttl`) to an RML mapping file 
(`mapping.rml.ttl`), the following database parameters are used in the example:

- **Database driver**: `psql`
- **Database host**: `localhost`
- **Database port**: `5432`
- **Database username**: `root`
- **Database password**: `root`
- **Database name**: `database`

```
./r2rml-to-rml.py --mapping-file=mapping.r2rml.ttl \
    --output-path=mapping.rml.ttl \
    --rdb-driver=psql \
    --rdb-host=localhost \
    --rdb-port=5432 \
    --rdb-username=root \
    --rdb-password=root \
    --rdb-name=database
```

## License

Released under MIT license
Copyright (c) Dylan Van Assche (2023)
IDLab - Ghent University - imec
