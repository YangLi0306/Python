import jieba
import collections
import re
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
from pyecharts import options as opts
from pyecharts.globals import ThemeType


def deal_txt(seg_list_exact):
    result_list = []
    with open('C:\\Users\\HP\\Desktop\\baidu_stopwords.txt', encoding='utf-8') as f:  # 使用百度的停词
        con = f.readlines()
        stop_words = set()

        for i in con:
            i = i.replace("\n", "")
            stop_words.add(i)
        for word in seg_list_exact:
            if word not in stop_words and len(word) > 1:
                result_list.append(word)
    return result_list


# 渲染词云

def render_cloud(word_counts_top100):
    word1 = WordCloud(init_opts=opts.InitOpts(width='1350px', height='750px', theme=ThemeType.MACARONS))

    word1.add('词频', data_pair=word_counts_top100,
              word_size_range=[15, 108], textstyle_opts=opts.TextStyleOpts(font_family='cursive'),
              shape=SymbolType.DIAMOND)

    word1.set_global_opts(title_opts=opts.TitleOpts('评论云图'),
                          toolbox_opts=opts.ToolboxOpts(is_show=True, orient='vertical'),
                          tooltip_opts=opts.TooltipOpts(is_show=True, background_color='red', border_color='yellow'))

    word1.render("评论云图.html")


if __name__ == '__main__':
    with open('C:\\Users\\HP\\Desktop\\content.txt', errors='ignore', encoding='GB2312') as f: #需要分词的文本
        date = f.read()
    new_data = re.findall('[\u4e00-\u9fa5]+', date, re.S)
    new_data = " ".join(new_data)
    seg_list_exact = jieba.cut(new_data, cut_all=True)
    final_list = deal_txt(seg_list_exact)
    word_counts = collections.Counter(final_list)
    word_counts_top100 = word_counts.most_common(100)
    render_cloud(word_counts_top100)
