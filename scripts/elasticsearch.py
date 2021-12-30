from service.converter import DataConversion, ElasticsearchConverter

if __name__ == "__main__":
    # Processing the data updates needed for ingestion
    DataConversion().process_update(converter=ElasticsearchConverter())
