import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = "https://www.amdoren.com/api/currency.php"
# You have to register in order to get an API KEY
API_KEY = os.getenv("AMDOREN_API_KEY")

if not API_KEY:
    raise Exception("API key not found. Make sure it's set in the .env file.")

# Currency and their description
list_of_currencies = """
AED	United Arab Emirates Dirham
AFN	Afghan Afghani
ALL	Albanian Lek
AMD	Armenian Dram
ANG	Netherlands Antillean Guilder
AOA	Angolan Kwanza
ARS	Argentine Peso
AUD	Australian Dollar
AWG	Aruban Florin
AZN	Azerbaijani Manat
BAM	Bosnia & Herzegovina Convertible Mark
BBD	Barbadian Dollar
BDT	Bangladeshi Taka
BGN	Bulgarian Lev
BHD	Bahraini Dinar
BIF	Burundian Franc
BMD	Bermudian Dollar
BND	Brunei Dollar
BOB	Bolivian Boliviano
BRL	Brazilian Real
BSD	Bahamian Dollar
BTN	Bhutanese Ngultrum
BWP	Botswana Pula
BYN	Belarus Ruble
BZD	Belize Dollar
CAD	Canadian Dollar
CDF	Congolese Franc
CHF	Swiss Franc
CLP	Chilean Peso
CNY	Chinese Yuan
COP	Colombian Peso
CRC	Costa Rican Colon
CUC	Cuban Convertible Peso
CVE	Cape Verdean Escudo
CZK	Czech Republic Koruna
DJF	Djiboutian Franc
DKK	Danish Krone
DOP	Dominican Peso
DZD	Algerian Dinar
EGP	Egyptian Pound
ERN	Eritrean Nakfa
ETB	Ethiopian Birr
EUR	Euro
FJD	Fiji Dollar
GBP	British Pound Sterling
GEL	Georgian Lari
GHS	Ghanaian Cedi
GIP	Gibraltar Pound
GMD	Gambian Dalasi
GNF	Guinea Franc
GTQ	Guatemalan Quetzal
GYD	Guyanaese Dollar
HKD	Hong Kong Dollar
HNL	Honduran Lempira
HRK	Croatian Kuna
HTG	Haiti Gourde
HUF	Hungarian Forint
IDR	Indonesian Rupiah
ILS	Israeli Shekel
INR	Indian Rupee
IQD	Iraqi Dinar
IRR	Iranian Rial
ISK	Icelandic Krona
JMD	Jamaican Dollar
JOD	Jordanian Dinar
JPY	Japanese Yen
KES	Kenyan Shilling
KGS	Kyrgystani Som
KHR	Cambodian Riel
KMF	Comorian Franc
KPW	North Korean Won
KRW	South Korean Won
KWD	Kuwaiti Dinar
KYD	Cayman Islands Dollar
KZT	Kazakhstan Tenge
LAK	Laotian Kip
LBP	Lebanese Pound
LKR	Sri Lankan Rupee
LRD	Liberian Dollar
LSL	Lesotho Loti
LYD	Libyan Dinar
MAD	Moroccan Dirham
MDL	Moldovan Leu
MGA	Malagasy Ariary
MKD	Macedonian Denar
MMK	Myanma Kyat
MNT	Mongolian Tugrik
MOP	Macau Pataca
MRO	Mauritanian Ouguiya
MUR	Mauritian Rupee
MVR	Maldivian Rufiyaa
MWK	Malawi Kwacha
MXN	Mexican Peso
MYR	Malaysian Ringgit
MZN	Mozambican Metical
NAD	Namibian Dollar
NGN	Nigerian Naira
NIO	Nicaragua Cordoba
NOK	Norwegian Krone
NPR	Nepalese Rupee
NZD	New Zealand Dollar
OMR	Omani Rial
PAB	Panamanian Balboa
PEN	Peruvian Nuevo Sol
PGK	Papua New Guinean Kina
PHP	Philippine Peso
PKR	Pakistani Rupee
PLN	Polish Zloty
PYG	Paraguayan Guarani
QAR	Qatari Riyal
RON	Romanian Leu
RSD	Serbian Dinar
RUB	Russian Ruble
RWF	Rwanda Franc
SAR	Saudi Riyal
SBD	Solomon Islands Dollar
SCR	Seychellois Rupee
SDG	Sudanese Pound
SEK	Swedish Krona
SGD	Singapore Dollar
SHP	Saint Helena Pound
SLL	Sierra Leonean Leone
SOS	Somali Shilling
SRD	Surinamese Dollar
SSP	South Sudanese Pound
STD	Sao Tome and Principe Dobra
SYP	Syrian Pound
SZL	Swazi Lilangeni
THB	Thai Baht
TJS	Tajikistan Somoni
TMT	Turkmenistani Manat
TND	Tunisian Dinar
TOP	Tonga Paanga
TRY	Turkish Lira
TTD	Trinidad and Tobago Dollar
TWD	New Taiwan Dollar
TZS	Tanzanian Shilling
UAH	Ukrainian Hryvnia
UGX	Ugandan Shilling
USD	United States Dollar
UYU	Uruguayan Peso
UZS	Uzbekistan Som
VEF	Venezuelan Bolivar
VND	Vietnamese Dong
VUV	Vanuatu Vatu
WST	Samoan Tala
XAF	Central African CFA franc
XCD	East Caribbean Dollar
XOF	West African CFA franc
XPF	CFP Franc
YER	Yemeni Rial
ZAR	South African Rand
ZMW	Zambian Kwacha
"""


def fetch_data(from_currency_, to_currency_, amount_):
    params = {
        'api_key': API_KEY,
        'from': from_currency_,
        'to': to_currency_,
        'amount': amount_
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch data: {str(e)}")


def convert_currency(currency_data):
    if currency_data['error'] == 0:
        return f"Converted Amount: {round(currency_data.get('amount', 'N/A'), 2)}"
    else:
        return f"Error: {currency_data.get('error_message', 'unknown error')}"
    # return str(currency_data['amount']) if (currency_data['error']) == 0 else currency_data['error_message']


# Usage
if __name__ == "__main__":
    try:
        # Get input from the user
        from_currency = input(f"Please enter the currency code to convert from (e.g. USD etc): ").upper()
        to_currency = input(f"Please enter the currency code to convert to (e.g. EUR etc): ").upper()
        amount = float(input(f"Please enter the amount to convert to : "))
        data = fetch_data(from_currency_=from_currency, to_currency_=to_currency, amount_=amount)
        result = convert_currency(data)
        print(result)

    except ValueError:
        print("Invalid input! Please enter a valid number for the amount.")

    except Exception as e:
        print(f"Failed to convert currency: {str(e)}")