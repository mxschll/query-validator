# YAML structure for test definition files
schema = {
    'name': {
        'type': 'string',
        'required': True
    },
    'query': {
        'type': 'string',
        'required': True
    },
    'assertions': {
        'type': 'dict',
        'required': True,
        'schema': {
            'count': {
                'type': 'integer',
            },
            'has': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'column': {
                            'type': 'string',
                            'required': True
                        },
                        'values': {
                            'type': 'list',
                            'schema': {
                                'type': 'string'
                            },
                            'required': True
                        }
                    }
                }
            },
            'missing': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'column': {
                            'type': 'string',
                            'required': True
                        },
                        'values': {
                            'type': 'list',
                            'schema': {'type': 'string'},
                            'required': True
                        },
                        'regex': {
                            'type': 'list',
                            'schema': {'type': 'string'},
                            'required': False
                        }
                    }
                }
            },
            'no_nulls': {
                'type': 'list',
                'schema': {'type': 'string', 'required': True},
            },
            'only_nulls': {
                'type': 'list',
                'schema': {'type': 'string', 'required': True},
            },
            'conditions': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'column': {
                            'type': 'string',
                            'required': True
                        },
                        'operator': {
                            'type': 'string',
                            'required': True
                        },
                        'value': {
                            'type': 'string',
                            'required': True
                        }
                    }
                }
            }
        }
    }
}
