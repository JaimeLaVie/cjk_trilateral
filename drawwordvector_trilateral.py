# -*- coding: utf-8 -*-
import os
import gensim
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import pandas as pd
pd.options.mode.chained_assignment = None
from sklearn.manifold import TSNE
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"simfang.ttf", size=14)
font_ko = FontProperties(fname=r"NanumGothic.ttf", size=14)
import matplotlib.patches as mpatches
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

basic_path = os.getcwd()
save_path = basic_path + '/' + 'preprocessed_for_trilateral_20200715_0728/for_draw_word_vector/'
doc_zh = "data_zh"
doc_ja = "data_ja"
doc_ko = "data_ko"
word_frequency_zh_cn = "words_frequency_no_stopwords_zh_cn.txt"
word_frequency_zh_cn_jp = "words_frequency_no_stopwords_zh_cn-jp.txt"
word_frequency_zh_cn_jp_kp = "words_frequency_no_stopwords_zh_cn-jp-kp.txt"
word_frequency_zh_cn_kp = "words_frequency_no_stopwords_zh_cn-kp.txt"
word_frequency_zh_jp = "words_frequency_no_stopwords_zh_jp.txt"
word_frequency_zh_jp_kp = "words_frequency_no_stopwords_zh_jp-kp.txt"
word_frequency_zh_kp = "words_frequency_no_stopwords_zh_kp.txt"
word_frequency_ja_cn = "words_frequency_no_stopwords_ja_cn.txt"
word_frequency_ja_cn_jp = "words_frequency_no_stopwords_ja_cn-jp.txt"
word_frequency_ja_cn_jp_kp = "words_frequency_no_stopwords_ja_cn-jp-kp.txt"
word_frequency_ja_cn_kp = "words_frequency_no_stopwords_ja_cn-kp.txt"
word_frequency_ja_jp = "words_frequency_no_stopwords_ja_jp.txt"
word_frequency_ja_jp_kp = "words_frequency_no_stopwords_ja_jp-kp.txt"
word_frequency_ja_kp = "words_frequency_no_stopwords_ja_kp.txt"
word_frequency_ko_cn = "words_frequency_no_stopwords_ko_cn.txt"
word_frequency_ko_cn_jp = "words_frequency_no_stopwords_ko_cn-jp.txt"
word_frequency_ko_cn_jp_kp = "words_frequency_no_stopwords_ko_cn-jp-kp.txt"
word_frequency_ko_cn_kp = "words_frequency_no_stopwords_ko_cn-kp.txt"
word_frequency_ko_jp = "words_frequency_no_stopwords_ko_jp.txt"
word_frequency_ko_jp_kp = "words_frequency_no_stopwords_ko_jp-kp.txt"
word_frequency_ko_kp = "words_frequency_no_stopwords_ko_kp.txt"

def getword(text):
    index = text.rfind("'")
    return text[1:index]

def pickwords(file_path, num):
    with open (file_path, "r") as f:
        str = f.read()
    wordlist = []
    str = str[2:]
    str = str.split("), (")
    i = 0
    for words in str:
        word = getword(words)
        # if word.lower() not in stopwords and word.find('\x00') is -1:
        wordlist.append(word)
        i += 1
        if i == num:
            break
        # with open (file_result, "a") as file:
        #     file.write(word + '\n')
    return wordlist

""" def getkeywords(keywordpath):
    word_list = []
    with open(keywordpath, 'r', encoding="utf-8") as f:
        for line in f:
            keyword = line.replace('\n', '')
            word_list.append(keyword)

    return word_list """

def makewordvector(docpath, min_count):
    text = open(save_path + docpath + '.txt', 'r',encoding='utf-8')
    model = Word2Vec(LineSentence(text), sg=0,size=200, window=5, min_count=min_count, workers=6)
    print(docpath + 'model训练完成')
    model.save(save_path + '{}.word2vec'.format(docpath))

makewordvector(doc_zh, 100)     # 注意第二个参数！中文语段较少，相应地最小计数词频也应小，不然没几个词会出现在图中
makewordvector(doc_ja, 1000)
makewordvector(doc_ko, 10)

def testtheresult(modelpath):
    model = gensim.models.Word2Vec.load(modelpath)
    print(model.similarity('中国','韩国'))  #相似度为0.60256344
    print(model.similarity('繁荣富强','国泰民安'))  #相似度为0.49495476

    result1 = pd.Series(model.most_similar(u'中共')) #查找近义相关词
    print(result1)
    result2 = pd.Series(model.most_similar(u'国庆'))
    print(result2)
    print(model.wv['中国']) #查看中国的词向量（单个词语的词向量）
    with open('testtheresult.txt', 'w') as f:
        f.write("model.similarity('中国','韩国') = " + str(model.similarity('中国','韩国')) + '\n')
        f.write("model.similarity('繁荣富强','国泰民安') = " + str(model.similarity('繁荣富强','国泰民安')) + '\n')
        f.write("model.most_similar(u'中共') = " + str(result1) + '\n')
        f.write("model.most_similar(u'国庆') = " + str(result2) + '\n')
        f.write("model.wv['中国'] = " + str(model.wv['中国']))

# testtheresult('data_zh.word2vec')

model_zh = gensim.models.Word2Vec.load(save_path + 'data_zh.word2vec')
model_ja = gensim.models.Word2Vec.load(save_path + 'data_ja.word2vec')
model_ko = gensim.models.Word2Vec.load(save_path + 'data_ko.word2vec')

def tsne_plot(model, chosen_words, picname):
    "Creates and TSNE model and plots it"
    print ("开始画图：" + picname)
    labels = []
    tokens = []
    # chosen_words_zh = ['🇨🇳', '70', '祖国','国庆', '快乐','生日']
    # chosen_words_en = ['China', 'Day', 'happy','Beijing']
    # if picname[-2:] == 'zh':
    #     for word in model.wv.vocab:
    #     # for word in chosen_words_zh:
    #         tokens.append(model[word])
    #         labels.append(word)
    # elif picname[-2:] == 'ja':
    #     for word in model.wv.vocab:
    #     # for word in chosen_words_en:
    #         tokens.append(model[word])
    #         labels.append(word)
    
    for word in model.wv.vocab:
        # for word in chosen_words_zh:
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)
    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    print ('len(x) = ', len(x))
    for i in range(len(x)):
        if labels[i] in chosen_words:
            dot1 = plt.scatter(x[i], y[i], s = 40, c = 'b', marker = 'o', edgecolors = 'none')
            plt.annotate(labels[i],
                        fontproperties=font,
                        xy=(x[i], y[i]),
                        xytext=(5, 2),
                        fontsize = 'xx-large',
                        textcoords='offset points',
                        color='b',
                        ha='right',
                        va='bottom')
    # plt.legend([dot1], ['frequently used words in tweets'], fontsize = 'xx-large')
    # plt.title('Word Vectors')
    plt.savefig(save_path + 'word_vector_images/{}.jpg'.format(picname))
    plt.clf()

def tsne_plot_ko(model, chosen_words, picname):
    "Creates and TSNE model and plots it"
    print ("开始画图：" + picname)
    labels = []
    tokens = []
    # chosen_words_zh = ['🇨🇳', '70', '祖国','国庆', '快乐','生日']
    # chosen_words_en = ['China', 'Day', 'happy','Beijing']
    # if picname[-2:] == 'zh':
    #     for word in model.wv.vocab:
    #     # for word in chosen_words_zh:
    #         tokens.append(model[word])
    #         labels.append(word)
    # elif picname[-2:] == 'ja':
    #     for word in model.wv.vocab:
    #     # for word in chosen_words_en:
    #         tokens.append(model[word])
    #         labels.append(word)
    
    for word in model.wv.vocab:
        # for word in chosen_words_zh:
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)
    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    print ('len(x) = ', len(x))
    for i in range(len(x)):
        if labels[i] in chosen_words:
            dot1 = plt.scatter(x[i], y[i], s = 40, c = 'b', marker = 'o', edgecolors = 'none')
            plt.annotate(labels[i],
                        fontproperties=font_ko,
                        xy=(x[i], y[i]),
                        xytext=(5, 2),
                        fontsize = 'xx-large',
                        textcoords='offset points',
                        color='b',
                        ha='right',
                        va='bottom')
    # plt.legend([dot1], ['frequently used words in tweets'], fontsize = 'xx-large')
    # plt.title('Word Vectors')
    plt.savefig(save_path + 'word_vector_images/{}.jpg'.format(picname))
    plt.clf()

word_frequency_zh_cn
word_frequency_zh_cn_jp = "words_frequency_no_stopwords_zh_cn-jp.txt"
word_frequency_zh_cn_jp_kp = "words_frequency_no_stopwords_zh_cn-jp-kp.txt"
word_frequency_zh_cn_kp = "words_frequency_no_stopwords_zh_cn-kp.txt"
word_frequency_zh_jp = "words_frequency_no_stopwords_zh_jp.txt"
word_frequency_zh_jp_kp = "words_frequency_no_stopwords_zh_jp-kp.txt"
word_frequency_zh_kp = "words_frequency_no_stopwords_zh_kp.txt"
word_frequency_ja_cn = "words_frequency_no_stopwords_ja_cn.txt"
word_frequency_ja_cn_jp = "words_frequency_no_stopwords_ja_cn-jp.txt"
word_frequency_ja_cn_jp_kp = "words_frequency_no_stopwords_ja_cn-jp-kp.txt"
word_frequency_ja_cn_kp = "words_frequency_no_stopwords_ja_cn-kp.txt"
word_frequency_ja_jp = "words_frequency_no_stopwords_ja_jp.txt"
word_frequency_ja_jp_kp = "words_frequency_no_stopwords_ja_jp-kp.txt"
word_frequency_ja_kp = "words_frequency_no_stopwords_ja_kp.txt"
word_frequency_ko_cn = "words_frequency_no_stopwords_ko_cn.txt"
word_frequency_ko_cn_jp = "words_frequency_no_stopwords_ko_cn-jp.txt"
word_frequency_ko_cn_jp_kp = "words_frequency_no_stopwords_ko_cn-jp-kp.txt"
word_frequency_ko_cn_kp = "words_frequency_no_stopwords_ko_cn-kp.txt"
word_frequency_ko_jp = "words_frequency_no_stopwords_ko_jp.txt"
word_frequency_ko_jp_kp = "words_frequency_no_stopwords_ko_jp-kp.txt"
word_frequency_ko_kp = "words_frequency_no_stopwords_ko_kp.txt"

chosen_words_zh_cn = pickwords(save_path + word_frequency_zh_cn, 400)
print ("chosen_words_zh_cn")
chosen_words_zh_cn_jp = pickwords(save_path + word_frequency_zh_cn_jp, 400)
print ("chosen_words_zh_cn_jp")
chosen_words_zh_cn_jp_kp = pickwords(save_path + word_frequency_zh_cn_jp_kp, 400)
print ("chosen_words_zh_cn_jp_kp")
chosen_words_zh_cn_kp = pickwords(save_path + word_frequency_zh_cn_kp, 400)
print ("chosen_words_zh_cn_kp", )
chosen_words_zh_jp = pickwords(save_path + word_frequency_zh_jp, 400)
print ("chosen_words_zh_jp")
chosen_words_zh_jp_kp = pickwords(save_path + word_frequency_zh_jp_kp, 400)
print ("chosen_words_zh_jp_kp")
chosen_words_zh_kp = pickwords(save_path + word_frequency_zh_kp, 400)
print ("chosen_words_zh_kp")

chosen_words_ja_cn = pickwords(save_path + word_frequency_ja_cn, 400)
print ("chosen_words_ja_cn")
chosen_words_ja_cn_jp = pickwords(save_path + word_frequency_ja_cn_jp, 400)
print ("chosen_words_ja_cn_jp")
chosen_words_ja_cn_jp_kp = pickwords(save_path + word_frequency_ja_cn_jp_kp, 400)
print ("chosen_words_ja_cn_jp_kp")
chosen_words_ja_cn_kp = pickwords(save_path + word_frequency_ja_cn_kp, 400)
print ("chosen_words_ja_cn_kp")
chosen_words_ja_jp = pickwords(save_path + word_frequency_ja_jp, 400)
print ("chosen_words_ja_jp")
chosen_words_ja_jp_kp = pickwords(save_path + word_frequency_ja_jp_kp, 400)
print ("chosen_words_ja_jp_kp")
chosen_words_ja_kp = pickwords(save_path + word_frequency_ja_kp, 400)
print ("chosen_words_ja_kp")

chosen_words_ko_cn = pickwords(save_path + word_frequency_ko_cn, 400)
print ("chosen_words_ko_cn")
chosen_words_ko_cn_jp = pickwords(save_path + word_frequency_ko_cn_jp, 400)
print ("chosen_words_ko_cn_jp")
chosen_words_ko_cn_jp_kp = pickwords(save_path + word_frequency_ko_cn_jp_kp, 400)
print ("chosen_words_ko_cn_jp_kp")
chosen_words_ko_cn_kp = pickwords(save_path + word_frequency_ko_cn_kp, 400)
print ("chosen_words_ko_cn_kp")
chosen_words_ko_jp = pickwords(save_path + word_frequency_ko_jp, 400)
print ("chosen_words_ko_jp")
chosen_words_ko_jp_kp = pickwords(save_path + word_frequency_ko_jp_kp, 400)
print ("chosen_words_ko_jp_kp")
chosen_words_ko_kp = pickwords(save_path + word_frequency_ko_kp, 400)
print ("chosen_words_ko_kp")

tsne_plot(model_zh, chosen_words_zh_cn, 'chosen_word_vector_zh_cn')
tsne_plot(model_zh, chosen_words_zh_cn_jp, 'chosen_word_vector_zh_cn_jp')
tsne_plot(model_zh, chosen_words_zh_cn_jp_kp, 'chosen_word_vector_zh_cn_jp_kp')
tsne_plot(model_zh, chosen_words_zh_cn_kp, 'chosen_word_vector_zh_cn_kp')
tsne_plot(model_zh, chosen_words_zh_jp, 'chosen_word_vector_zh_jp')
tsne_plot(model_zh, chosen_words_zh_jp_kp, 'chosen_word_vector_zh_jp_kp')
tsne_plot(model_zh, chosen_words_zh_kp, 'chosen_word_vector_zh_kp')

tsne_plot(model_ja, chosen_words_ja_cn, 'chosen_word_vector_ja_cn')
tsne_plot(model_ja, chosen_words_ja_cn_jp, 'chosen_word_vector_ja_cn_jp')
tsne_plot(model_ja, chosen_words_ja_cn_jp_kp, 'chosen_word_vector_ja_cn_jp_kp')
tsne_plot(model_ja, chosen_words_ja_cn_kp, 'chosen_word_vector_ja_cn_kp')
tsne_plot(model_ja, chosen_words_ja_jp, 'chosen_word_vector_ja_jp')
tsne_plot(model_ja, chosen_words_ja_jp_kp, 'chosen_word_vector_ja_jp_kp')
tsne_plot(model_ja, chosen_words_ja_kp, 'chosen_word_vector_ja_kp')

tsne_plot_ko(model_ko, chosen_words_ko_cn, 'chosen_word_vector_ko_cn')
tsne_plot_ko(model_ko, chosen_words_ko_cn_jp, 'chosen_word_vector_ko_cn_jp')
tsne_plot_ko(model_ko, chosen_words_ko_cn_jp_kp, 'chosen_word_vector_ko_cn_jp_kp')
tsne_plot_ko(model_ko, chosen_words_ko_cn_kp, 'chosen_word_vector_ko_cn_kp')
tsne_plot_ko(model_ko, chosen_words_ko_jp, 'chosen_word_vector_ko_jp')
tsne_plot_ko(model_ko, chosen_words_ko_jp_kp, 'chosen_word_vector_ko_jp_kp')
tsne_plot_ko(model_ko, chosen_words_ko_kp, 'chosen_word_vector_ko_kp')