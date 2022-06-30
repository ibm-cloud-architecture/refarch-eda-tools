In IBM Event Streams version 11 and onwards on OpenShift, schemas must be registered exactly the same as the json.load() function will serialize them because that will then get passed to the schema_lookup() function within the kafkaAvroProducer and Apicurio will compare strings as opposed to load the jsons and compare them. As a result, unless the schema you register in ES is exactly the same as what gets returned from getDefaultEventValueSchema() in AvroEDAUtils.py, you will get the following error:

confluent_kafka.schema_registry.error.SchemaRegistryError: No artifact with ID 'topic-value' in group 'null' was found. (HTTP status code 404, SR code 40401)

See https://github.com/ibm-cloud-architecture/refarch-eda-tools/issues/15