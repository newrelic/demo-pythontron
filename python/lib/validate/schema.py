def get_schema():
    config_file_schema = {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "port": { "type": "integer" },
          "dependencies": { "type": "array" }
        }

    }
    return config_file_schema