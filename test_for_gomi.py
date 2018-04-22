# -*- coding: utf-8 -*-
f = open('gomi.txt')
text_sjis = f.read()
f.close()
text = text_sjis.decode('utf-8')

# ファイル整形
import re
from janome.tokenizer import Tokenizer
from gensim.models import word2vec


def extract_words(text):
    tokens = t.tokenize(text)
    return [token.base_form for token in tokens]
	#if token.part_of_speech.split(',')[0] in[u'名詞', u'動詞']]



# | の除去
text = text.replace(u'|', u'')
# ルビの削除
text = re.sub(u'《.+?》', u'', text)
# 入力注の削除
text = re.sub(u'［＃.+?］', u'',text)
# 空行の削除
text = re.sub(u'\n\n', '\n', text) 
text = re.sub(u'\r', '', text)

regexp = re.compile(r'^(?:\xEF\xBD[\xA1-\xBF]|\xEF\xBE[\x80-\x9F])+$') #半角のみの単語を弾くために 
rules = re.compile(r'^[-②①③「」\[\]./｡)(（） ○]*$') #よく使われる符号を弾くために。

# Tokenneizerインスタンスの生成 
t = Tokenizer()

# テキストを引数として、形態素解析の結果、名詞・動詞原型のみを配列で抽出する関数を定義


#改行コードで区切る
sentences = text.split(u'\n')
# それぞれの文章を単語リストに変換(処理に数分かかります)
word_list = [extract_words(sentence) for sentence in sentences]

# 結果の一部を確認 


# size: 圧縮次元数
# min_count: 出現頻度の低いものをカットする
# window: 前後の単語を拾う際の窓の広さを決める
# iter: 機械学習の繰り返し回数(デフォルト:5)十分学習できていないときにこの値を調整する
# model.wv.most_similarの結果が1に近いものばかりで、model.dict['wv']のベクトル値が小さい値ばかりの 
# ときは、学習回数が少ないと考えられます。
# その場合、iterの値を大きくして、再度学習を行います。

# 事前準備したword_listを使ってWord2Vecの学習実施
model = word2vec.Word2Vec(word_list, size=200,min_count=3,window=5,iter=100)
#print model.__dict__['wv'][u'世間']
ret = model.wv.most_similar(positive=[u'廃棄']) 
for item in ret:
    print item[0], item[1]

