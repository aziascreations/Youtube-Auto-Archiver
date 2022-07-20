# Standard exit codes
NONE = 0
"""Standard exit code returned when everything went well."""

NO_ERROR = NONE
"""Standard exit code returned when everything went well."""


# Custom exit codes
ERROR_CONFIG_INVALID_PATH = 2000
"""Returned when the config file couldn't be found or is a folder."""

ERROR_CONFIG_PARSING_FAILURE = 2001
"""Returned when the config file couldn't be parsed."""

__ERROR_OUTDATED_CONFIG = 2002
""" Returned when the config file is using an outdated and unsupported format."""


ERROR_RUNNING_AS_ROOT = 2010
"""Returned when the application is running as 'root' when it shouldn't."""

ERROR_NO_OS_GETUID = 2011
"""Returned couldn't find the 'os.getuid' method when it was required."""


ERROR_CWD_FAILURE = 2020
"""Returned when the application failed to changed its current working directory."""


# Legacy custom exit codes  (DO NOT USE !!!)
__ERROR_MKDIR_FAILURE = 1001
"""Returned when the application failed to create the folder structure for its downloads."""
