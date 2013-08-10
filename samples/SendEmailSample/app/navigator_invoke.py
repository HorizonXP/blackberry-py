'''Wrappers for libbps routines'''

import ctypes
from ctypes import (c_int, c_int64, c_char_p, c_void_p, c_size_t,
    POINTER, Structure)

from bb._wrap import _func, _register_funcs
from bb.bps import _dll, bps_event_t


#-------------------------------------
class navigator_invoke_invocation_t(Structure):
    _fields_ = []

class navigator_invoke_query_t(Structure):
    _fields_ = []

class navigator_invoke_query_result_action_t(Structure):
    _fields_ = []

class navigator_invoke_query_result_target_t(Structure):
    _fields_ = []

class navigator_invoke_viewer_t(Structure):
    _fields_ = []

NAVIGATOR_INVOKE_TARGET_TYPE_UNSPECIFIED = 0x00
NAVIGATOR_INVOKE_TARGET_TYPE_APPLICATION = 0x01
NAVIGATOR_INVOKE_TARGET_TYPE_CARD         = 0x02
NAVIGATOR_INVOKE_TARGET_TYPE_VIEWER      = 0x04
NAVIGATOR_INVOKE_TARGET_TYPE_SERVICE     = 0x08
NAVIGATOR_INVOKE_TARGET_TYPE_SELF        = 0x10
navigator_invoke_target_type_t = c_int

NAVIGATOR_INVOKE_QUERY_ACTION_TYPE_UNSPECIFIED = 0
NAVIGATOR_INVOKE_QUERY_ACTION_TYPE_MENU        = 1
NAVIGATOR_INVOKE_QUERY_ACTION_TYPE_ALL         = 2
navigator_invoke_query_action_type_t = c_int

NAVIGATOR_INVOKE_PERIMETER_TYPE_UNSPECIFIED = 0
NAVIGATOR_INVOKE_PERIMETER_TYPE_PERSONAL    = 1
NAVIGATOR_INVOKE_PERIMETER_TYPE_ENTERPRISE  = 2
navigator_invoke_perimeter_type_t = c_int

NAVIGATOR_INVOKE_FILE_TRANSFER_MODE_UNSPECIFIED = 0
NAVIGATOR_INVOKE_FILE_TRANSFER_MODE_PRESERVE    = 1
NAVIGATOR_INVOKE_FILE_TRANSFER_MODE_COPY_RO     = 2
NAVIGATOR_INVOKE_FILE_TRANSFER_MODE_COPY_RW     = 3
NAVIGATOR_INVOKE_FILE_TRANSFER_MODE_LINK        = 4
navigator_invoke_file_transfer_mode_t = c_int

navigator_invoke_invocation_create = _func(c_int, POINTER(POINTER(navigator_invoke_invocation_t)))
navigator_invoke_invocation_destroy = _func(c_int, POINTER(navigator_invoke_invocation_t))
navigator_invoke_invocation_set_id = _func(c_int, POINTER(navigator_invoke_invocation_t), c_char_p)
navigator_invoke_invocation_set_target = _func(c_int, POINTER(navigator_invoke_invocation_t), c_char_p)
navigator_invoke_invocation_set_source = _func(c_int, POINTER(navigator_invoke_invocation_t), c_char_p)
navigator_invoke_invocation_set_action = _func(c_int, POINTER(navigator_invoke_invocation_t), c_char_p)
navigator_invoke_invocation_set_type = _func(c_int, POINTER(navigator_invoke_invocation_t), c_char_p)
navigator_invoke_invocation_set_uri = _func(c_int, POINTER(navigator_invoke_invocation_t), c_char_p)
navigator_invoke_invocation_set_file_transfer_mode = _func(c_int, POINTER(navigator_invoke_invocation_t), navigator_invoke_file_transfer_mode_t)
navigator_invoke_invocation_set_data = _func(c_int, POINTER(navigator_invoke_invocation_t), c_void_p, c_int)
navigator_invoke_invocation_set_perimeter = _func(c_int, POINTER(navigator_invoke_invocation_t), navigator_invoke_perimeter_type_t)
navigator_invoke_invocation_set_metadata = _func(c_int, POINTER(navigator_invoke_invocation_t), c_char_p)
navigator_invoke_invocation_set_target_type_mask = _func(c_int, POINTER(navigator_invoke_invocation_t), c_int)
navigator_invoke_invocation_get_id = _func(c_char_p, POINTER(navigator_invoke_invocation_t))
navigator_invoke_invocation_get_target = _func(c_char_p, POINTER(navigator_invoke_invocation_t))
navigator_invoke_invocation_get_source = _func(c_char_p, POINTER(navigator_invoke_invocation_t))
navigator_invoke_invocation_get_action = _func(c_char_p, POINTER(navigator_invoke_invocation_t))
navigator_invoke_invocation_get_type = _func(c_char_p, POINTER(navigator_invoke_invocation_t))
navigator_invoke_invocation_get_uri = _func(c_char_p, POINTER(navigator_invoke_invocation_t))
navigator_invoke_invocation_get_file_transfer_mode = _func(c_int, POINTER(navigator_invoke_invocation_t))
navigator_invoke_invocation_get_data_length = _func(c_int, POINTER(navigator_invoke_invocation_t))
navigator_invoke_invocation_get_data = _func(c_void_p, POINTER(navigator_invoke_invocation_t))
navigator_invoke_invocation_get_perimeter = _func(navigator_invoke_perimeter_type_t, POINTER(navigator_invoke_invocation_t))
navigator_invoke_invocation_get_metadata = _func(c_char_p, POINTER(navigator_invoke_invocation_t))
navigator_invoke_invocation_get_target_type_mask = _func(c_int, POINTER(navigator_invoke_invocation_t))
navigator_invoke_event_get_invocation = _func(POINTER(navigator_invoke_invocation_t), POINTER(bps_event_t))
navigator_invoke_invocation_send = _func(c_int, POINTER(navigator_invoke_invocation_t))
navigator_invoke_query_create = _func(c_int, POINTER(POINTER(navigator_invoke_query_t)))
navigator_invoke_query_destroy = _func(c_int, POINTER(navigator_invoke_query_t))
navigator_invoke_query_set_id = _func(c_int, POINTER(navigator_invoke_query_t), c_char_p)
navigator_invoke_query_set_action = _func(c_int, POINTER(navigator_invoke_query_t), c_char_p)
navigator_invoke_query_set_type = _func(c_int, POINTER(navigator_invoke_query_t), c_char_p)
navigator_invoke_query_set_file_uri = _func(c_int, POINTER(navigator_invoke_query_t), c_char_p)
navigator_invoke_query_set_target_type_mask = _func(c_int, POINTER(navigator_invoke_query_t), c_int)
navigator_invoke_query_set_action_type = _func(c_int, POINTER(navigator_invoke_query_t), navigator_invoke_query_action_type_t)
navigator_invoke_query_set_perimeter = _func(c_int, POINTER(navigator_invoke_query_t), navigator_invoke_perimeter_type_t)
navigator_invoke_query_get_id = _func(c_char_p, POINTER(navigator_invoke_query_t))
navigator_invoke_query_get_action = _func(c_char_p, POINTER(navigator_invoke_query_t))
navigator_invoke_query_get_type = _func(c_char_p, POINTER(navigator_invoke_query_t))
navigator_invoke_query_get_file_uri = _func(c_char_p, POINTER(navigator_invoke_query_t))
navigator_invoke_query_get_target_type_mask = _func(c_int, POINTER(navigator_invoke_query_t))
navigator_invoke_query_get_action_type = _func(navigator_invoke_query_action_type_t, POINTER(navigator_invoke_query_t))
navigator_invoke_query_get_perimeter = _func(navigator_invoke_perimeter_type_t, POINTER(navigator_invoke_query_t))
navigator_invoke_query_send = _func(c_int, POINTER(navigator_invoke_query_t))
navigator_invoke_event_get_query_result_action_count = _func(c_int, POINTER(bps_event_t))
navigator_invoke_event_get_query_result_action = _func(POINTER(navigator_invoke_query_result_action_t), POINTER(bps_event_t), c_int)
navigator_invoke_query_result_action_get_name = _func(c_char_p, POINTER(navigator_invoke_query_result_action_t))
navigator_invoke_query_result_action_get_icon = _func(c_char_p, POINTER(navigator_invoke_query_result_action_t))
navigator_invoke_query_result_action_get_label = _func(c_char_p, POINTER(navigator_invoke_query_result_action_t))
navigator_invoke_query_result_action_get_default_target = _func(c_char_p, POINTER(navigator_invoke_query_result_action_t))
navigator_invoke_query_result_action_get_target_count = _func(c_int, POINTER(navigator_invoke_query_result_action_t))
navigator_invoke_query_result_action_get_target = _func(POINTER(navigator_invoke_query_result_target_t), POINTER(navigator_invoke_query_result_action_t), c_int)
navigator_invoke_query_result_target_get_key = _func(c_char_p, POINTER(navigator_invoke_query_result_target_t))
navigator_invoke_query_result_target_get_icon = _func(c_char_p, POINTER(navigator_invoke_query_result_target_t))
navigator_invoke_query_result_target_get_label = _func(c_char_p, POINTER(navigator_invoke_query_result_target_t))
navigator_invoke_query_result_target_get_type = _func(navigator_invoke_target_type_t, POINTER(navigator_invoke_query_result_target_t))
navigator_invoke_query_result_target_get_perimeter = _func(navigator_invoke_perimeter_type_t, POINTER(navigator_invoke_query_result_target_t))
navigator_invoke_event_get_target = _func(c_char_p, POINTER(bps_event_t))
navigator_invoke_event_get_target_type = _func(c_int, POINTER(bps_event_t))
navigator_invoke_event_get_group_id = _func(c_int64, POINTER(bps_event_t))
navigator_invoke_event_get_dname = _func(c_char_p, POINTER(bps_event_t))
navigator_invoke_set_filters = _func(c_int, c_char_p, c_char_p,POINTER(c_char_p), c_size_t)
navigator_invoke_get_filters = _func(c_int, c_char_p, c_char_p)
navigator_invoke_event_get_filters_target = _func(c_char_p, POINTER(bps_event_t))
navigator_invoke_event_get_filters_count = _func(c_int, POINTER(bps_event_t))
navigator_invoke_event_get_filter = _func(c_char_p, POINTER(bps_event_t), c_int)
navigator_invoke_uri_to_local_path = _func(c_char_p, c_char_p)
navigator_invoke_local_path_to_uri = _func(c_char_p, c_char_p)


#----------------------------
# apply argtypes/restype to all functions
#
_register_funcs(_dll, globals())


# EOF
