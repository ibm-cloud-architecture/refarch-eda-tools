import avro.schema
import json

# def getContainerEventSchema(schema_files_location):
#   # Read all the schemas needed in order to produce the final Container Event Schema
#   known_schemas = avro.schema.Names()
#   container_status_schema = LoadAvsc(schema_files_location + "/container_status.avsc", known_schemas)
#   container_event_payload_schema = LoadAvsc(schema_files_location + "/container_event_payload.avsc", known_schemas)
#   container_event_type_schema = LoadAvsc(schema_files_location + "/container_event_type.avsc", known_schemas)
#   container_event_schema = LoadAvsc(schema_files_location + "/container_event.avsc", known_schemas)
#   return container_event_schema

def getDefaultEventValueSchema(schema_files_location):
  # Get the default event value data schema
  known_schemas = avro.schema.Names()
  default_event_value_schema = LoadAvsc(schema_files_location + "/default_value.avsc", known_schemas)
  return default_event_value_schema

def getDefaultEventValueSchemaConsumer(schema_files_location):
  # Get the default event value data schema
  known_schemas = avro.schema.Names()
  default_event_value_schema = LoadAvsc(schema_files_location + "/default_value.avsc", known_schemas)
  return default_event_value_schema

def getDefaultEventKeySchema(schema_files_location):
  # Get the default event key data schema
  known_schemas = avro.schema.Names()
  default_event_key_schema = LoadAvsc(schema_files_location + "/default_key.avsc", known_schemas)
  return default_event_key_schema

def LoadAvsc(file_path, names=None):
  # Load avsc file
  # file_path: path to schema file
  # names(optional): avro.schema.Names object
  file_text = open(file_path).read()
  json_data = json.loads(file_text)
  schema = avro.schema.SchemaFromJSONData(json_data, names)
  return schema