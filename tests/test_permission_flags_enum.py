# Imports
from unittest import TestCase

from yaa.enums.permission_flags import PermissionFlags


# Tests
class TestPermissionFlagsEnum(TestCase):
    def test_single(self):
        # Read
        self.assertTrue(PermissionFlags.can_read(PermissionFlags.READ))
        self.assertFalse(PermissionFlags.can_read(PermissionFlags.EDIT))
        self.assertFalse(PermissionFlags.can_read(PermissionFlags.CREATE))
        self.assertFalse(PermissionFlags.can_read(PermissionFlags.DELETE))
        
        # Edit
        self.assertFalse(PermissionFlags.can_edit(PermissionFlags.READ))
        self.assertTrue(PermissionFlags.can_edit(PermissionFlags.EDIT))
        self.assertFalse(PermissionFlags.can_edit(PermissionFlags.CREATE))
        self.assertFalse(PermissionFlags.can_edit(PermissionFlags.DELETE))
        
        # Create
        self.assertFalse(PermissionFlags.can_create(PermissionFlags.READ))
        self.assertFalse(PermissionFlags.can_create(PermissionFlags.EDIT))
        self.assertTrue(PermissionFlags.can_create(PermissionFlags.CREATE))
        self.assertFalse(PermissionFlags.can_create(PermissionFlags.DELETE))
        
        # Delete
        self.assertFalse(PermissionFlags.can_delete(PermissionFlags.READ))
        self.assertFalse(PermissionFlags.can_delete(PermissionFlags.EDIT))
        self.assertFalse(PermissionFlags.can_delete(PermissionFlags.CREATE))
        self.assertTrue(PermissionFlags.can_delete(PermissionFlags.DELETE))
    
    def test_multiple(self):
        flags_all = PermissionFlags.READ | PermissionFlags.EDIT | PermissionFlags.CREATE | PermissionFlags.DELETE
        
        # Read
        self.assertTrue(PermissionFlags.can_read(flags_all))
        self.assertFalse(PermissionFlags.can_read(flags_all ^ PermissionFlags.READ))
        
        # Edit
        self.assertTrue(PermissionFlags.can_edit(flags_all))
        self.assertFalse(PermissionFlags.can_edit(flags_all ^ PermissionFlags.EDIT))
        
        # Create
        self.assertTrue(PermissionFlags.can_create(flags_all))
        self.assertFalse(PermissionFlags.can_create(flags_all ^ PermissionFlags.CREATE))
        
        # Delete
        self.assertTrue(PermissionFlags.can_delete(flags_all))
        self.assertFalse(PermissionFlags.can_delete(flags_all ^ PermissionFlags.DELETE))
