
import os
from ctypes import (c_int, byref, POINTER, pointer,
    create_string_buffer, string_at, sizeof)
import string

from bb import bps
from bb.payment import *

import tart


class PaymentError(Exception):
    '''represents failure in payment services call'''

class PaymentEvent:
    EVENT_TYPES = {
        PURCHASE_RESPONSE: 'PURCHASE_RESPONSE',
        GET_EXISTING_PURCHASES_RESPONSE: 'GET_EXISTING_PURCHASES_RESPONSE',
        GET_PRICE_RESPONSE: 'GET_PRICE_RESPONSE',
        CHECK_EXISTING_RESPONSE: 'CHECK_EXISTING_RESPONSE',
        CANCEL_SUBSCRIPTION_RESPONSE: 'CANCEL_SUBSCRIPTION_RESPONSE',
        }

    ITEM_STATES = {
            ITEM_STATE_OWNED: 'Owned',
            ITEM_STATE_NEW_SUBSCRIPTION: 'NewSubscription',
            ITEM_STATE_SUBSCRIPTION_REFUNDED: 'SubscriptionRefunded',
            ITEM_STATE_SUBSCRIPTION_CANCELLED: 'SubscriptionCancelled',
            ITEM_STATE_SUBSCRIPTION_RENEWED: 'SubscriptionRenewed',
            ITEM_STATE_UNKNOWN: 'Unknown'
        }


    def __init__(self, code, type, payment_event, fake=False):
        self.code = code
        self.type = type
        self.payment_event = payment_event
        self.fake = fake


    def __repr__(self):
        r = ['<PaymentEvent %d' % self.code]
        r.append(' ' + self.EVENT_TYPES.get(self.type, 'type?'))
        if self.fake:
            r.append(' (fake!)')
        r.append('>')
        return ''.join(r)


class PaymentHandler:
    def __init__(self, dispatcher):
        # must call this only once, apparently (see native sample)
        rc = paymentservice_request_events(0)
        if rc == FAILURE_RESPONSE:
            tart.send('paymentsDisabled')
            raise BbmError('cannot use payment service, try restart')
        print('paymentservice_request_events(0), rc', rc)

        dispatcher.add_handler(paymentservice_get_domain(), self.handle_event)
        self.prev_access = -1


    def make_event(self, bps_event):
        code = bps.bps_event_get_code(bps_event)

        rc = paymentservice_event_get_response_code(bps_event)
        if rc == bps.BPS_FAILURE:
            raise PaymentError('unable to get event type')
        type = rc

        payment_event = bps_event

        return PaymentEvent(code, type, payment_event)

    #---------------------------------------------
    #
    def handle_event(self, bps_event):
        '''Handle BPS events for payment domain'''

        # print('domain', domain, 'bbm_domain', bbmsp_get_domain())
        event = self.make_event(bps_event)
        code = event.code
        tart.send('paymentEvent', code=code, text=event.EVENT_TYPES.get(code, '?unrecognized?'))
        if code == PURCHASE_RESPONSE:
            self.handlePurchaseResponse(event)
        elif code == GET_EXISTING_PURCHASES_RESPONSE:
            self.handleGetExistingPurchasesResponse(event)
        elif code == GET_PRICE_RESPONSE:
            self.handleGetPriceResponse(event)
        elif code == CHECK_EXISTING_RESPONSE:
            self.handleCheckExistingResponse(event)
        elif code == CANCEL_SUBSCRIPTION_RESPONSE: 
            self.handleCancelSubscriptionResponse
        elif code == FAILURE_RESPONSE:
            self.handleErrorResponse

    def setConnectionMode(self, local=False):
        rc = paymentservice_set_connection_mode(local)
        print('paymentservice_set_connection_mode to local', rc)

    def setWindowGroupId(self, windowGroupId):
        self.windowGroupId = windowGroupId.encode('utf-8')

    def getExistingPurchases(self, allow_refresh=True):
        if not self.windowGroupId:
            raise PaymentError('windowGroupId is not defined. Set it before you call other methods.')

        request_id = c_uint()
        rc = paymentservice_get_existing_purchases_request(allow_refresh, self.windowGroupId, byref(request_id))
        print('paymentservice_get_existing_purchases_request', rc)
        return request_id

    def requestPurchase(self, digitalGoodSku, digitalGoodId=None, digitalGoodName=None,
            purchaseMetaData=None, extraParameters=dict()):
        if not self.windowGroupId:
            raise PaymentError('windowGroupId is not defined. Set it before you call other methods.')

        if (digitalGoodId == None):
            digitalGoodId = digitalGoodSku
        else:
            digitalGoodSku = digitalGoodId

        purchase_arguments = POINTER(purchase_arguments_t)()
        rc = paymentservice_purchase_arguments_create(byref(purchase_arguments))
        print('paymentservice_purchase_arguments_create', rc)

        rc = paymentservice_purchase_arguments_set_group_id(purchase_arguments, self.windowGroupId)
        print('paymentservice_purchase_arguments_set_group_id', rc)

        rc = paymentservice_purchase_arguments_set_digital_good_id(purchase_arguments, digitalGoodId.encode('utf-8'))
        print('paymentservice_purchase_arguments_set_digital_good_id', rc)
        rc = paymentservice_purchase_arguments_set_digital_good_sku(purchase_arguments, digitalGoodSku.encode('utf-8'))
        print('paymentservice_purchase_arguments_set_digital_good_sku', rc)

        if digitalGoodName:
            rc = paymentservice_purchase_arguments_set_digital_good_name(purchase_arguments, digitalGoodName.encode('utf-8'))
            print('paymentservice_purchase_arguments_set_digital_good_name', rc)

        if purchaseMetaData:
            rc = paymentservice_purchase_arguments_set_metadata(purchase_arguments, purchaseMetaData.encode('utf-8'))
            print('paymentservice_purchase_arguments_set_metadata', rc)

        for key in extraParameters:
            rc = paymentservice_purchase_arguments_set_extra_parameter(purchase_arguments, key.encode('utf-8'), str(extraParameters[key]).encode('utf-8'))
            print('paymentservice_purchase_arguments_set_extra_parameter', rc)


        rc = paymentservice_purchase_request_with_arguments(purchase_arguments)
        print('paymentservice_purchase_request_with_arguments', rc)

        rc = paymentservice_purchase_arguments_get_request_id(purchase_arguments)
        print('paymentservice_purchase_arguments_get_request_id', rc)
        request_id = rc

        rc = paymentservice_purchase_arguments_destroy(purchase_arguments)
        print('paymentservice_purchase_arguments_destroy', rc)

        return request_id

    def handleGetExistingPurchasesResponse(self, event):
        purchases = self.getPurchases(event)
        if len(purchases):
            tart.send('existingPurchasesResponse', purchases=purchases)
        else: 
            self.handleErrorResponse(event)

    def handlePurchaseResponse(self, event):
        purchases = self.getPurchases(event)
        if len(purchases):
            tart.send('purchaseResponse', purchases=purchases)
        else: 
            self.handleErrorResponse(event)

    def getPurchases(self, event):
        count = paymentservice_event_get_number_purchases(byref(event.payment_event))
        purchases = list()

        for i in range(count):
            date = paymentservice_event_get_date(byref(event.payment_event), i)
            digitalGoodId = paymentservice_event_get_digital_good_id(byref(event.payment_event), i)
            digitalGoodSku = paymentservice_event_get_digital_good_sku(byref(event.payment_event), i)
            startDate = paymentservice_event_get_start_date(byref(event.payment_event), i)
            endDate = paymentservice_event_get_end_date(byref(event.payment_event), i)
            state = paymentservice_event_get_item_state(byref(event.payment_event), i)
            licenseKey = paymentservice_event_get_license_key(byref(event.payment_event), i)
            purchase_id = paymentservice_event_get_purchase_id(byref(event.payment_event), i)
            initialPeriod = paymentservice_event_get_purchase_initial_period(byref(event.payment_event), i)
            request_id = paymentservice_event_get_request_id(byref(event.payment_event), i)

            data = dict()
            data['date'] = date.decode('utf-8') if date else None
            data['digitalGoodId'] = digitalGoodId.decode('utf-8') if digitalGoodId else None
            data['digitalGoodSku'] = digitalGoodSku.decode('utf-8') if digitalGoodSku else None
            data['startDate'] = startDate.decode('utf-8') if startDate else None
            data['endDate'] = endDate.decode('utf-8') if endDate else None
            data['state'] = event.ITEM_STATES.get(state, "state?") if state else None
            data['licenseKey'] = licenseKey.decode('utf-8') if licenseKey else None
            data['purchaseId'] = purchase_id.decode('utf-8') if purchase_id else None
            data['initialPeriod'] = initialPeriod.decode('utf-8') if initialPeriod else None
            data['requestId'] = request_id if request_id else None
            purchases.append(data)
        return purchases


    def handleGetPriceResponse(self, event):
        pass

    def handleCheckExistingResponse(self, event):
        pass

    def handleCancelSubscriptionResponse(self, event):
        pass

    def handleErrorResponse(self, event):
        rc = paymentservice_event_get_error_id(byref(event.payment_event))
        errStr = paymentservice_event_get_error_text(byref(event.payment_event))
        data = dict()
        data['code'] = rc
        data['text'] = errStr.decode('utf-8')

        tart.send('paymentErrorResponse', error=data)


# EOF
