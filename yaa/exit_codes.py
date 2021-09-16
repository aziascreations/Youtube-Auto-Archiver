# Standard exit codes
NONE = 0
""" Standard exit code returned when everything went well. """

NO_ERROR = NONE
""" Standard exit code returned when everything went well."""

# Custom exit codes
ERROR_CWD_FAILURE = 1000
""" Returned when the application failed to changed its current working directory. """

ERROR_MKDIR_FAILURE = 1001
""" Returned when the application failed to create the folder structure for its downloads. """

ERROR_CONFIG_OS_ERROR = 1002
"""
Returned when the application encountered a generic OSError.
Only happens when loading the config file.
"""

ERROR_CONFIG_JSON_ERROR = 1003
""" Returned when the application encountered an error when parsing the config file's content. """

ERROR_OUTDATED_CONFIG = 1004
""" Returned when the config file is using the old 0.4.0 format. """

ERROR_RUNNING_AS_ROOT = 1005
""" Returned when the application is running as 'root' when it shouldn't. """

ERROR_INVALID_CONFIG_FIELD_TYPE = 1006
""" Returned when one of the field in the config file doesn't have the right data type. """
