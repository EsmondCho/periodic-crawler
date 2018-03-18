from analyzer.models import *


def input_coin_upbit():
    coin_ko_name_list = []
    coin_symbol_list = []

    f = open("/Users/esmond/Desktop/coin_upbit", 'r')
    lines = f.readlines()
    for index, line in enumerate(lines):
        print(line)

    f.close()

    return True

def input_coin_coinmarketcap():

    f = open("/Users/esmond/Desktop/coin_coinmarketcap.txt", 'r')
    lines = f.readlines()

    for line in lines:
        coin_info_list = []
        coin_info_list = line.split("\t")
        coin_symbol = coin_info_list[2]
        coin_eng_name = coin_info_list[1]

        sym = CoSymTb.objects.create(
            cosm_symbol = coin_symbol
        )
        sym.save()





        # comment = CoTb.objects.create(
        #     ps_id=post, co_content=content,
        #     co_date=timezone.make_aware(co_date_obj)
        # )
        # comment.save()

    # print(coin_symbol_list)
    # print(coin_eng_name_list)

    f.close()
    return True