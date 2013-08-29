
from ._wrap import _func, _register_funcs
from ctypes import (POINTER, c_int, c_uint, c_uint8, c_uint16, c_uint32, c_int32,
    c_char_p, c_void_p, Structure, c_bool)

from .bps import bps_event_t

#----------------------------
# from bps/paymentservice.h
#
# This enumeration defines the Payment Service events.

#  Indicates that a response to a purchase request has been received.
PURCHASE_RESPONSE = 0x00
#  Indicates that a response to a request to retrieve purchase history has
#  been received.
GET_EXISTING_PURCHASES_RESPONSE = 0x01
#  Indicates that a response to a request to get the price of a digital good
#  has been received.
GET_PRICE_RESPONSE = 0x02
#  Indicates that a response to a request to check the subscription status
#  of a digital good has been received.
CHECK_EXISTING_RESPONSE = 0x03
#  Indicates that a response to a request to cancel a subscription has been
#  received.
CANCEL_SUBSCRIPTION_RESPONSE = 0x04

#  This enumeration defines response codes. These reponse codes indicate whether
#  a request that was sent to the Payment Service was successful or
#  unsuccessful.

SUCCESS_RESPONSE = 0
FAILURE_RESPONSE = 1

#  This enumeration defines the possible states of a digital good. For example,
#  whether the digital good item is owned, subscribed, cancelled, renewed, or
#  unknown.
(ITEM_STATE_OWNED,
ITEM_STATE_NEW_SUBSCRIPTION,
ITEM_STATE_SUBSCRIPTION_REFUNDED,
ITEM_STATE_SUBSCRIPTION_CANCELLED,
ITEM_STATE_SUBSCRIPTION_RENEWED,
ITEM_STATE_UNKNOWN) = map(int, range(6))

class purchase_arguments_t(Structure):
    _fields_ = []

PAYMENTSERVICE_APP_SUBSCRIPTION = -1

paymentservice_request_events = _func(c_int, c_int)
paymentservice_stop_events = _func(c_int, c_int)
paymentservice_get_domain = _func(c_int)

paymentservice_purchase_request = _func(c_int, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, POINTER(c_uint))
paymentservice_purchase_request_with_arguments = _func(c_int, POINTER(purchase_arguments_t))
paymentservice_get_existing_purchases_request = _func(c_int, c_bool, c_char_p, POINTER(c_uint))
paymentservice_get_price = _func(c_int, c_char_p, c_char_p, c_char_p, POINTER(c_uint))

paymentservice_check_existing = _func(c_int, c_char_p, c_char_p, c_char_p, POINTER(c_uint))
paymentservice_cancel_subscription = _func(c_int, c_char_p, c_char_p, POINTER(c_uint))
paymentservice_set_connection_mode = _func(c_int, c_bool)

paymentservice_purchase_arguments_create = _func(c_int, POINTER(POINTER(purchase_arguments_t)))
paymentservice_purchase_arguments_destroy = _func(c_int, POINTER(purchase_arguments_t))
paymentservice_purchase_arguments_set_digital_good_id = _func(c_int, POINTER(purchase_arguments_t), c_char_p)
paymentservice_purchase_arguments_get_digital_good_id = _func(c_char_p, POINTER(purchase_arguments_t))
paymentservice_purchase_arguments_set_digital_good_sku = _func(c_int, POINTER(purchase_arguments_t), c_char_p)
paymentservice_purchase_arguments_get_digital_good_sku = _func(c_char_p, POINTER(purchase_arguments_t))
paymentservice_purchase_arguments_set_digital_good_name = _func(c_int, POINTER(purchase_arguments_t), c_char_p)
paymentservice_purchase_arguments_get_digital_good_name = _func(c_char_p, POINTER(purchase_arguments_t))
paymentservice_purchase_arguments_set_metadata = _func(c_int, POINTER(purchase_arguments_t), c_char_p)
paymentservice_purchase_arguments_get_metadata = _func(c_char_p, POINTER(purchase_arguments_t))
paymentservice_purchase_arguments_set_extra_parameter = _func(c_int, POINTER(purchase_arguments_t), c_char_p, c_char_p)
paymentservice_purchase_arguments_get_extra_parameter_by_key = _func(c_char_p, POINTER(purchase_arguments_t), c_char_p)
paymentservice_purchase_arguments_set_app_name = _func(c_int, POINTER(purchase_arguments_t), c_char_p)
paymentservice_purchase_arguments_get_app_name = _func(c_char_p, POINTER(purchase_arguments_t))
paymentservice_purchase_arguments_set_app_icon = _func(c_int, POINTER(purchase_arguments_t), c_char_p)
paymentservice_purchase_arguments_get_app_icon = _func(c_char_p, POINTER(purchase_arguments_t))
paymentservice_purchase_arguments_set_group_id = _func(c_int, POINTER(purchase_arguments_t), c_char_p)
paymentservice_purchase_arguments_get_group_id = _func(c_char_p, POINTER(purchase_arguments_t))
paymentservice_purchase_arguments_set_vendor_customer_id = _func(c_int, POINTER(purchase_arguments_t), c_char_p)
paymentservice_purchase_arguments_get_vendor_customer_id = _func(c_char_p, POINTER(purchase_arguments_t))
paymentservice_purchase_arguments_set_vendor_content_id = _func(c_int, POINTER(purchase_arguments_t), c_char_p)
paymentservice_purchase_arguments_get_vendor_content_id = _func(c_char_p, POINTER(purchase_arguments_t))
paymentservice_purchase_arguments_get_request_id = _func(c_uint, POINTER(purchase_arguments_t))

paymentservice_event_get_response_code = _func(c_int, POINTER(bps_event_t))
paymentservice_event_get_number_purchases = _func(c_int, POINTER(bps_event_t))
paymentservice_event_get_request_id = _func(c_uint, POINTER(bps_event_t))
paymentservice_event_get_date = _func(c_char_p, POINTER(bps_event_t), c_uint)
paymentservice_event_get_digital_good_id = _func(c_char_p, POINTER(bps_event_t), c_uint)
paymentservice_event_get_digital_good_sku = _func(c_char_p, POINTER(bps_event_t), c_uint)
paymentservice_event_get_license_key = _func(c_char_p, POINTER(bps_event_t), c_uint)
paymentservice_event_get_metadata = _func(c_char_p, POINTER(bps_event_t), c_uint)
paymentservice_event_get_extra_parameter_count = _func(c_int, POINTER(bps_event_t), c_uint)
paymentservice_event_get_extra_parameter_key_at_index = _func(c_char_p, POINTER(bps_event_t), c_uint, c_uint)
paymentservice_event_get_extra_parameter_value_at_index = _func(c_char_p, POINTER(bps_event_t), c_uint, c_uint)
paymentservice_event_get_purchase_id = _func(c_char_p, POINTER(bps_event_t), c_uint)
paymentservice_event_get_start_date = _func(c_char_p, POINTER(bps_event_t), c_uint)
paymentservice_event_get_end_date = _func(c_char_p, POINTER(bps_event_t), c_uint)
paymentservice_event_get_purchase_initial_period = _func(c_char_p, POINTER(bps_event_t), c_uint)
paymentservice_event_get_item_state = _func(c_int, POINTER(bps_event_t), c_uint)

paymentservice_event_get_price = _func(c_char_p, POINTER(bps_event_t))
paymentservice_event_get_initial_period = _func(c_char_p, POINTER(bps_event_t))
paymentservice_event_get_renewal_price = _func(c_char_p, POINTER(bps_event_t))
paymentservice_event_get_renewal_period = _func(c_char_p, POINTER(bps_event_t))
paymentservice_event_get_subscription_exists = _func(c_bool, POINTER(bps_event_t))
paymentservice_event_get_cancelled_purchase_id = _func(c_char_p, POINTER(bps_event_t))
paymentservice_event_get_cancelled = _func(c_bool, POINTER(bps_event_t))
paymentservice_event_get_error_id = _func(c_int, POINTER(bps_event_t))
paymentservice_event_get_error_text = _func(c_char_p, POINTER(bps_event_t))

_register_funcs('libbps.so', globals())
