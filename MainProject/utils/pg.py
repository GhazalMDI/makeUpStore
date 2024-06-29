import requests

PIN = 'sandbox'
URL = 'https://panel.aqayepardakht.ir/api/v2'
CALL_BACK = 'http://127.0.0.1:8000/order/verifyPay/'


def get_error(err_code):
    ERROR = {
        '-1': 'amount نمی تواند خالی باشد',
        '-2': 'کد پین درگاه نمی تواند خالی باشد',
        '-3': 'callback نمی تواند خالی باشد',
        '-4': 'amount باید عددی باشد',
        '-5': 'amount باید بین 1,000 تا 200,000,000 تومان باشد',
        '-6': 'کد پین درگاه اشتباه هست',
        '-7': 'transid نمی تواند خالی باشد',
        '-8': 'تراکنش مورد نظر وجود ندارد',
        '-9': 'کد پین درگاه با درگاه تراکنش مطابقت ندارد',
        '-10': 'مبلغ با مبلغ تراکنش مطابقت ندارد',
        '-11': 'درگاه درانتظار تایید و یا غیر فعال است',
        '-12': 'امکان ارسال درخواست برای این پذیرنده وجود ندارد',
        '-13': 'شماره کارت باید 16 رقم چسبیده بهم باشد',
        '-14': 'درگاه برروی سایت دیگری درحال استفاده است'
    }
    err = ERROR.get(err_code)
    if not err:
        return 'unknown'
    return err


def create(data):
    data = {
        'pin': PIN,
        'amount': data.get('amount'),
        'callback': CALL_BACK,
        'invoice_id': data.get('invoice_id')
    }
    request = requests.post(f'{URL}/create/', data)
    return request


def verify(data):
    data = {
        'pin': PIN,
        'amount': data.get('amount'),
        'transid': data.get('transid')
    }
    response = requests.post(f'{URL}/verify/', data)
    return response
