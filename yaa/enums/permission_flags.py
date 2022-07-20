# Imports
from enum import IntFlag


# Code
class PermissionFlags(IntFlag):
    READ = 0b0000_0001
    EDIT = 0b0000_0010
    CREATE = 0b0000_0100
    DELETE = 0b0000_1000
    
    @classmethod
    def _can(cls, permission_flags: int, bitmask: int) -> bool:
        return (permission_flags & bitmask) == bitmask
    
    @classmethod
    def can_read(cls, permission_flags: int) -> bool:
        return cls._can(permission_flags, cls.READ)
    
    @classmethod
    def can_edit(cls, permission_flags: int) -> bool:
        return cls._can(permission_flags, cls.EDIT)
    
    @classmethod
    def can_create(cls, permission_flags: int) -> bool:
        return cls._can(permission_flags, cls.CREATE)
    
    @classmethod
    def can_delete(cls, permission_flags: int) -> bool:
        return cls._can(permission_flags, cls.DELETE)
