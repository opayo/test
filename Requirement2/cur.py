import locale

currencies = []
locales = locale.locale_alias
for l in locales.values():
    try:
        locale.setlocale(locale.LC_ALL, l)
        conv=locale.localeconv()
        currencies.append(conv['currency_symbol'])
    except:
        print(currencies)

print(currencies)