from analyzer.models import *


def input_coin_upbit():

    f = open("/Users/esmond/Desktop/coin_upbit.txt", 'r')
    lines = f.readlines()
    for index, line in enumerate(lines):
        if index%10 == 2:
            coin_name_ko = line.strip()
        elif index%10 == 3:
            print(index)
            coin_symbol = line.split('/')[0]
            coins = []
            coins = CoNmTb.objects.filter(conm_symbol=coin_symbol)
            if coins:
                coins[0].conm_name_ko = coin_name_ko
                coins[0].save()
            else:
                coin = CoNmTb.objects.create(
                    conm_name_ko=coin_name_ko,
                    conm_symbol=coin_symbol
                )
                coin.save()

    f.close()

    return True

def input_coin_coinmarketcap():

    f = open("/Users/esmond/Desktop/coin_coinmarketcap.txt", 'r')
    lines = f.readlines()

    for index, line in enumerate(lines):
        print(index)
        coin_info_list = []
        coin_info_list = line.split("\t")
        coin_symbol = coin_info_list[2]
        coin_name_eng = coin_info_list[1]

        if CoNmTb.objects.filter(conm_name_eng=coin_name_eng):
            continue

        coin = CoNmTb.objects.create(
            conm_name_eng=coin_name_eng,
            conm_symbol=coin_symbol
        )
        coin.save()

    f.close()

    return True