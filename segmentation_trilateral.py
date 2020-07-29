# -*- coding: utf-8 -*-
import os
import re
import json
import jsonlines
import thulac
thuseg = thulac.thulac(seg_only=True, filt = False)
import MeCab                                           #日语分词
mecab_tagger = MeCab.Tagger("-Owakati")


filedir = os.getcwd()+'/preprocessed_for_trilateral_20200715_0728'
filenames = os.listdir(filedir)
file_result = filedir + "/for_draw_word_vector/data_"
badwords = ['约炮', '约 炮', '爆乳', '情趣', '迷奸', '内射', '吞精', '吞 精', '补肾', '偷情', '强奸', '捉奸', '轮奸', '献妻', '白翘', '宠幸', '屁眼', 'AV素人', '厕拍', '肥臀', 
            '淫水', '啪啪', '女优', '女 优', '增大增粗', '潮吹', '潮 吹', '吃屌', '吃 屌', '裸照', 'porn']
stopwords_zh = ['，', '的', '。', '、', '：', '和', '在', '中', '朝', '国', '了', '是', '“', '”', '为', '#', ':', '（', '）', '35520398', '🐱@', '_', '…@', '.', 'o', '去',
                '(', ')', '-', ',', '|', '就', '他们', '@', '…#', '要', '有', '看', '里', '地', '所', '一', '🐱#', '/', '】', '对', '！', '太', '真', '着', '很', '【', '入',
                '們', '写', '因为', '买', '来', '也', '。\x00PLAYTHE']
stopwords_ja = ['の', 'が', 'で', 'を', 'は', '\x00@', 'た', 'に', 'て', 'れ', 'し', '，', '。', '、', '：', '“', '”', '#', ':', '（', '）', '🐱@', '_', '…@', '.', 'o', 
                '(', ')', '-', ',', '|', '@', '…#', '一', '🐱#', '/', '】', '【']
stopwords_ko = []
stopwords = {'zh': stopwords_zh, 'ja': stopwords_ja, 'ko': stopwords_ko}

def delurl(text, url):
    for i in range (len(url)):
        text = text.replace(str(url[i]), '')
    return text

def dataprep(text, lang):
    url = re.findall(r'http[a-zA-Z0-9\.\?\/\&\=\:\^\%\$\#\!]*', text)
    text = delurl(text, url)
    if lang == 'zh':
        text = thuseg.cut(text, text=True)
    if lang == 'ja':
        text = mecab_tagger.parse(text)
    text = text.replace("\n", "\0")
    if text[0:2] == 'RT':
        text_delRT = text[3:]
    else:
        text_delRT = text
    return text_delRT

def words_frequency(inputfile, outputfile1, outputfile2, stopwords_):
    # 获得词频
    print ("1、开始计算词频...")
    wordlist = inputfile.split()
    counted_words = []
    words_count = {}
    for i in range(len(wordlist)):
        if wordlist[i] not in counted_words:
            counted_words.append(wordlist[i])
            words_count[wordlist[i]] = 1
            for j in range(i+1, len(wordlist)):
                if wordlist[i] == wordlist[j]:
                    words_count[wordlist[i]] += 1
    # 合并词与对应频数
    print ("2、合并词与对应频数...")
    words = []
    counts = []
    for items in words_count:
        words.append(items)
        counts.append(words_count[items])
    combined = list(zip(words, counts))
    # 冒泡法排大小，获得未去除停用词的词频表
    print ("3、冒泡法排大小...")
    for k in range(len(combined)-1):
        for i in range(len(combined)-1):
            if combined[i][1] < combined[i+1][1]:
                variable = combined[i]
                combined[i] = combined[i+1]
                combined[i+1] = variable
    with open (file_result[:-5] + "{}.txt".format(outputfile1), "w", encoding='utf-8') as file:
        file.write(str(combined))
    # 去除停用词后的词频表
    print ("4、去除停用词...")
    combined_no_stopwords = []
    for n in range(len(combined)):
        if combined[n][0] in stopwords_:
            continue
        combined_no_stopwords.append(combined[n])
    with open (file_result[:-5] + "{}.txt".format(outputfile2), "w", encoding='utf-8') as file:
        file.write(str(combined_no_stopwords))

print ("开始汇总语段：")

text_all = {'zh_cn': '', 'zh_cn-jp': '', 'zh_cn-jp-kp': '', 'zh_cn-kp': '', 'zh_jp': '', 'zh_jp-kp': '', 'zh_kp': '', 'ja_cn': '', 'ja_cn-jp': '', 'ja_cn-jp-kp': '', 
            'ja_cn-kp': '', 'ja_jp': '', 'ja_jp-kp': '', 'ja_kp': '', 'ko_cn': '', 'ko_cn-jp': '', 'ko_cn-jp-kp': '', 'ko_cn-kp': '', 'ko_jp': '', 'ko_jp-kp': '', 
            'ko_kp': ''}
for filename in filenames:
    print (filename)
    if filename[0:2] == 'zh':
        filepath = filedir + '/' + filename
        with open (filepath, 'r', encoding='utf-8') as f:
            for tweets in jsonlines.Reader(f):
                text = dataprep(tweets['text'], 'zh')
                signal_zh = 0
                for badword in badwords:
                    if text.find(badword) != -1:
                        # print (text)
                        signal_zh = 1
                # print (signal_zh)
                if signal_zh == 0:
                    with open (file_result + "zh" + ".txt", "a", encoding='utf-8') as file:
                        file.write(text + ' ')
                    text_all[filename[:-6]] += text
    if filename[0:2] == 'ja':
        filepath = filedir + '/' + filename
        with open (filepath, 'r', encoding='utf-8') as f:
            for tweets in jsonlines.Reader(f):
                text = dataprep(tweets['text'], 'ja')
                signal_ja = 0
                for badword in badwords:
                    if text.find(badword) != -1:
                        # print (text)
                        signal_ja = 1
                # print (signal_ja)
                if signal_ja == 0:
                    with open (file_result + "ja" + ".txt", "a", encoding='utf-8') as file:
                        file.write(text + ' ')
                    text_all[filename[:-6]] += text
    if filename[0:2] == 'ko':
        filepath = filedir + '/' + filename
        with open (filepath, 'r', encoding='utf-8') as f:
            for tweets in jsonlines.Reader(f):
                text = dataprep(tweets['text'], 'ko')
                signal_ko = 0
                for badword in badwords:
                    if text.find(badword) != -1:
                        # print (text)
                        signal_ko = 1
                # print (signal_ko)
                if signal_ko == 0:
                    with open (file_result + "ko" + ".txt", "a", encoding='utf-8') as file:
                        file.write(text + ' ')
                    text_all[filename[:-6]] += text

with open (file_result + 'text_all.jsonl', "w", encoding='utf-8') as file:
    # file.write(str(text_all))
    file.write(json.dumps(text_all)+'\n')

print ("开始求词频：")

for filename in filenames:
    print (filename)
    try:                                      # 避免for_draw...文件夹影响
        stopwords_ = stopwords[filename[0:2]]
        words_frequency(text_all[filename[:-6]], 'words_frequency_original_' + filename[:-6], 'words_frequency_no_stopwords_' + filename[:-6], stopwords_)
    except:
        assert filename == 'for_draw_word_vector'
        pass

print ("完成！")
