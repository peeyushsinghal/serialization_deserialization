# Stock and Trade Data Serialization

This project implements JSON serialization and deserialization for Stock and Trade data using both custom JSON encoders/decoders and Marshmallow schemas.

## Features

- Custom JSON encoder/decoder for Stock and Trade objects
- Marshmallow schemas for data validation and serialization
- Support for Decimal numbers, dates, and timestamps
- Comprehensive test suite

## CI/CD

This project uses GitHub Actions for continuous integration. The workflow:
- Triggers on push to main branch and pull requests
- Tests Python 3.9 compatibility
- Executes the full test suite

## Dependencies

- Python 3.9+
- marshmallow: Data serialization/deserialization
- pytest: Testing framework