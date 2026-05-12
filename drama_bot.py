import logging
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# ============================================================
# ⚙️ SOZLAMALAR
# ============================================================
BOT_TOKEN = "8734990502:AAG2bA78hUewOaDOHaDn33fOM0Egw3wWC2c"
ADMIN_ID = 7356097969
GROUP_USERNAME = "uz_korean_vibe"
GROUP_ID = -1003813851367

VISA_CARD = "4149 6005 1234 5678"
HUMO_CARD = "9860 1234 5678 9012"

PRICES = {
    "15kun": {"name": "15 Kunlik", "price": 20000, "days": 15},
    "1oy":   {"name": "1 Oylik",   "price": 35000, "days": 30},
    "1yil":  {"name": "1 Yillik",  "price": 320000, "days": 365},
}

# ============================================================
# 🗄️ BAZALAR
# ============================================================
premium_users = {}
pending_payments = {}

dramas = {
    # Phantom Lawyer
    "1":  {"name": "Phantom Lawyer 1-qism",  "drama": "Phantom Lawyer", "file_id": "BAACAgQAAxkBAAMxaf2tHv7e8DUhr36yzbB5smQk6O0AAiYfAAIoL9hS3aixAAEw7LAlOwQ"},
    "2":  {"name": "Phantom Lawyer 2-qism",  "drama": "Phantom Lawyer", "file_id": "BAACAgQAAxkBAAMzaf2tRo7boSnCvyHE5X3S8-myZasAAnQcAAIoL-BS2TyOyittV207BA"},
    "3":  {"name": "Phantom Lawyer 3-qism",  "drama": "Phantom Lawyer", "file_id": "BAACAgQAAxkBAAM1af2tbrq66ApLt46NHX_mn_OSxy0AArodAALqAAHpUjqzjJXYdt9DOwQ"},
    "4":  {"name": "Phantom Lawyer 4-qism",  "drama": "Phantom Lawyer", "file_id": "BAACAgQAAxkBAAMvaf2sxVcu6FJ1S0YiMbMow2VdeuwAArweAAKV1vFS__52aTz8p9I7BA"},
    "5":  {"name": "Phantom Lawyer 5-qism",  "drama": "Phantom Lawyer", "file_id": "BAACAgQAAxkBAAN4af3JCIS67g0T_gABKRlxXE-wPDe9AALCHQACBJgIUx-0E4h94zwYOwQ"},
    "6":  {"name": "Phantom Lawyer 6-qism",  "drama": "Phantom Lawyer", "file_id": "BAACAgQAAxkBAAN6af3JJPPbODswhXI0A3zraT7weh8AAhAeAAIEmAhT-tr8EsQH4Ug7BA"},
    "7":  {"name": "Phantom Lawyer 7-qism",  "drama": "Phantom Lawyer", "file_id": "BAACAgQAAxkBAAN8af3JNXaBKLRQ-BNjrWXwHnrF2QsAAgIdAAItYRlTDRSVWRqAwe07BA"},
    "8":  {"name": "Phantom Lawyer 8-qism",  "drama": "Phantom Lawyer", "file_id": "BAACAgQAAxkBAAN-af3JR--4HQHDHq11SF4holVzWBUAAiIeAAL1vDlTcpNkZP5_RxE7BA"},
    "9":  {"name": "Phantom Lawyer 9-qism",  "drama": "Phantom Lawyer", "file_id": "BAACAgQAAxkBAAOAaf3JV9hYIQ4XCooHeJ8Bskpzg0IAAmkeAALr9lFTf6bG7y5YPmg7BA"},
    "10": {"name": "Phantom Lawyer 10-qism", "drama": "Phantom Lawyer", "file_id": "BAACAgQAAxkBAAOCaf3JZSsieHsZ8HrZ0OOfou-1BHUAAsEcAAJvhGlTigAB_m2Pupy_OwQ"},
    "11": {"name": "Phantom Lawyer 11-qism", "drama": "Phantom Lawyer", "file_id": "BAACAgQAAxkBAAOEaf3JciRnOn9smSFbW3jUD8HgXbQAApwqAALqvJlThZdRkIq_GUs7BA"},

    # Sen tomon uchganimda
    "12": {"name": "Sen tomon uchganimda 1-qism",  "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAOxaf6LhLnyPDqHtLlvM6rQ2l-3tRQAAiRmAAIqrkhKgtimcJq4bAc7BA"},
    "13": {"name": "Sen tomon uchganimda 2-qism",  "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAOyaf6LhBRJeMe_0psnFZGcXjCuCBUAAjZmAAIqrkhKCdjEkimFuVc7BA"},
    "14": {"name": "Sen tomon uchganimda 3-qism",  "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAOyaf6LhBRJeMe_0psnFZGcXjCuCBUAAjZmAAIqrkhKCdjEkimFuVc7BA"},
    "15": {"name": "Sen tomon uchganimda 4-qism",  "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAO0af6LhKWLFZW5cy74zwT_HXu40AIAAqJjAAJSmUlKoRK5tpPsvSM7BA"},
    "16": {"name": "Sen tomon uchganimda 5-qism",  "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAO1af6LhDPIMtRRE52isWcMAUeZGJkAAqRjAAJSmUlKtsx-6ZpnZ5A7BA"},
    "17": {"name": "Sen tomon uchganimda 6-qism",  "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAO2af6LhCH3YntM8GcdPGvg2ZMfVusAAq5jAAJSmUlK68rXNTGIW_k7BA"},
    "18": {"name": "Sen tomon uchganimda 7-qism",  "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAO3af6LhMqP3YZ3ogjWJF1eHiGmo9wAArFjAAJSmUlKguRa91qBOOc7BA"},
    "19": {"name": "Sen tomon uchganimda 8-qism",  "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAO4af6LhJbV4hqguEKwxj9GRStR7sUAArZjAAJSmUlKMkyUCZUFkN47BA"},
    "20": {"name": "Sen tomon uchganimda 9-qism",  "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAO5af6LhBZ4UfAkQQLIjlLz43L-2EoAAtVjAAJSmUlKMOjQ66535a47BA"},
    "21": {"name": "Sen tomon uchganimda 10-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAO6af6LhDF-DQengRs9QfI0R9Z4AyIAAu1jAAJSmUlKkbS-ckyyhIw7BA"},
    "22": {"name": "Sen tomon uchganimda 11-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAO7af6LhI-CWmXAX_LI45hBInJJk3QAAhhkAAJSmUlK2iBHQbZJO2I7BA"},
    "23": {"name": "Sen tomon uchganimda 12-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAO8af6LhN286oBhGbZiBWSbGgeoZOEAAiJkAAJSmUlKFmAhUsmphpI7BA"},
    "24": {"name": "Sen tomon uchganimda 13-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAO9af6LhJKQrYykU-AlHiStNAIremMAAjVkAAJSmUlKa-xjte-SDzE7BA"},
    "25": {"name": "Sen tomon uchganimda 14-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAO-af6LhOi0rypaJ_htfz--gaTXU1wAArdbAAJSmVFKoG2mWvyRo8I7BA"},
    "26": {"name": "Sen tomon uchganimda 15-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAO_af6LhFFsK7toeL3akQH2284v84wAAjBpAAKPGIFIi50iCQu9oVs7BA"},
    "27": {"name": "Sen tomon uchganimda 16-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAPAaf6LhGmXVOUiaUQSoCc1zFoOysMAAv5tAALYJXlIlCRIQq0y10s7BA"},
    "28": {"name": "Sen tomon uchganimda 17-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAPBaf6LhANe9DPEvnbE3y26HwREFjIAAklvAAKXdpFJ83VpYG5QFkE7BA"},
    "29": {"name": "Sen tomon uchganimda 18-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAPCaf6LhBFD8iLcmCGazSg7P0arNsUAAotyAAKXdpFJQ67g2LZB2bs7BA"},
    "30": {"name": "Sen tomon uchganimda 19-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAPDaf6LhGeGFspOpJ_-63V8bTe05GAAAs9jAAKXyahJx-a1fVJuGNY7BA"},
    "31": {"name": "Sen tomon uchganimda 20-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAPEaf6LhKB7--diUeN0mGtVyEL8uKwAAlxjAAKj7sBJo81Bc9bmFbc7BA"},
    "32": {"name": "Sen tomon uchganimda 21-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgQAAxkBAAPFaf6LhNGlV8tXY2ShnNGEehCFa2gAAk4UAAKXA3hSljut0imM1IU7BA"},
    "33": {"name": "Sen tomon uchganimda 22-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAPGaf6LhB6hiV-2ns_5qiitnzx2kT0AAuWAAAIeLTFLOanTvrLJTwo7BA"},
    "34": {"name": "Sen tomon uchganimda 23-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAPHaf6LhMJzgSRgAnMJ8hMRaT3u8_kAArxkAAKYTAABSwdwf_NlDNpKOwQ"},
    "35": {"name": "Sen tomon uchganimda 24-qism", "drama": "Sen tomon uchganimda", "file_id": "BAACAgIAAxkBAAPIaf6LhK9TMv4gvTCrlJBnObqgdIAAAvRhAAIG6RFLDeHLA6CCcn47BA"},

    # Sirena bosasi
    "36": {"name": "Sirena bosasi 1-qism",           "drama": "Sirena bosasi", "file_id": "BAACAgIAAxkBAAPraf67SO_owFiUjiPoF6e1hk_sWfsAAjOXAAJSrThJSrrmno1PJLc7BA"},
    "37": {"name": "Sirena bosasi 2-qism",           "drama": "Sirena bosasi", "file_id": "BAACAgQAAxkBAAPsaf67SBET7GnQAz9Fax7_2Fd3-NAAAkUvAAI4TxFS-XIxlai4uzM7BA"},
    "38": {"name": "Sirena bosasi 3-qism",           "drama": "Sirena bosasi", "file_id": "BAACAgQAAxkBAAPtaf67SDi2MfPIOYNm_aci9jx3mVkAAl4cAAJt1CBSTTNfuS5X-v07BA"},
    "39": {"name": "Sirena bosasi 4-qism",           "drama": "Sirena bosasi", "file_id": "BAACAgQAAxkBAAPuaf67SGexOaWB2XXG0oM1kspfm1cAAlIdAAIOeSlSZFnseBOcfnw7BA"},
    "40": {"name": "Sirena bosasi 5-qism",           "drama": "Sirena bosasi", "file_id": "BAACAgQAAxkBAAPvaf67SFCCjZrob5HALOQk37S_V0IAAjkdAAIOeTlS_pzRzJ2VD5k7BA"},
    "41": {"name": "Sirena bosasi 6-qism",           "drama": "Sirena bosasi", "file_id": "BAACAgQAAxkBAAPwaf67SMEYQeOq9gABHp8JYM5tMc1XAALMGgACMBxJUj8f5dIr5zLZOwQ"},
    "42": {"name": "Sirena bosasi 7-qism",           "drama": "Sirena bosasi", "file_id": "BAACAgQAAxkBAAPxaf67SGJXVUhwg_9goRzq0eaM7hcAAuQcAAItZWBSt7sM6YFXL9Y7BA"},
    "43": {"name": "Sirena bosasi 8-qism",           "drama": "Sirena bosasi", "file_id": "BAACAgQAAxkBAAPyaf67SAjpKpEz8CQ2h8_M4vS2sVoAAtYaAAJ3lHBScm6l-sonN0U7BA"},
    "44": {"name": "Sirena bosasi 9-qism",           "drama": "Sirena bosasi", "file_id": "BAACAgQAAxkBAAPzaf67SHpaS5cdkS2ClDEvuE512LIAAiciAAKdzIhSeDUa3kILPis7BA"},
    "45": {"name": "Sirena bosasi 10-qism",          "drama": "Sirena bosasi", "file_id": "BAACAgQAAxkBAAP0af67SNAYsoj_vUywVsuAPiL5gVgAAiocAAKdzJhSClgXmEEO7vY7BA"},
    "46": {"name": "Sirena bosasi 11-qism",          "drama": "Sirena bosasi", "file_id": "BAACAgQAAxkBAAP1af67SHmPbXEZ1u9g0ElbF3dxassAApMfAAJt0LFSdieJkY-x-Yc7BA"},
    "47": {"name": "Sirena bosasi 12-qism (FINAL)",  "drama": "Sirena bosasi", "file_id": "BAACAgQAAxkBAAP2af67SPZoWnqliZOLTNdMGmtB0kkAAo4cAAIMoMFS6dXkOlJaYtI7BA"},

    # Darbadar ruh 1-fasl
    "48": {"name": "Darbadar ruh 1-qism",         "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBPGoAAbYbtJRhKvh_xSVl2IJ35GmGqQACgBAAAr3i0VLhEl5cb5IGGTsE"},
    "49": {"name": "Darbadar ruh 2-qism",         "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBPWoAAbYbB95yiHrTsD6FilqY_7LmegACgxAAAr3i0VKByMm6o-aWhTsE"},
    "50": {"name": "Darbadar ruh 3-qism",         "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBPmoAAbYbWb-KDMeeuYgMO6-WdFmG7QACiBAAAr3i0VJnKLWtRByAwDsE"},
    "51": {"name": "Darbadar ruh 4-qism",         "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBP2oAAbYbZf91KmZ6vTvtueP_xA_o0wACjhAAAr3i0VI3o4-MVPSchzsE"},
    "52": {"name": "Darbadar ruh 5-qism",         "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBQGoAAbYb9tj4NkEzEgHvD4nbeIPiGgACmRAAAr3i0VK63MWVI4b2YTsE"},
    "53": {"name": "Darbadar ruh 6-qism",         "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBQWoAAbYbcai0Ayy9aZdKEagySAzZ-wACkhAAAnVZ4VIAAYe38L1B5eo7BA"},
    "54": {"name": "Darbadar ruh 7-qism",         "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBQmoAAbYbjZXfdDpZr2tT1nJFQa43QQACnRAAAr3i0VKXEeiWzNIMXTsE"},
    "55": {"name": "Darbadar ruh 8-qism",         "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBQ2oAAbYbu3ABx6LgK9RQSgK04HvZ3QACnxAAAr3i0VJZHeYt_YLNXTsE"},
    "56": {"name": "Darbadar ruh 9-qism",         "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBRGoAAbYb-uDgyuXUtW76a4qVPj1IuwACvg8AAmug6VL_GKFQ_UDhHzsE"},
    "57": {"name": "Darbadar ruh 10-qism",        "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBRWoAAbYbGlhBRZQwMJOOfeWHAAFzpXQAAiEPAAKFZQABUzLlZTf-g7qcOwQ"},
    "58": {"name": "Darbadar ruh 11-qism",        "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBRmoAAbYbdgidgpjM2kWcaGtM8r7w9wACBBEAAuJDGFOHRBmG1fhctTsE"},
    "59": {"name": "Darbadar ruh 12-qism",        "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBR2oAAbYbpSVFN3M2I8QmYXPawNc-MAACCxEAAuJDGFNJp9IMihlIyjsE"},
    "60": {"name": "Darbadar ruh 13-qism",        "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBSGoAAbYbs5Q9elw1-hwalgIZQTbDOAACRA4AAjYIQVMsWIPH-9OjXTsE"},
    "61": {"name": "Darbadar ruh 14-qism",        "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBSWoAAbYbqOjkrakz1yJlM7W4MlczYQACmw8AAgraYVMaQfHeBfzeQzsE"},
    "62": {"name": "Darbadar ruh 15-qism",        "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBSmoAAbYbdcZCWTLKpQzvBZtLAr21ZQACzhUAAmOnoFOa8Hu-MEylrzsE"},
    "63": {"name": "Darbadar ruh 16-qism",        "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBS2oAAbYbavEGCy7Qdtc-XYsWMFcucwAC3RUAAmOnoFNAvT0kBIDzhzsE"},
    "64": {"name": "Darbadar ruh 17-qism",        "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBTGoAAbYbbEh8KchhGaHt8GOvGlkZqgACoREAAgcBoFMJJJhw2ZflpjsE"},
    "65": {"name": "Darbadar ruh 18-qism",        "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBTWoAAbYba4slcuAwr_B1Jbm4lF4ruQAC9hMAAgcBoFOg7frsjJjS_zsE"},
    "66": {"name": "Darbadar ruh 19-qism",        "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBTmoAAbYbI0cyzPptj5EhwiCdjHrlhgAC_BMAAgcBoFOcP8SsMY_t5jsE"},
    "67": {"name": "Darbadar ruh 20-qism (FASL FINALI)", "drama": "Darbadar ruh 1-fasl", "file_id": "BAACAgQAAxkBAAIBT2oAAbYbSt7J-gcEZf_xAed7Az6AbQAClxEAAkODqVMSSrgAATmj-XA7BA"},

    # Darbadar ruh 2-fasl
    "68": {"name": "Darbadar ruh 21-qism",        "drama": "Darbadar ruh 2-fasl", "file_id": "BAACAgQAAxkBAAIBUGoAAbYbeSPyca3QA4z_l5mcOGdRiAACIRQAAkODsVMJUi4f22CkgjsE"},
    "69": {"name": "Darbadar ruh 22-qism",        "drama": "Darbadar ruh 2-fasl", "file_id": "BAACAgQAAxkBAAIBUWoAAbYbrrJ72rLDgfoiW3WcBHDlPgAC5xMAAuf5qVPBlxJVRY1zQjsE"},
    "70": {"name": "Darbadar ruh 23-qism",        "drama": "Darbadar ruh 2-fasl", "file_id": "BAACAgQAAxkBAAIBUmoAAbYb3WG4Ankxrx2k_DNZb8Li_wAC7BMAAuf5qVNDaSfQgoDs2DsE"},
    "71": {"name": "Darbadar ruh 24-qism",        "drama": "Darbadar ruh 2-fasl", "file_id": "BAACAgQAAxkBAAIBU2oAAbYbns7Rmhp2cBbopruCO3WtqQACMBQAAkODsVPx1O6dadBvKDsE"},
    "72": {"name": "Darbadar ruh 25-qism",        "drama": "Darbadar ruh 2-fasl", "file_id": "BAACAgQAAxkBAAIBVGoAAbYbAdmjQ7UDVx2nL8_WIyNVZAACNBQAAkODsVMxqfVvlXI9_jsE"},
    "73": {"name": "Darbadar ruh 26-qism",        "drama": "Darbadar ruh 2-fasl", "file_id": "BAACAgQAAxkBAAIBVWoAAbYbuWvNhyZPWGKKoOvWluF7sAACWxQAAkODsVPSYifYBpJrTTsE"},
    "74": {"name": "Darbadar ruh 27-qism",        "drama": "Darbadar ruh 2-fasl", "file_id": "BAACAgQAAxkBAAIBVmoAAbYbeJEfHrHzGLOkJEGj3qzYugACdBQAAkODsVPBPPnrvRWpVDsE"},
    "75": {"name": "Darbadar ruh 28-qism",        "drama": "Darbadar ruh 2-fasl", "file_id": "BAACAgQAAxkBAAIBV2oAAbYbjVqjTl0cE1O_XQxJ002aYQACaBQAAkODsVNsKUtz5WJ6VTsE"},
    "76": {"name": "Darbadar ruh 29-qism",        "drama": "Darbadar ruh 2-fasl", "file_id": "BAACAgQAAxkBAAIBWGoAAbYbYL2Cl6dmsyzCcYRmHGHD_AACNxEAAuf5sVPMRmT8XSP3EjsE"},
    "77": {"name": "Darbadar ruh 30-qism (FINAL)", "drama": "Darbadar ruh 2-fasl", "file_id": "BAACAgQAAxkBAAIBWWoAAbYbQvj9QvDU_-NCJ7uW7p_LOgACbxQAAkODsVMg3wotf52xTTsE"},

    # Vorislar
    "78":  {"name": "Vorislar 1-qism",          "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBgGoAAbyStqrBXW_lPJ1uGL0JckK_LQAC8gEAAneXEEno1cpLgKnAgTsE"},
    "79":  {"name": "Vorislar 2-qism",          "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBgWoAAbyScjT7wHBla18Q7kM9COhC2QACewIAAizFGUnafsHGFn7VzTsE"},
    "80":  {"name": "Vorislar 3-qism",          "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBgmoAAbySzJdjE9xBBxqJunmvmcFGuQAC7gEAAif0MEnp36AAAYD8dy47BA"},
    "81":  {"name": "Vorislar 4-qism",          "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBg2oAAbySdrmEIX07H1Ok9KAXxF-KrAAC8gEAAif0MEm3rrB72ArHoTsE"},
    "82":  {"name": "Vorislar 5-qism",          "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBhGoAAbySWGjwphMuiJ1zxQVpBzT9QQACBwMAAoBlYUmeYqpq0NFzgTsE"},
    "83":  {"name": "Vorislar 6-qism",          "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBhWoAAbyS2c3_-pmQCr2ydARE5LXpOgACzwEAArAEeUmYealhXh6NMDsE"},
    "84":  {"name": "Vorislar 7-qism",          "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBhmoAAbySfsd5AzNLfodnS0W-NthL9wACPAMAArAEgUlhCUjwzyvQDzsE"},
    "85":  {"name": "Vorislar 8-qism",          "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBh2oAAbySZzvkN3nTmtGuLPRzdXgKNAACwAIAAnatgUny8_IgzMNiijsE"},
    "86":  {"name": "Vorislar 9-qism",          "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBiGoAAbySGU_yHr_-3aNCt_5EKdYCWgACsQwAAq2vqUsah9blXuu6bjsE"},
    "87":  {"name": "Vorislar 10-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBiWoAAbySdBi_6W_8jaoNfxWtcD1EFQACtAwAAq2vqUuLe4QQxjXAgzsE"},
    "88":  {"name": "Vorislar 11-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBimoAAbyScRZ2i4lDDHrXVNPwpPri3gACtgwAAq2vqUsFLZflmR-sHjsE"},
    "89":  {"name": "Vorislar 12-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBi2oAAbySwKdImoPUxh71dI9HOiJNIQACxgwAAq2vqUsH0RfFsUilBjsE"},
    "90":  {"name": "Vorislar 13-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBjGoAAbySIqTCO3vmmPShJhhsMKHqkwACzgwAAq2vqUvWHxRkHEJDBzsE"},
    "91":  {"name": "Vorislar 14-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBjWoAAbySKqzOuTYc-39uR0i8Q-yGlgAC0AwAAq2vqUvhxSdzwYi0UzsE"},
    "92":  {"name": "Vorislar 15-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBjmoAAbySTwsKaku8MOAE3czA2I1X3QAC0QwAAq2vqUsAAfW2BvEAAad-OwQ"},
    "93":  {"name": "Vorislar 16-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBj2oAAbySDnBeP7VreWxDorHNlI7UUgAC0wwAAq2vqUud7fjfEJU9QTsE"},
    "94":  {"name": "Vorislar 17-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBkGoAAbySOcS5czwEbhK1yVM6VG0FWQAC1AwAAq2vqUtQluzHyjzYiTsE"},
    "95":  {"name": "Vorislar 18-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBkWoAAbyS5Vi2JZB6Q1zQGKfDAdzhWAAC1QwAAq2vqUu7CbCc_mHonDsE"},
    "96":  {"name": "Vorislar 19-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBkmoAAbyS1qk2E99b45Iz3rzPsH7S7gAC1gwAAq2vqUubB5qNR-jvWzsE"},
    "97":  {"name": "Vorislar 20-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBk2oAAbySk1-eIYKT6tD6JlxREZHD6gAC1wwAAq2vqUsoxJHci8spWzsE"},
    "98":  {"name": "Vorislar 21-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBlGoAAbySp4N9yJeQIzJmLTPYwW_9UwAC2AwAAq2vqUtuT7I5nNgAAeY7BA"},
    "99":  {"name": "Vorislar 22-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBlWoAAbySA_0Jwar8v6PrVyZDPyOwnwAC2QwAAq2vqUtQWwhNpnVIAzsE"},
    "100": {"name": "Vorislar 23-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBlmoAAbySjXeTv68Qv-t-HUE9rPDmTAAC2gwAAq2vqUvj2p6N1CHTrTsE"},
    "101": {"name": "Vorislar 24-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBl2oAAbyS5AaZYrg7UTkJEIhrTXNvsQAC3QwAAq2vqUuQsHFWCMHD7TsE"},
    "102": {"name": "Vorislar 25-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBmGoAAbySvdAAAa1PL4ffXgPropebW2AAAuIMAAKtr6lLetScsDwBXkg7BA"},
    "103": {"name": "Vorislar 26-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBmWoAAbyStHqlAcOHQFg217twp0Yr-wAC4wwAAq2vqUufhvwi1jeSvDsE"},
    "104": {"name": "Vorislar 27-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBmmoAAbySGzeVSq75uGlNxSoD1hlcFAAC5AwAAq2vqUsyHfHyxPcLCjsE"},
    "105": {"name": "Vorislar 28-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBm2oAAbyS_YNkSMM4HM9cOEF7Luy_1wAC5QwAAq2vqUs5KUlbHX84DzsE"},
    "106": {"name": "Vorislar 29-qism",         "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBnGoAAbyS4jXfR2Oa15o4vLkSF4tMBgAC5gwAAq2vqUvcS0xkNPQbhjsE"},
    "107": {"name": "Vorislar 30-qism (FINAL)", "drama": "Vorislar", "file_id": "BAACAgIAAxkBAAIBnWoAAbySynR_OeXOnpdJ1COWXsCKjQAC5wwAAq2vqUt8WEMxxL57czsE"},

    # Quyosh avlodlari
    "108": {"name": "Quyosh avlodlari 1-qism",          "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIBy2oAAcTeN8KqD59wo0666KwhvTFTkQACRwIAAjvhoEsigL6mDu1z9TsE"},
    "109": {"name": "Quyosh avlodlari 2-qism",          "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIBzGoAAcTeqs3wWsSLEGubdkqjHQ7jbAACLwIAAjvhqEtrdtzQWyjPnjsE"},
    "110": {"name": "Quyosh avlodlari 3-qism",          "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIBzWoAAcTeRR1efU0U_qnccer118yTWQACiAIAAho5sUsUsgUySku53TsE"},
    "111": {"name": "Quyosh avlodlari 4-qism",          "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIBzmoAAcTePxvAN0BjMeAn43Wl4YtgPQAC5gIAAkJ-uUuklK3K3lEYlDsE"},
    "112": {"name": "Quyosh avlodlari 5-qism",          "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIBz2oAAcTeHcPhSysxdDU1ejb5GXYr3AAC4QEAAj5r2EsGgVxKTB-8gjsE"},
    "113": {"name": "Quyosh avlodlari 6-qism",          "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB0GoAAcTeO6dwcx9a-EctUV9VukgqSgACRwIAAsIm6EsgRZMjBoLxfjsE"},
    "114": {"name": "Quyosh avlodlari 7-qism",          "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB0WoAAcTeF32Nkmu0mQ8C8mh8p9qxwwAC7AEAAiw28UuLUGWJVM0ZrzsE"},
    "115": {"name": "Quyosh avlodlari 8-qism",          "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB0moAAcTe8AddaFt80aXWB_0VOez7tQAClwMAAoIi-Us-wBVPjzEmWjsE"},
    "116": {"name": "Quyosh avlodlari 9-qism",          "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB02oAAcTeRMR4aMkBJm7xKiyfDcJlfQAC_gEAAoIiCUis_ZAJUlcW7zsE"},
    "117": {"name": "Quyosh avlodlari 10-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB1GoAAcTeZNFk9ZzSrQPrtGKeSe4kRQAC6QEAAiT7KUj6d_fXiGTEdzsE"},
    "118": {"name": "Quyosh avlodlari 11-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB1WoAAcTemlvFJEUxHvoZHn8l6e8Q3gACqwIAArVWgUodEPtnIteNcDsE"},
    "119": {"name": "Quyosh avlodlari 12-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB1moAAcTeVhPUsr60ga21NhBYYjRGvAACxgEAAuFOQEjy-OWwhysBszsE"},
    "120": {"name": "Quyosh avlodlari 13-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB12oAAcTeGqtRBVP2ue9Gmncex8GENwACbwIAAuFOSEh0CS0MIZV2hzsE"},
    "121": {"name": "Quyosh avlodlari 14-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB2GoAAcTe3okv7IzacQV16km--xAuBgACsgIAAohrUUiNGvNiM6-jUjsE"},
    "122": {"name": "Quyosh avlodlari 15-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB2WoAAcTeGx1Iq4hLY6DGWeHBqv2iWAACEgMAA1dhSCa4tTdaNFSgOwQ"},
    "123": {"name": "Quyosh avlodlari 16-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB2moAAcTeHm4gJAAB_rUg3LerRaSPu48AApQCAAK8NXlIuwiFutcYjEQ7BA"},
    "124": {"name": "Quyosh avlodlari 17-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB22oAAcTeJAZ0JDwDqChdDy0OiJJ_UwACIgIAApNygEi9cYijF3C9yjsE"},
    "125": {"name": "Quyosh avlodlari 18-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB3GoAAcTeUt79MKjAUH1mzGOTnrp0mgACqwEAAgrjmUiNg0xcX-0d0DsE"},
    "126": {"name": "Quyosh avlodlari 19-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB3WoAAcTe_cGwaNPXXyVutIOuFIhXwwACwgEAAgrjmUi-m2Aw7tf52DsE"},
    "127": {"name": "Quyosh avlodlari 20-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB3moAAcTeyautz-uEYRep2eQrK6OIEAACSwIAAgrjoUjnTHnb4eBb9jsE"},
    "128": {"name": "Quyosh avlodlari 21-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB32oAAcTeUS7rX_Y42Dl1TpF9v8TjnQACzAIAAvSIyEhZHmOjRDDq7jsE"},
    "129": {"name": "Quyosh avlodlari 22-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB4GoAAcTeVsaGXeTSezSMYZbHl9ydngACAwIAAiuq0UitfWa_crAEIjsE"},
    "130": {"name": "Quyosh avlodlari 23-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB4WoAAcTewKFKtIHPBdOOxbR1hSHJvAACuAIAAvd72UjRCofNh2P_MTsE"},
    "131": {"name": "Quyosh avlodlari 24-qism",         "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB4moAAcTejwcrBogYCGFoZ7hBGaPi6AACvgIAAvd74UjfBn2fHGHjyjsE"},
    "132": {"name": "Quyosh avlodlari 25-qism (FINAL)", "drama": "Quyosh avlodlari", "file_id": "BAACAgIAAxkBAAIB42oAAcTen2-MWaJscTho742CY_9l6AACEQMAAog08Ug8MrWnzk44IjsE"},
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ✅ Guruh a'zoligini tekshirish
async def check_subscription(user_id: int, bot) -> bool:
    try:
        member = await bot.get_chat_member(f"@{GROUP_USERNAME}", user_id)
        logger.info(f"User {user_id} status: {member.status}")
        # faqat shu statuslar a'zo hisoblanadi
        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False
    except Exception as e1:
        logger.error(f"Username orqali xato: {e1}")
        try:
            member = await bot.get_chat_member(GROUP_ID, user_id)
            logger.info(f"User {user_id} status (ID): {member.status}")
            if member.status in ["member", "administrator", "creator"]:
                return True
            else:
                return False
        except Exception as e2:
            logger.error(f"ID orqali xato: {e2}")
            return False


# ✅ Premium tekshirish
def is_premium(user_id: int) -> bool:
    if user_id in premium_users:
        if premium_users[user_id]["premium_until"] > datetime.now():
            return True
        else:
            del premium_users[user_id]
    return False


# 🚀 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if is_premium(user_id):
        await send_main_menu(update, context)
        return

    subscribed = await check_subscription(user_id, context.bot)
    logger.info(f"START: user {user_id} subscribed={subscribed}")
    if subscribed:
        await send_main_menu(update, context)
        return

    keyboard = [
        [InlineKeyboardButton("📢 Kanalga a'zo bo'lish", url=f"https://t.me/{GROUP_USERNAME}")],
        [InlineKeyboardButton("✅ Obuna bo'ldim", callback_data="check_sub")],
        [InlineKeyboardButton("💎 Premium harid qilish", callback_data="premium_menu")],
    ]
    await update.message.reply_text(
        f"👋 Salom, {user.first_name}!\n\n"
        f"🎬 *Korean Drama Bot*ga xush kelibsiz!\n\n"
        f"📌 Botdan foydalanish uchun:\n"
        f"1️⃣ Kanalga a'zo bo'ling\n"
        f"2️⃣ *Obuna bo'ldim* tugmasini bosing\n\n"
        f"💎 Yoki premium obuna oling — kanalga a'zo bo'lmasdan ishlating!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# 📋 Asosiy menyu
async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    premium = is_premium(user.id)
    premium_text = "💎 Premium foydalanuvchi" if premium else "🆓 Bepul rejim"

    keyboard = [
        [InlineKeyboardButton("💎 Premium harid qilish", callback_data="premium_menu")],
    ]
    text = (
        f"✅ Salom, {user.first_name}!\n\n"
        f"🎬 *Korean Drama Bot*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 Holat: {premium_text}\n\n"
        f"📌 Drama kodini yuboring, masalan: `1`\n\n"
        f"🎁 *Premium* — kanalga a'zo bo'lmasdan ishlating!"
    )
    if hasattr(update, 'message') and update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


# 🔄 Obuna tekshirish callback
async def check_sub_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    subscribed = await check_subscription(user_id, context.bot)

    if subscribed:
        await send_main_menu(update, context)
    else:
        keyboard = [
            [InlineKeyboardButton("📢 Kanalga a'zo bo'lish", url=f"https://t.me/{GROUP_USERNAME}")],
            [InlineKeyboardButton("✅ Obuna bo'ldim", callback_data="check_sub")],
            [InlineKeyboardButton("💎 Premium harid qilish", callback_data="premium_menu")],
        ]
        await query.edit_message_text(
            "Siz hali kanalga azo emassiz!\n\nAvval kanalga azo boling.\nAzo bolgach Obuna boldim tugmasini bosing.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# 💎 Premium menyu
async def premium_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🔹 15 Kunlik — 20,000 so'm", callback_data="buy_15kun")],
        [InlineKeyboardButton("🔸 1 Oylik — 35,000 so'm",   callback_data="buy_1oy")],
        [InlineKeyboardButton("💎 1 Yillik — 320,000 so'm", callback_data="buy_1yil")],
        [InlineKeyboardButton("◀️ Orqaga", callback_data="back_main")],
    ]
    await query.edit_message_text(
        "💎 *Premium Obuna*\n\n"
        "✅ Kanalga a'zo bo'lmasdan ishlating\n"
        "✅ Cheksiz drama ko'ring\n\n"
        "📦 Tarifni tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# 💳 Tarif tanlash
async def buy_tarif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tarif_key = query.data.replace("buy_", "")
    tarif = PRICES[tarif_key]
    pending_payments[query.from_user.id] = {"tarif": tarif_key, "waiting_check": False}
    keyboard = [
        [InlineKeyboardButton("💳 Visa karta",  callback_data=f"card_visa_{tarif_key}")],
        [InlineKeyboardButton("🟡 Humo karta",  callback_data=f"card_humo_{tarif_key}")],
        [InlineKeyboardButton("◀️ Orqaga",      callback_data="premium_menu")],
    ]
    await query.edit_message_text(
        f"💳 *To'lov usulini tanlang*\n\n"
        f"📦 Tarif: {tarif['name']}\n"
        f"💰 Narx: {tarif['price']:,} so'm",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# 💳 Karta ko'rsatish
async def show_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split("_")
    card_type = parts[1]
    tarif_key = parts[2]
    tarif = PRICES[tarif_key]
    card_number = VISA_CARD if card_type == "visa" else HUMO_CARD
    card_name = "Visa" if card_type == "visa" else "Humo"
    pending_payments[query.from_user.id] = {"tarif": tarif_key, "card_type": card_type, "waiting_check": True}
    keyboard = [[InlineKeyboardButton("◀️ Orqaga", callback_data=f"buy_{tarif_key}")]]
    await query.edit_message_text(
        f"💳 *{card_name} orqali to'lov*\n\n"
        f"📦 Tarif: *{tarif['name']}*\n"
        f"💰 Summa: *{tarif['price']:,} so'm*\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💳 Karta raqami:\n`{card_number}`\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"1. Yuqoridagi kartaga pul o'tkazing\n"
        f"2. Chek rasmini shu chatga yuboring\n"
        f"3. Admin tasdiqlaydi ✅\n\n"
        f"⏱ Tasdiqlash: 5-30 daqiqa",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# 📸 Chek qabul qilish
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    if user_id not in pending_payments or not pending_payments[user_id].get("waiting_check"):
        return
    payment = pending_payments[user_id]
    tarif = PRICES[payment["tarif"]]
    photo = update.message.photo[-1]
    caption = (
        f"💳 Yangi to'lov cheki!\n\n"
        f"👤 {user.first_name}\n"
        f"🆔 {user_id}\n"
        f"📦 {tarif['name']}\n"
        f"💰 {tarif['price']:,} so'm"
    )
    keyboard = [[
        InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"confirm_{user_id}_{payment['tarif']}"),
        InlineKeyboardButton("❌ Rad etish",  callback_data=f"reject_{user_id}"),
    ]]
    await context.bot.send_photo(ADMIN_ID, photo.file_id, caption=caption, reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text("✅ Chek qabul qilindi! Admin tez orada tasdiqlaydi 🙏")
    pending_payments[user_id]["waiting_check"] = False


# ✅ Admin tasdiqlash
async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_ID:
        return
    parts = query.data.split("_")
    user_id = int(parts[1])
    tarif_key = parts[2]
    tarif = PRICES[tarif_key]
    premium_until = datetime.now() + timedelta(days=tarif["days"])
    premium_users[user_id] = {"premium_until": premium_until}
    await query.edit_message_caption(caption=query.message.caption + "\n\n✅ TASDIQLANDI!")
    await context.bot.send_message(
        user_id,
        f"🎉 *Premium faollashtirildi!*\n\n"
        f"📦 {tarif['name']}\n"
        f"📅 {premium_until.strftime('%d.%m.%Y')} gacha\n\n"
        f"Drama kodini yuboring! 🎬",
        parse_mode="Markdown"
    )


# ❌ Admin rad etish
async def reject_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != ADMIN_ID:
        return
    user_id = int(query.data.split("_")[1])
    await query.edit_message_caption(caption=query.message.caption + "\n\n❌ RAD ETILDI")
    await context.bot.send_message(user_id, "❌ To'lovingiz tasdiqlanmadi. Muammo bo'lsa admin bilan bog'laning.")


# 🎬 Drama yuborish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    text = update.message.text.strip()

    # Chek kutilayotgan bo'lsa
    if user_id in pending_payments and pending_payments[user_id].get("waiting_check"):
        await update.message.reply_text("📸 Iltimos, to'lov cheki rasmini yuboring!")
        return

    # Kirish tekshiruvi
    if not is_premium(user_id):
        subscribed = await check_subscription(user_id, context.bot)
        if not subscribed:
            keyboard = [
                [InlineKeyboardButton("📢 Kanalga a'zo bo'lish", url=f"https://t.me/{GROUP_USERNAME}")],
                [InlineKeyboardButton("✅ Obuna bo'ldim", callback_data="check_sub")],
                [InlineKeyboardButton("💎 Premium harid qilish", callback_data="premium_menu")],
            ]
            await update.message.reply_text(
                "⚠️ Avval kanalga a'zo bo'ling!",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

    # Drama kodi
    if text in dramas:
        drama = dramas[text]
        drama_nomi = drama["drama"]

        # Birinchi marta — ro'yxat chiqar
        seen_key = f"seen_{drama_nomi}_{user_id}"
        if not context.bot_data.get(seen_key):
            qismlar = sorted([(k, v) for k, v in dramas.items() if v["drama"] == drama_nomi], key=lambda x: int(x[0]))
            royhat = f"🎬 {drama_nomi}\n━━━━━━━━━━━━━━━\n"
            for kod, info in qismlar:
                marker = "✅" if kod == text else "▶️"
                royhat += f"{marker} {kod} - {info['name'].replace(drama_nomi + ' ', '')}\n"
            royhat += "━━━━━━━━━━━━━━━\nKerakli qism kodini yuboring!"
            await update.message.reply_text(royhat)
            context.bot_data[seen_key] = True

        await update.message.reply_text(f"⏳ {drama['name']} yuklanmoqda...")
        await context.bot.send_video(chat_id=user_id, video=drama["file_id"], caption=f"🎬 {drama['name']}")
    else:
        await update.message.reply_text(f"❌ {text} kodi topilmadi!\n\nTo'g'ri kod yuboring.")


# 🔙 Orqaga
async def back_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await send_main_menu(update, context)


import os

# 🚀 Ishga tushirish
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    private = filters.ChatType.PRIVATE

    app.add_handler(CommandHandler("start", start, filters=private))
    app.add_handler(CallbackQueryHandler(check_sub_callback, pattern="^check_sub$"))
    app.add_handler(CallbackQueryHandler(premium_menu,       pattern="^premium_menu$"))
    app.add_handler(CallbackQueryHandler(buy_tarif,          pattern="^buy_"))
    app.add_handler(CallbackQueryHandler(show_card,          pattern="^card_"))
    app.add_handler(CallbackQueryHandler(confirm_payment,    pattern="^confirm_"))
    app.add_handler(CallbackQueryHandler(reject_payment,     pattern="^reject_"))
    app.add_handler(CallbackQueryHandler(back_main,          pattern="^back_main$"))
    app.add_handler(MessageHandler(private & filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(private & filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot ishga tushdi!")

    # Webhook yoki polling
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
    PORT = int(os.environ.get("PORT", 8443))

    if WEBHOOK_URL:
        print(f"Webhook rejimida: {WEBHOOK_URL}")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=WEBHOOK_URL,
        )
    else:
        print("Polling rejimida...")
        app.run_polling()


if __name__ == "__main__":
    main()
