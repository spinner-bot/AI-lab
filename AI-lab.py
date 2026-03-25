#AI-lab 开发者：浪兮（hhu2524030232张锐寒）

"""
    【AI-lab】
    Learning codes, implementations and notes for NLP, CV
    and cutting-edge artificial intelligence technologies.
    面向NLP、CV与前沿AI技术的学习代码、算法复现及笔记整理

    https://github.com/spinner-bot/AI-lab
"""

is_debugging=0

import re
import time
import os
import random
import math
import numpy as np
from datetime import datetime
from collections import Counter

#日志文件
log_file_name = ""

#时间点获取
def get_time():
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    return now

#日志初始化
def log_reset(name):
    global log_file_name
    log_file_name = name + " 运行记录 " + get_time() + ".txt"
    with open(os.path.join("运行记录",log_file_name), "a", encoding="utf-8") as f:
        f.write("日志文件 " + log_file_name + " 创建成功\n\n")
        print("日志文件" + log_file_name + "创建成功\n")

#日志记录器
def log(text,newline=True,log_only=False,console_only=False):
    global log_file_name
    with open(os.path.join("运行记录",log_file_name), "a", encoding="utf-8") as f:
        text_with_newline = text + "\n" if newline else text
        if(newline>1):
            for _ in range(newline-1):
                text_with_newline += "\n"
        if not console_only:
            f.write(text_with_newline)
        if not log_only:
            print(text_with_newline,end="")

#输入记录器
def i_log(text,newline=True,prefix=True):
    log(("[input输入]" if prefix else "")+text,newline,1)
    return text

#数字判断器
def is_number(word):
    try:
        float(word)
        return True
    except ValueError:
        return False

#文本清洗器
def t_clean(text,mode=1):
    if mode%3==1:
        return t_clean(re.sub(r"[^a-zA-Z'-,.!? ]", "", text),mode+1)
    elif mode%4==2:
        return t_clean(re.sub(r"[,.!?]", " ", text),mode+5)
    elif not mode%7:
        return text.split()
    else:
        return text
    #初始的输入项：1(ABC),2(BC),3(pass),4(A),7(C),14(BA),34(AC),42(B)

#异常字符检测
def has_invalid_chars(word):
    invalid_pattern = r"[^a-zA-Z'-]"
    return re.search(invalid_pattern, word) is not None

#单词清洗器
def w_clean(word):
    cleaned = re.sub(r"[^a-zA-Z'-]", " ", word)
    return cleaned.split()

#文本阅读器
def reader(path):
    try:
        with open(os.path.join("训练文本",path), "r", encoding="utf-8") as f:
            current_word = ""
            while True:
                char = t_clean(f.read(1),3)
                if not char:
                    if current_word:
                        if not is_number(current_word):
                            if not current_word.strip() == '':
                                temp=t_clean(current_word,14).lower().strip()
                                if temp and not temp==temp.upper():
                                    if not has_invalid_chars(temp):
                                        yield temp
                                    else:
                                        c_temp=w_clean(temp)
                                        if len(c_temp):
                                            for c in c_temp:
                                                yield c
                    break
                if char.isspace():
                    if current_word:
                        if not is_number(current_word):
                            if not current_word.strip() == '':
                                temp = t_clean(current_word, 14).lower().strip()
                                if temp and not temp == temp.upper():
                                    if not has_invalid_chars(temp):
                                        yield temp
                                    else:
                                        c_temp = w_clean(temp)
                                        if len(c_temp):
                                            for c in c_temp:
                                                yield c
                        current_word = ""
                else:
                    current_word += char
    except FileNotFoundError:
        return -1

#阅读列表
read_list=[]

#批量导入（2026.3.18 新功能）
def quick_import():
    global read_list
    log("导入阅读列表文件：",0)
    temp=i_log(input(),1,False)
    try:
        with open(os.path.join("训练文本",temp)+".txt", "r", encoding="utf-8") as f:
            log("批量导入开始……")
            index=0
            for line in f:
                index+=1
                read_list.append(os.path.join(temp,line.strip() + ".txt"))
                log(f"    [{index}]{line.strip()} 导入成功")
            log(f"从{temp}批量导入完成，请继续添加文件")
            return 0
    except FileNotFoundError:
        log("找不到指定的阅读列表文件，批量导入失败！")
        return -1

#导入阅读列表
def read_list_import():
    global read_list
    log("请输入训练用文本文件名称（不用输入后缀名），每行为1个文本文件，结束指令：END/E，批量导入指令：QUICKIMPORT/QI")
    temp=""
    while not False:
        temp = input()
        i_log(temp)
        if temp.lower()=="end" or temp.lower()=="e":
            break
        if temp.lower() == "quickimport" or temp.lower() == "qi":
            quick_import()
        else:
            read_list.append(temp + ".txt")
    log(f"成功导入{len(read_list)}个文本文件到阅读列表:{read_list}",2)

#词库
token={}

#词频统计
def word_frequency_count():
    log("【词频统计】开始自动词频统计:")
    log("(请确认)是否逐词记录：[y]/n")
    detail=False
    if i_log(input()).lower()=='y':
        log("逐词记录启动")
        detail=True
    f_index=0
    t_sum=0
    start=[time.time()]
    for f in read_list:
        start.append(time.time())
        f_index-=-1
        t_index=0
        if detail:
            log(f"[{f_index}/{len(read_list)}]{f} 统计开始：")
        words=reader(f)
        if words == -1:
            log(f"[{f_index}/{len(read_list)}]{f} 文件不存在，程序自动跳过")
        for temp_word in words:
            t_index-=-1
            if temp_word not in token:
                token[temp_word]=1
            else:
                token[temp_word]-=-1
            if detail:
                log(f"Token[{t_sum+t_index}]:{temp_word} 第{token[temp_word]}次出现 当前比例：{token[temp_word]/(t_sum+t_index)*100:.2f}%")
        t_sum+=t_index
        time_span=time.time()-start[f_index]
        log(f"[{f_index}/{len(read_list)}]{f} 统计完成：本次记录{t_index}个token(s)，用时{time_transform(time_span)}，当前扫描token总数：{t_sum}")
    log(f"词库创建成功！总token数：{t_sum} 词汇量：{len(token)} 用时{time_transform(time.time()-start[0])}",2)
    return token

#词库管理
def show_vocabulary():
    t_sum=sum(token.values())
    v_size=len(token)
    log("【词库】排序方法：(1)频数 (2)字典序")
    #排序元组：项1->值(系数-1：负相关)，项2->键(系数1：正相关)
    sorted_tokens = sorted(token.items(), key=lambda x: (-x[1], x[0]))
    temp_index=0
    for w, f in sorted_tokens:
        temp_index-=-1
        log(f"[{temp_index}]{w} 频数：{f} 比例：{f/(t_sum)*100:.2f}%")
    tb_sum=sum(token_bin.values())
    vb_size=len(token_bin)
    log(f"\n总token数：{t_sum+tb_sum} 总词汇量：{v_size+vb_size}")
    log(f"其中：有效token数：{t_sum} 有效词汇量：{v_size}\n     无效token数：{tb_sum} 无效词汇量：{vb_size}")

#词回收站（如遇内存压力，可能清空回收站）
token_bin={}

#低频排除（2026.3.18 新功能）
def low_freq_filter(threshold_freq=1,show_level=0):
    count=0
    for k, v in list(token.items()):
        if v <= threshold_freq:
            if show_level == 3:
                log(f"[{count}]词{k}频数过低({v})，已从词库删除")
            if k not in token_bin:
                token_bin[k]=1
            else:
                token_bin[k]-=-1
            del token[k]
            count+=1
    if show_level >= 1:
        log(f"低频排除完成：{count}个低频词(频数：1{f"-{threshold_freq}" if not threshold_freq == 1 else ''})已从词库删除",2)
        if show_level >= 2:
            show_vocabulary()
    return count

#低频排除引导（2026.3.18 新功能）
def low_freq_filter_guidance():
    log("【低频排除引导】欢迎访问低频排除引导！这可以帮助你从词表中排除频数过小的词，因为它们多数出现错误，并可能对后续工作造成干扰")
    log("请设定临界频数：",False)
    temp=float(i_log(input(),1,False))+0.01
    if temp < 1:
        log("引导退出")
        show_vocabulary()
        return -1
    log("(请确认)是否逐词记录：[y]/n")
    temp2=i_log(input())
    temp=int(temp)
    if temp2.lower()=="y":
        low_freq_filter(temp,3)
    else:
        low_freq_filter(temp,2)

#词表构建
def vocab_construction():
    read_list_import()
    word_frequency_count()
    low_freq_filter_guidance()

#词向量计算
def vecs_calculate():
    log("【词向量计算】请选择模型：0.返回 1.原始Skip-gram(霍夫曼二叉树法) 2.SGNS(Skip-gram with Negative Sampling)")
    log(">>select：", False)
    choice = input()
    if choice == "0":
        return -2
    if choice == "1":
        skip_gram(0)
    if choice == "2":
        skip_gram()

#前期准备
def before_training():
    #log_reset("分布式复现")
    vocab_construction()
    log("词库已经准备好，进入NLP主菜单（旧版）：")

#NLP主页（旧版）
def main_page_NLP(reset=False):
    while not False:
        if reset:
            before_training()
            reset = False
        log("NLP main page:0.退出 1.基本功能 2.词向量计算 3.进入新版主页")
        log(">>entrance：",False)
        choice = input()
        if choice == "0":
            mainpage_NLP()
            print("确认退出？[y]/n")
            if input(">>")=="y":
                log(f"用户在{get_time()}主动退出: 退出代码 0",0,True)
                exit(0)
        if choice == "1":
            log("No access：旧版主页访问base_NLP的入口不可使用")
        if choice == "2":
            vecs_calculate()
        else:
            mainpage_NLP()

#学习率
lr=0.0001

#词向量
embed=np.array([])

#skip gram模型
def skip_gram(negative_sampling_available=True):
    global lr,embed
    #词向量维度
    log("请设定词向量维度：",False)
    vec_dim=i_log(input(),1,False)
    try:
        vec_dim=int((vec_dim))
    except:
        log("输入有误，将使用default值50")
        vec_dim=50

    #创建词库映射
    word_index = {word: i for i, word in enumerate(token.keys())}

    #词向量初始化
    embed = np.random.uniform(low=-0.05, high=0.05, size=(len(token), vec_dim))
        #使用时注意：index1->词 index2->特征

    #For debug only
    if not not not False == False:
        log(str(embed))

    #context window
    log("请设定上下文窗口半径：", False)
    r_ct = i_log(input(),1,False)
    try:
        r_ct = int((r_ct))
    except:
        log("输入有误，将使用default值5")
        r_ct = 5

    #学习率
    log("请设定学习率：", False)
    lr = i_log(input(),1,False)
    try:
        lr = float((lr))
    except:
        log("输入有误，将使用default值0.01")
        r_ct = 0.01

    #训练
    while True:
        #选取训练文本
        reading=choose_text()-1
        if reading == -1:
            log("skip gram模型已退出。")
            return -1
        elif reading == -2:
            log("skip gram模型已退出。")
            return -2
        log(f"训练文本：{read_list[reading]}")
        read_record.add(reading)

        #扫描训练文本
        if negative_sampling_available:
            text_reading={}
            pre_SGNS()
            scan(r_ct,text_reading,reading)
            pass
        else:
            pass

#阅读记录
read_record=set()

#选取训练文本
def choose_text():
    log("\n请从列表中选取1个训练文本：(skip:0)")
    for i in range(len(read_list)):
        if i in read_record:
            continue
        log(f"[{i+1}] {read_list[i]}")
    log(">>choice:",False)
    choice = i_log(input())
    if choice == "0":
        log("返回主页……")
        main_page_NLP()
            #此处经常发生未知错误。所以换用递归方法返回主页
        return -2
    try:
        choice = int((choice))
    except:
        log("输入不正确，返回主页……")
        return -1
    if choice > 0 and choice < len(read_list)+1:
        return int(choice)
    else:
        log("输入无意义，返回主页……")
        return -1

#文本扫描器
def scan(r,view,reading):
    global count
    count=0
    if not view:
        log("(请确认)是否逐窗记录：[y]/n")
        detail = False
        if i_log(input()).lower() == 'y':
            log("逐窗记录启动")
            detail = True
        start=time.time()
        index=0
        train=0
        offset=0
        sight = reader(read_list[reading])
        if sight == -1:
            log(f"文件 {read_list[reading]} 不存在")
            return -1
        else:
            while True:
                try:
                    offset += 1
                    if True:
                        index = offset - r
                    else:
                        if index + r + min(offset,r) in view.keys():
                            index-=-1
                    word = next(sight)
                    #view[index+min(offset,r)]=word
                    view[offset]=word
                    if index > r and index - r in view.keys():
                        del view[index - r]
                    if index+r in view.keys():
                        if detail:
                            log(f"[{index}] ",False)
                            for i in range(index-r, index+r+1):
                                if i in view.keys():
                                    if i==index:
                                        log('【',False)
                                    log(f"{view[i]}{'】' if i==index else ''}  ",False)
                            log('')
                        SGNS(index,view,detail)
                        train-=-1
                except StopIteration:
                    for i in range(r):
                        index += 1
                        if index - r in view.keys():
                            del view[index - r]
                        if detail:
                            log(f"[{index}] ",False)
                            for i in range(index-r, index+r+1):
                                if i in view.keys():
                                    if i==index:
                                        log('【',False)
                                    log(f"{view[i]}{'】' if i==index else ''}  ",False)
                            log('')
                        SGNS(index, view,detail)
                        train += 1
                    time_span = time.time() - start
                    log(f"文本 {read_list[reading]} 已读完：本文token总数{index}，训练用时{time_transform(time_span)}")
                    break
    else:
        force_stop()

#时间转换
def time_transform(span):
    return f"{f"{int(span // 3600)}h" if span >= 3600 else ''}{f"{int(span // 60 % 60)}min" if span >= 60 else ''}{int(span) % 60}s"

#强制退出
def force_stop():
    log("致命数据错误，程序将返回NLP主页。本次训练过程数据将不会被自动保存，请尽快保存内存中的数据，并查看运行日志获取运行情况")
    main_page_NLP()
    log("程序异常退出。请查看日志获取运行情况")
    exit(-1)

#SGNS负采样取噪声词
def get_neg_word():
    return random.choices(word_list, weights=weights, k=1)[0]

#词元频率
def p_t(i_token):
    return token[i_token]/sum(token.values())

#随机事件发生器
def rp_h(p):
    r=random.random()
    if r<p:
        return True
    else:
        return False

#下采样超参
T=10e-5
    #目前不对该超参提供应用内修改途径

#下采样
def subsampling(i_token):
    try:
        return 1-pow((T/p_t(i_token)),0.5)
    except:
        return 0

#负采样临时表
word_list=[]
weights=[]

#词库索引分表
word2idx={}

#SGNS准备
def pre_SGNS():
    global word_list,weights,word2idx
    word_list = list(token.keys())
    weights = [math.pow(freq, 0.75) for freq in token.values()]
    word2idx = {w: i for i, w in enumerate(token.keys())}

#SGNS训练（外层）
def SGNS(index_m,context,record_or_not):
    #如果窗口未构建好
    if index_m not in context:
        return 0

    #中心词下采样
    if rp_h(subsampling(context[index_m])):
        return 0

    #视窗内遍历
    for c_t in context.values():
        # 上下文词下采样
        if rp_h(subsampling(c_t)):
            continue
        SGNS2(context[index_m],c_t,get_neg_word(),record_or_not)

#通用sigmoid
def sigmoid(x):
    return 1/(1+math.exp(-x)) if x>=0 else math.exp(x)/(1+math.exp(x))

#统一计数器
count=0

#SGNS训练（内层）
def SGNS2(c,p,n,r):
    global embed, lr, word2idx,count

    #前期确认
    if c not in word2idx or p not in word2idx or n not in word2idx:
        return 0
    else:
        count+=1

    #获取词向量
    c_vec = embed[word2idx[c]]
    p_vec = embed[word2idx[p]]
    n_vec = embed[word2idx[n]]

    #逻辑回归损失
    p_cost = 1 - sigmoid(np.dot(c_vec, p_vec))
    n_cost = 0 - sigmoid(np.dot(c_vec, n_vec))

    #训练中报告
    if r:
        log(f" {count}.({c},{p},{n}),误差：({p_cost:.4f},{n_cost:.4f})")

    #梯度下降更新
    embed[word2idx[c]] += lr * (p_cost * p_vec + n_cost * n_vec)
    embed[word2idx[p]] += lr * p_cost * c_vec
    embed[word2idx[n]] += lr * n_cost * c_vec

#封装菜单
def menu2(menu_name,guidance="choice",back="返回",*entrance):
    choice=menu(menu_name,guidance,back,entrance)
    if choice==-1:
        log("入口不存在，请重新输入！")
        return menu2(menu_name, guidance, back, entrance)
    if choice==-2:
        log("输入不合法，请重新输入！")
        return menu2(menu_name, guidance, back, entrance)
    if choice==0:
        log("返回上一级：")
    return choice

#通用菜单
def menu(menu_name,guidance="choice",back="返回",*entrance):
    try:
        if len(entrance)==1:
            while isinstance(entrance[0],tuple):
                entrance=entrance[0]
    except:
        entrance=()
    log(f"{menu_name}:0.{back}",False)
    for i in range(len(entrance)):
        log(f" {i+1}.{entrance[i]}",False)
    log(f"\n>>{guidance}：", False)
    choice = input()
    try:
        choice=int(choice)
        if(choice>=0 and choice<=len(entrance)):
            return choice
        else:
            return -1
    except:
        return -2

#基本功能
def base_NLP():
    match menu2("基本功能(NLP版)", "skill", "返回主页","词库管理"):
        case 0:
            return -2
        case 1:
            global core_vocab
            if has_legacy_vocab_data():
                log("检测到旧版词表存有数据，正在自动迁移……")
                core_vocab.merge_legacy_vocab()
                log("全部数据已经迁移至主词表。正在清理旧版词表……")
                clear_legacy_vocab()
                log("清理完成。词库管理系统现在可以被正常使用！")
            while True:
                match menu2("词库管理", "skill", "返回主页","词库统计","词库显示","词库搜索","词库导出"):
                    case 0:
                        return -2
                    case 1:
                        core_vocab.stats()
                    case 2:
                        core_vocab.show_vocab()
                    case 3:
                        log("欢迎使用搜索————")
                        log("输入搜索词：", False)
                        for_searching=i_log(input())

                        log("确定模糊度：", False)
                        f=i_log(input())
                        try:
                            f=float(f)
                            if(f<0 or f>1):
                                log("输入不正确，将使用default值0.5")
                                f = 0.5
                        except:
                            log("输入不合法，将使用default值0.5")
                            f=0.5

                        core_vocab.search(for_searching,f).show_vocab(True)
                    case 4:
                        core_vocab.export(f"词表 {core_vocab.name} {get_time()}")
                    case 5:
                        pass
                    case 6:
                        pass
                log('')

#基本功能
def base_CV():
    match menu2("基本功能(CV版)", "skill", "返回主页"):
        case 0:
            return -2

#开始菜单
def homepage(reset=True):
    if reset:
        log_reset("AI-lab")
        log("【AI-lab】 开发者：spinner-bot 抖音@浪兮有点浪")
    while(True):
        match menu2("AI-lab homepage", "entrance", "退出", "NLP", "CV"):
            case 0:
                print("确认退出？[y]/n")
                if input(">>") == "y":
                    log(f"用户在{get_time()}主动退出: 退出代码 0", 0, True)
                    exit(0)
            case 1:
                mainpage_NLP()
            case 2:
                mainpage_CV()

#NLP主页
def mainpage_NLP():
    while (True):
        match menu2("NLP mainpage", "entrance", "返回主页", "基本功能", "词向量计算"):
            case 0:
                return -2
            case 1:
                base_NLP()
            case 2:
                log("说明：将使用旧版主页访问该模块。")
                main_page_NLP(True)

#CV主页
def mainpage_CV():
    while (True):
        match menu2("CV mainpage", "entrance", "返回主页", "基本功能"):
            case 0:
                return -2
            case 1:
                base_CV()

# 词表封装
class Vocab:
    def __init__(self, name, parent_vocab=None, keep_words: tuple = None):
        self.name = name

        # 有效分区
        self.word2idx = {}
        self.word2vec = {}
        self.word2count = {}

        # 无效分区
        self.u_word2idx = {}
        self.u_word2vec = {}
        self.u_word2count = {}

        # 分表逻辑
        if parent_vocab is not None and keep_words is not None:
            # 遍历保留词元组，只筛选需要的词
            for word in keep_words:
                # 仅当词存在于父词表时，才加入子词表
                if word in parent_vocab.word2idx:
                    self.word2idx[word] = parent_vocab.word2idx[word]
                    self.word2vec[word] = parent_vocab.word2vec[word]
                    self.word2count[word] = parent_vocab.word2count[word]

                if word in parent_vocab.u_word2idx:
                    self.u_word2idx[word] = parent_vocab.u_word2idx[word]
                    self.u_word2vec[word] = parent_vocab.u_word2vec[word]
                    self.u_word2count[word] = parent_vocab.u_word2count[word]

    # 1.添加词
    def add(self, word, idx, vec, count,available=True):
        if available:
            self.word2idx[word] = idx
            self.word2vec[word] = vec
            self.word2count[word] = count
        else:
            self.u_word2idx[word] = idx
            self.u_word2vec[word] = vec
            self.u_word2count[word] = count
        return idx

    # 2.注销词
    def unavailable(self, word):
        if word in self.word2idx:
            self.u_word2idx[word] = self.word2idx.pop(word)
            self.u_word2vec[word] = self.word2vec.pop(word)
            self.u_word2count[word] = self.word2count.pop(word)

    # 3.使生效
    def available(self, word):
        if word in self.u_word2idx:
            self.word2idx[word] = self.u_word2idx.pop(word)
            self.word2vec[word] = self.u_word2vec.pop(word)
            self.word2count[word] = self.u_word2count.pop(word)

    # 4.词索引
    def get_idx(self, word, available_only=True):
        if available_only:
            return self.word2idx.get(word, None)
        return self.word2idx.get(word, self.u_word2idx.get(word, None))

    # 5.词向量
    def get_vec(self, word, available_only=True):
        if available_only:
            return self.word2vec.get(word, None)
        return self.word2vec.get(word, self.u_word2vec.get(word, None))

    # 6.词频数
    def get_count(self, word, available_only=True):
        if available_only:
            return self.word2count.get(word, 0)
        return self.word2count.get(word, self.u_word2count.get(word, 0))

    # 7.词状态
    def get_state(self, word, available_only=True):
        if available_only:
            return word in self.word2idx
        return word in self.word2idx or word in self.u_word2idx

    # 8.随机取词
    def random_select(self,amount,unavailable_after_select=False):
        words = list(self.word2idx.keys())
        if not words:
            return []
        selected = random.sample(words, k=min(amount, len(words)))

        if unavailable_after_select:
            for w in selected:
                self.unavailable(w)
        return selected

    # 9.加权取词
    def weight_select(self,amount,weight=1,unavailable_after_select=False):
        words = list(self.word2idx.keys())
        if not words:
            return []

        weights = []
        if isinstance(weight, dict):
            weights = [weight.get(w, 1) for w in words]
        else:
            weights = [self.word2count[w] ** float(weight) for w in words]

        selected = random.choices(words, weights=weights, k=min(amount, len(words)))

        if unavailable_after_select:
            for w in selected:
                self.unavailable(w)
        return selected

    # 10.余弦相似度
    def similarity(self, word1, word2):
        # 获取两个词的向量
        vec1 = self.get_vec(word1, available_only)
        vec2 = self.get_vec(word2, available_only)

        # 异常处理
        if vec1 is None or vec2 is None:
            return 0.0

        if vec1.shape != vec2.shape:
            return 0.0

        # 计算
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        # 避免除零错误
        if norm1 == 0 or norm2 == 0:
            return 0.0

        #返回值
        return dot_product / (norm1 * norm2)

    # 11.维度清洗
    def dim_clean(self, dim=0):
        # 1. 收集全量词汇（有效 + 无效，全覆盖扫描）
        all_words = list(self.word2idx.keys()) + list(self.u_word2idx.keys())
        if not all_words:
            # 空表直接返回空临时表
            temp_vocab = Vocab(name=f"{self.name}_d_empty")
            return temp_vocab

        # 2. 统计所有词的向量维度 → dim=0时自动选众数
        dim_list = []
        for word in all_words:
            vec = self.get_vec(word, available_only=False)
            if vec is not None:
                dim_list.append(vec.shape[0])  # 取向量的维度值

        # 自动选择数量最多的维度
        if dim == 0 and dim_list:
            dim = Counter(dim_list).most_common(1)[0][0]
        elif dim == 0:
            dim = 0  # 无向量，默认0维

        # 3. 创建临时表（动态命名：原表名_d目标维度 → 递归兼容、无固定名）
        temp_vocab = Vocab(name=f"{self.name}_d{dim}exc")

        # 4. 分离词汇：目标维度留在原表，非目标移入临时表
        # 处理【有效词】分区
        for word in list(self.word2idx.keys()):
            vec = self.word2vec[word]
            if vec.shape[0] != dim:
                # 移入临时表（保持有效状态）
                temp_vocab.add(
                    word=word,
                    idx=self.word2idx[word],
                    vec=self.word2vec[word],
                    count=self.word2count[word],
                    available=True
                )
                # 从原表删除
                self.word2idx.pop(word)
                self.word2vec.pop(word)
                self.word2count.pop(word)

        # 处理【无效词】分区
        for word in list(self.u_word2idx.keys()):
            vec = self.u_word2vec[word]
            if vec.shape[0] != dim:
                # 移入临时表（保持无效状态）
                temp_vocab.add(
                    word=word,
                    idx=self.u_word2idx[word],
                    vec=self.u_word2vec[word],
                    count=self.u_word2count[word],
                    available=False
                )
                # 从原表删除
                self.u_word2idx.pop(word)
                self.u_word2vec.pop(word)
                self.u_word2count.pop(word)

        # 5. 打印日志（可选，方便调试）
        log(f"维度清洗完成 | 原表：{self.name} | 保留维度：{dim} | 分离词数：{len(temp_vocab.word2idx) + len(temp_vocab.u_word2idx)}")
        log(f"临时表名称：{temp_vocab.name}")

        # 6. 返回分离出的临时表实例
        return temp_vocab

    # 12.清空词表
    def clear(self):
        # 清空有效分区
        self.word2idx.clear()
        self.word2vec.clear()
        self.word2count.clear()
        # 清空无效分区
        self.u_word2idx.clear()
        self.u_word2vec.clear()
        self.u_word2count.clear()

    # 13.从文件导入
    def import_from_file(self, filename, replace=False,record=False):
        start_time = time.time()
        imported_count = 0
        invalid_count = 0

        # 替换模式：直接调用清空方法
        if replace:
            self.clear()

        current_idx = max(self.word2idx.values()) + 1 if self.word2idx else 0

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        invalid_count += 1
                        continue
                    parts = line.split()
                    if len(parts) < 2:
                        invalid_count += 1
                        continue

                    word = parts[0]
                    try:
                        vec = np.array(parts[1:], dtype=np.float32)
                    except ValueError:
                        invalid_count += 1
                        continue

                    self.add(word=word, idx=current_idx, vec=vec, count=1, available=True)
                    imported_count += 1
                    current_idx += 1

            cost_time = round(time.time() - start_time, 4)
            if record:
                log(f"词表文件导入完成 | 文件：{filename} | 模式：{'替换' if replace else '追加'}")
                log(f"用时：{cost_time}s | 成功导入：{imported_count} 词 | 无效行：{invalid_count}")
                log(f"词表【{self.name}】当前有效词：{len(self.word2idx)} 个")

        except FileNotFoundError:
            log(f"导入失败：文件【{filename}】不存在！", 2)
        except Exception as e:
            log(f"导入异常：{str(e)}", 2)

    # 14.从分表导入
    def import_from_subvocab(self, *subvocab):
        start_time = time.time()
        total_merge = 0
        valid_merge = 0
        invalid_merge = 0
        skip_invalid = 0

        for sub in subvocab:
            if not isinstance(sub, Vocab):
                skip_invalid += 1
                continue

            # 合并有效分区
            for word, idx in sub.word2idx.items():
                vec = sub.word2vec[word]
                count = sub.word2count[word]
                if word in self.word2idx:
                    self.word2count[word] += count
                else:
                    self.add(word, idx, vec, count, available=True)
                valid_merge += 1
                total_merge += 1

            # 合并无效分区
            for word, idx in sub.u_word2idx.items():
                vec = sub.u_word2vec[word]
                count = sub.u_word2count[word]
                if word in self.u_word2idx:
                    self.u_word2count[word] += count
                else:
                    self.add(word, idx, vec, count, available=False)
                invalid_merge += 1
                total_merge += 1

        cost_time = round(time.time() - start_time, 4)
        log(f"批量导入子词表完成 | 源表数量：{len(subvocab)} | 跳过非Vocab实例：{skip_invalid}")
        log(f"耗时：{cost_time}s | 合并总词数：{total_merge} | 有效词：{valid_merge} | 无效词：{invalid_merge}")
        log(f"词表【{self.name}】当前有效词：{len(self.word2idx)} 个 | 无效词：{len(self.u_word2idx)} 个")

    # 15.词表统计
    def stats(self):
        """输出词表完整统计信息"""
        # 词汇量：词的个数
        valid_vocab = len(self.word2idx)
        invalid_vocab = len(self.u_word2idx)
        total_vocab = valid_vocab + invalid_vocab

        # token数：词频累加
        valid_token = sum(self.word2count.values())
        invalid_token = sum(self.u_word2count.values())
        total_token = valid_token + invalid_token

        log(f"📊 词表【{self.name}】统计信息", 1)
        log(f"总词汇量：{total_vocab} | 总token数：{total_token}")
        log(f"有效词汇：{valid_vocab} | 有效token：{valid_token}")
        log(f"无效词汇：{invalid_vocab} | 无效token：{invalid_token}", 2)

    # 16.词表搜索
    def search(self, term, fuzziness=0.0,record=False):
        """
        搜索词表，返回结果子词表
        fuzziness=0：精确包含字符串匹配
        fuzziness>0：基于编辑距离的模糊匹配
        """
        result_vocab = Vocab(name=f"{self.name}_search_{term}_{fuzziness}")
        all_words = set(list(self.word2idx.keys()) + list(self.u_word2idx.keys()))

        for word in all_words:
            match = False
            if fuzziness == 0.0:
                match = term in word
            else:
                max_dist = max(1, int(len(word) * fuzziness))
                dist = levenshtein_distance(term, word)
                match = dist <= max_dist

            if match:
                # 复制状态与数据
                if word in self.word2idx:
                    result_vocab.add(
                        word, self.word2idx[word], self.word2vec[word],
                        self.word2count[word], available=True
                    )
                if word in self.u_word2idx:
                    result_vocab.add(
                        word, self.u_word2idx[word], self.u_word2vec[word],
                        self.u_word2count[word], available=False
                    )

        if record:
            log(f"搜索完成 | 词表：{self.name} | 关键词：{term} | 模糊度：{fuzziness}")
            log(f"命中词汇：{len(result_vocab.word2idx)+len(result_vocab.u_word2idx)} 个", 2)
        return result_vocab

    # 17.词表筛选
    def filter(self, freq=None, record=False):
        freq_dist = self.freq_distribution(available_only=True)
        if freq is None:
            freq = max(freq_dist.keys()) if freq_dist else 0

        filter_vocab = Vocab(name=f"{self.name}_filter_ge{freq}")

        # 筛选有效词
        for word, count in self.word2count.items():
            if count >= freq:
                filter_vocab.add(
                    word, self.word2idx[word], self.word2vec[word],
                    count, available=True
                )
        # 筛选无效词（保持无效）
        for word, count in self.u_word2count.items():
            if count >= freq:
                filter_vocab.add(
                    word, self.u_word2idx[word], self.u_word2vec[word],
                    count, available=False
                )

        if record:
            log(f"筛选完成 | 词表：{self.name} | 最小词频：{freq}")
            log(f"筛选后词汇：{len(filter_vocab.word2idx)+len(filter_vocab.u_word2idx)} 个", 2)
        return filter_vocab

    # 18.频数分布
    def freq_distribution(self, in_ratio=False, available_only=True):
        count_dict = {}
        total = 0

        # 统计有效分区
        for cnt in self.word2count.values():
            count_dict[cnt] = count_dict.get(cnt, 0) + 1
            total += 1

        # 统计无效分区
        if not available_only:
            for cnt in self.u_word2count.values():
                count_dict[cnt] = count_dict.get(cnt, 0) + 1
                total += 1

        # 转占比
        if in_ratio and total > 0:
            count_dict = {k: round(v/total, 4) for k, v in count_dict.items()}

        return dict(sorted(count_dict.items()))

    # 19.词频
    def freq(self, word, available_only=True):
        # 总频数
        total = sum(self.word2count.values())
        if not available_only:
            total += sum(self.u_word2count.values())
        # 当前词频数
        cnt = self.get_count(word, available_only)
        return cnt / total if total > 0 else 0.0

    # 20.无效清理
    def clear_u(self, record=False):
        self.u_word2idx.clear()
        self.u_word2vec.clear()
        self.u_word2count.clear()
        if record:
            log(f"无效分区已清空 | 词表：{self.name}")

    # 21.词表导出
    def export(self, path, file_type="txt", record=False, with_u=False, mark_u=True):
        try:
            # 只支持通用 txt（NLP 行业标准）
            if file_type.lower() != "txt":
                log(f"仅支持 txt 导出，已自动修正", 2)
                file_type = "txt"

            file_path = f"{path}.{file_type}"
            with open(file_path, "w", encoding="utf-8") as f:
                # 导出有效词
                for w in self.word2idx:
                    idx = self.word2idx[w]
                    vec = " ".join(map(str, self.word2vec[w].tolist()))
                    cnt = self.word2count[w]
                    f.write(f"{w} {idx} {vec} {cnt}\n")

                if with_u:
                    f.write("\n")

                    # 导出无效词（标记 unavailable）
                    for w in self.u_word2idx:
                        idx = self.u_word2idx[w]
                        vec = " ".join(map(str, self.u_word2vec[w].tolist()))
                        cnt = self.u_word2count[w]
                        if mark_u:
                            f.write(f"{w} {idx} {vec} {cnt} unavailable\n")
                        else:
                            f.write(f"{w} {idx} {vec} {cnt}\n")

            if record:
                log(f"词表导出成功 | 路径：{file_path}")
        except Exception as e:
            if record:
                log(f"导出失败：{str(e)}", 2)

    # 22.合并旧版词表
    def merge_legacy_vocab(self):
        self.import_from_subvocab(migrate_legacy_vocab())

    # 23.显示词表
    def show_vocab(self, available_only=False):
        """
        日志可视化展示词表内容
        :param available_only: True=仅展示有效词 False=展示全部词(有效+无效)
        """
        # 标题分隔线
        log("=" * 100)
        log(f"📖 词表展示 | 名称：{self.name} | 模式：{'仅有效词' if available_only else '全部词'}")
        log("=" * 100)

        # 1. 展示有效词汇
        valid_words = list(self.word2idx.items())
        total_valid_token = sum(self.word2count.values())
        # 按【词频降序 + 字典序升序】排序
        valid_words_sorted = sorted(
            valid_words,
            key=lambda x: (-self.word2count[x[0]], x[0])
        )

        log(f"\n✅ 有效词汇（共 {len(valid_words)} 个）：")
        log("-" * 90)
        if valid_words_sorted:
            for idx, (word, word_idx) in enumerate(valid_words_sorted, 1):
                count = self.word2count[word]
                # 计算频率（百分比）
                freq = (count / total_valid_token * 100) if total_valid_token != 0 else 0.0
                vec = self.word2vec[word]
                vec_dim = vec.shape[0] if vec is not None else 0
                log(f"[{idx:2d}] 索引：{word_idx:4d} | 单词：{word:<15} | 频数：{count:4d} | 频率：{freq:6.2f}% | 向量维度：{vec_dim}d")
        else:
            log("    暂无有效词汇")

        # 2. 展示无效词汇
        if not available_only:
            invalid_words = list(self.u_word2idx.items())
            total_invalid_token = sum(self.u_word2count.values())
            invalid_words_sorted = sorted(
                invalid_words,
                key=lambda x: (-self.u_word2count[x[0]], x[0])
            )

            log(f"\n❌ 无效词汇（共 {len(invalid_words)} 个）：")
            log("-" * 90)
            if invalid_words_sorted:
                for idx, (word, word_idx) in enumerate(invalid_words_sorted, 1):
                    count = self.u_word2count[word]
                    # 计算频率（百分比）
                    freq = (count / total_invalid_token * 100) if total_invalid_token != 0 else 0.0
                    vec = self.u_word2vec[word]
                    vec_dim = vec.shape[0] if vec is not None else 0
                    log(f"[{idx:2d}] 索引：{word_idx:4d} | 单词：{word:<15} | 频数：{count:4d} | 频率：{freq:6.2f}% | 向量维度：{vec_dim}d")
            else:
                log("    暂无无效词汇")

        # 3. 底部统计总结
        log("-" * 100)
        self.stats()
        log("=" * 100 + "\n")

# 旧版词表整理
def migrate_legacy_vocab():
    """
    【无参数一键迁移】
    自动读取全局旧数据：token(有效词)、token_bin(无效词)、embed(词向量)、word2idx(索引)
    整理为标准 Vocab 实例并返回
    """
    # 读取
    legacy_token = token
    legacy_token_bin = token_bin
    legacy_embed = embed
    legacy_word2idx = word2idx

    # 初始化目标词表
    vocab = Vocab(name="final_migrated_vocab")

    # 空数据判断
    if not legacy_token and not legacy_token_bin:
        log(f"旧词表为空，迁移完成", 2)
        return vocab

    # 自动匹配向量维度
    vec_dim = 100
    if isinstance(legacy_embed, np.ndarray) and legacy_embed.ndim == 2:
        vec_dim = legacy_embed.shape[1]

    # 初始化索引
    current_idx = 0

    # 统计变量
    start_time = time.time()
    valid_migrate = 0
    valid_vec_migrate = 0
    invalid_migrate = 0

    # 迁移 有效词 + 训练好的词向量
    for word, count in legacy_token.items():
        word = word.strip().lower()
        if not word:
            continue

        # 读取旧向量
        vec = np.zeros(vec_dim, dtype=np.float32)
        if word in legacy_word2idx:
            old_idx = legacy_word2idx[word]
            if 0 <= old_idx < len(legacy_embed):
                vec = legacy_embed[old_idx].astype(np.float32)
                valid_vec_migrate += 1

        # 添加到词表
        vocab.add(word, current_idx, vec, count, available=True)
        current_idx += 1
        valid_migrate += 1

    # 迁移 无效词（零向量）
    for word, count in legacy_token_bin.items():
        word = word.strip().lower()
        if not word:
            continue

        vec = np.zeros(vec_dim, dtype=np.float32)
        vocab.add(word, current_idx, vec, count, available=False)
        current_idx += 1
        invalid_migrate += 1

    # 日志输出
    cost_time = round(time.time() - start_time, 4)
    log(f"旧词表一键迁移完成！", 1)
    log(f"耗时：{cost_time}s")
    log(f"有效词：{valid_migrate} 个（含训练向量：{valid_vec_migrate} 个）")
    log(f"无效词：{invalid_migrate} 个")
    vocab.stats()

    # 返回整理完成的词表实例
    return vocab

# 旧版词表清空
def clear_legacy_vocab():
    """
    【无参数一键清空】
    清空所有旧版词表数据：token、token_bin、embed、word2idx
    """
    global token, token_bin, embed, word2idx

    # 清空所有旧数据
    token.clear()
    token_bin.clear()
    embed = np.array([])
    word2idx = {}

    log("✅ 旧版词表所有数据已完全清空", 2)

# 旧版词表检测
def has_legacy_vocab_data():
    """
    【无参数检测】
    检查是否存在旧版词表数据（任意一个不为空就返回 True）
    :return: True = 有旧数据 | False = 无旧数据
    """
    global token, token_bin, embed, word2idx

    # 只要任意一个有数据，就返回 True
    has_data = (
            len(token) > 0
            or len(token_bin) > 0
            or (isinstance(embed, np.ndarray) and embed.size > 0)
            or len(word2idx) > 0
    )
    return has_data

# 莱文斯坦距离
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

# 主词表
core_vocab = Vocab("core_vocab")

#流程控制
if not is_debugging:
    homepage()