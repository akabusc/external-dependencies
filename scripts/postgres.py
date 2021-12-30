from service.converter import DataConversion, PostgresConverter

if __name__ == "__main__":
    # Processing the data updates needed for ingestion
    DataConversion().process_update(converter=PostgresConverter())
