""" 本程序将收集到的原始数据按语言分类，再按是否提及指定国家分类 """
import os
import jsonlines
import json
# from langdetect import detect    # 检测正确率惨不忍睹
import langid
import re

countries_zh_en = ['中国', '中华人民共和国', '中華人民共和国', '日本', '韩国', '韓国', '大韩民国', '大韓民国', '朝鲜', '北韩', '印度尼西亚', '印尼', '马来西亚', '菲律宾', '泰国', '新加坡', '文莱', '柬埔寨', '老挝',
'缅甸', '越南', '印度', '巴基斯坦', '哈萨克斯坦', '吉尔吉斯斯坦', '塔吉克斯坦', '乌兹别克斯坦', '阿富汗', '伊朗', '蒙古', '土耳其', '沙特',
'以色列', '英国', '法国', '德国', '意大利', '奥地利', '比利时', '丹麦', '希腊', '冰岛', '爱尔兰', '卢森堡', '荷兰', '挪威', '葡萄牙', '西班牙', '瑞典',
'瑞士', '芬兰', '捷克', '匈牙利', '波兰', '斯洛伐克', '斯洛文尼亚', '爱沙尼亚', '拉脱维亚', '立陶宛', '俄罗斯', '白俄罗斯', '白罗斯', '欧盟', '美国', '加拿大',
'墨西哥', '巴西', '阿根廷', '智利', '南非', '澳大利亚', '新西兰', 'China', 'the PRC', 'Japan', 'SouthKorea', 'South Korea', 'Republic of Korea', 'NorthKorea', 'North Korea', 'Indonesia', 
'Malaysia', 'Philippines', 'Thailand', 'Singapore', 'Brunei', 'Cambodia', 'Laos', 'Myanmar', 'Vietnam', 'Viet nam', 'India', 'Pakistan', 'Kazakhstan', 'Kyrgyzstan', 
'Tajikistan', 'Uzbekistan', 'Afghanistan', 'Afghan', 'Iran', 'Mongolia', 'Turkey', 'SaudiArabia', 'Saudi Arabia', 'Israel', 'UnitedKingdom', 'United Kingdom', 'Britain', 
'France', 'Germany', 'Italy', 'Austria', 'Belgium', 'Denmark', 'Greece', 'Iceland', 'Ireland', 'Luxembourg', 'Netherlands', 'Holland', 'Norway', 'Portugal', 'Spain', 
'Sweden', 'Switzerland', 'Swiss', 'Finland', 'Czech', 'Hungary', 'Poland', 'Slovakia', 'Slovenia', 'Estonia', 'Latvia', 'Lithuania', 'Russia', 'Belarus', 'EuropeanUnion', 
'European Union', 'UnitedStates', 'United States', 'America', 'Canada', 'Mexico', 'Brazil', 'Argentina', 'Chile', 'SouthAfrica', 'South Africa', 'Australia', 
'NewZealand', 'New Zealand', '중국', '중화 인민 공화국', '일본', '대한민국', '한국']
country_CJK = ['中国', '中华人民共和国', '中華人民共和国', '日本', '韩国', '韓国', '大韩民国', '大韓民国', 'China', "People's Republic of China" , 'PRC', 'Japan', 'SouthKorea', 
                'South Korea', 'Republic of Korea', 'ROK', '중국', '중화 인민 공화국', '일본', '대한민국', '한국']
dictionary = {'中国': 'cn', '中华人民共和国': 'cn', '中華人民共和国': 'cn', 'China': 'cn', "People's Republic of China": 'cn', 'the PRC': 'cn', '중국': 'cn', '중화 인민 공화국': 'cn',
'日本':'jp', 'Japan':'jp', '일본':'jp',
'韩国': 'kp', '韓国': 'kp', '大韩民国': 'kp', '大韓民国': 'kp', 'SouthKorea': 'kp', 'South Korea': 'kp', 'Republic of Korea': 'kp', 'ROK': 'kp', '대한민국': 'kp', '한국': 'kp',
'朝鲜': 'kr', '北韩': 'kr', 'NorthKorea': 'kr', 'North Korea': 'kr', 
'印度尼西亚': 'id', '印尼': 'id', 'Indonesia': 'id', 
'马来西亚': 'my', 'Malaysia': 'my', 
'菲律宾': 'pl', 'Philippines': 'pl',
'泰国': 'th', 'Thailand': 'th', 
'新加坡': 'sg', 'Singapore': 'sg',
'文莱': 'bn', 'Brunei': 'bn', 
'柬埔寨': 'kh', 'Cambodia': 'kh', 
'老挝':'la', 'Laos':'la', 
'缅甸': 'mm', 'Myanmar': 'mm', 
'越南': 'vn', 'Vietnam': 'vn', 'Viet nam': 'vn', 
'印度': 'in', 'India': 'in', 
'巴基斯坦': 'pk', 'Pakistan': 'pk', 
'哈萨克斯坦': 'kz', 'Kazakhstan': 'kz', 
'吉尔吉斯斯坦': 'kg', 'Kyrgyzstan': 'kg',
'塔吉克斯坦': 'tj', 'Tajikistan': 'tj', 
'乌兹别克斯坦': 'uz', 'Uzbekistan': 'uz', 
'阿富汗': 'af', 'Afghanistan': 'af', 'Afghan': 'af', 
'伊朗': 'ir', 'Iran': 'ir', 
'蒙古': 'mn', 'Mongolia': 'mn', 
'土耳其': 'tr', 'Turkey': 'tr', 
'沙特': 'sa', 'SaudiArabia': 'sa', 'Saudi Arabia': 'sa', 
'以色列': 'il', 'Israel': 'il', 
'英国': 'uk', 'UnitedKingdom': 'uk', 'United Kingdom': 'uk', 'Britain': 'uk', 
'法国': 'fr', 'France': 'fr', 
'德国': 'de', 'Germany': 'de', 
'意大利': 'it', 'Italy': 'it', 
'奥地利': 'at', 'Austria': 'at', 
'比利时': 'be', 'Belgium': 'be', 
'丹麦': 'dk', 'Denmark': 'dk', 
'希腊': 'gr', 'Greece': 'gr', 
'冰岛': 'is', 'Iceland': 'is',
'爱尔兰': 'ie', 'Ireland': 'ie',
'卢森堡': 'lu', 'Luxembourg': 'lu',
'荷兰': 'nl', 'Netherlands': 'nl', 'Holland': 'nl',
'挪威': 'no', 'Norway': 'no',
'葡萄牙': 'pt', 'Portugal': 'pt',
'西班牙': 'es', 'Spain': 'es',
'瑞典': 'se', 'Sweden': 'se',
'瑞士': 'ch', 'Switzerland': 'ch', 'Swiss': 'ch',
'芬兰': 'fi', 'Finland': 'fi',
'捷克': 'cz', 'Czech': 'cz',
'匈牙利': 'hu', 'Hungary': 'hu',
'波兰': 'pl', 'Poland': 'pl',
'斯洛伐克': 'sk', 'Slovakia': 'sk',
'斯洛文尼亚': 'si', 'Slovenia': 'si',
'爱沙尼亚': 'ee', 'Estonia': 'ee',
'拉脱维亚': 'lv', 'Latvia': 'lv',
'立陶宛': 'lt', 'Lithuania': 'lt',
'俄罗斯': 'ru', 'Russia': 'ru',
'白俄罗斯': 'by', '白罗斯': 'by', 'Belarus': 'by', 
'欧盟': 'eu', 'EuropeanUnion': 'eu', 'European Union': 'eu',
'美国': 'us', 'UnitedStates': 'us', 'United States': 'us', 'America': 'us',
'加拿大': 'ca', 'Canada': 'ca', 
'墨西哥': 'mx', 'Mexico': 'mx',
'巴西': 'br', 'Brazil': 'br',
'阿根廷': 'ar', 'Argentina': 'ar',
'智利': 'cl', 'Chile': 'cl',
'南非': 'za', 'SouthAfrica': 'za', 'South Africa': 'za',
'澳大利亚': 'au', 'Australia': 'au',
'新西兰': 'nz', 'NewZealand': 'nz', 'New Zealand': 'nz'}

# filedir = os.getcwd() + '/data'
# filenames = os.listdir(filedir)
# targetdir = os.getcwd() + '/preprocessed'

# paths = ['/intl_relations_20200304_0514', '/intl_relations_20200515_0604', '/intl_relations_20200605_0624', '/intl_relations_20200625_0714', '/intl_relations_20200715_0804']
paths = ['/intl_relations_20200715_0804']
targetdir = os.getcwd() + '/preprocessed_for_trilateral_latter'

for path in paths:
    print (path)
    filedir = os.getcwd() + path
    filenames = os.listdir(filedir)

    for filename in filenames:
        print (filename)
        filepath = filedir + '/' + filename
        # print (filepath)
        with open (filepath, 'r') as f:
            try:
                for tweets in jsonlines.Reader(f):
                    try:
                        text = tweets['text'].lower()
                        try:
                            lang = str(langid.classify(text)[0])
                            if lang == 'ja' or lang == 'ko' or lang == 'zh':                  
                                country_codes = []
                                country_names = ''
                                # for countries in countries_zh_en:
                                for countries in country_CJK:
                                    if re.findall(countries.lower(), text) != []:
                                        country_codes.append(dictionary[countries])
                                if country_codes == []:
                                    continue
                                country_codes = list(set(country_codes))   #去除重复项
                                country_codes.sort()
                                underline = '-'
                                country_names = underline.join(country_codes)
                                with open ('{}/{}.jsonl'.format(targetdir, lang + '_' + country_names), "a") as file:
                                    file.write(json.dumps(tweets)+'\n')
                                # print ('2')
                        except:
                            pass
                            # with open ('{}/not_a_language_{}.jsonl'.format(targetdir, country_names), "a") as file:
                            #     file.write(json.dumps(tweets)+'\n')
                            # print ('3')
                    except:
                        print (filename)
                        try:
                            print (tweets['id'])
                        except:
                            try:
                                print (tweets['limit'])
                            except:
                                print (tweets)
            except:
                print ("文件内没有内容！文件名：" + filename)
                continue