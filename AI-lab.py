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
        log("NLP main page（旧版）:0.退出 1.基本功能 2.词向量计算 3.进入新版主页")
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
    match menu2("基本功能(NLP版)", "skill", "返回主页","词库管理","文库管理"):
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
                match menu2("词库管理", "skill", "返回主页","词库统计","查看词库","模糊搜索","文件导出","文件导入","一键清洗","分表管理"):
                    case 0:
                        return -2
                    # 词库统计
                    case 1:
                        core_vocab.stats()
                    # 词库显示
                    case 2:
                        core_vocab.show_vocab()
                    # 词库搜索
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

                        core_vocab.search(for_searching,f).show_vocab()
                    # 词库导出
                    case 4:
                        core_vocab.export(f"词表 {core_vocab.name} {get_time()}")
                    # 词库导入
                    case 5:
                        a=1
                        path=''
                        while a==1:
                            a-=1
                            match menu2("词库资源", "select", "返回", "Stanford2024","自定义文件"):
                                case 0:
                                    continue
                                case 1:
                                    path=os.path.join("资源","dolma_300_2024_1.2M.100_combined")
                                    log("这可能需要几分钟，请等待……")
                                case 2:
                                    log("输入文件路径：", False)
                                    path=i_log(input())
                            core_vocab.import_from_file(path+".txt",False,True)
                            match menu2("清除词频？","choice","否","是"):
                                case 0:
                                    pass
                                case 1:
                                    core_vocab.clear_freq()
                    case 6:
                        core_vocab.dim_clean()
                    case 7:
                        sub_table_manager()
                log('')
        case 2:
            library_manager()

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
        match menu2("AI-lab homepage", "entrance", "退出", "NLP", "CV","RS"):
            case 0:
                print("确认退出？[y]/n")
                if input(">>") == "y":
                    log(f"用户在{get_time()}主动退出: 退出代码 0", 0, True)
                    exit(0)
            case 1:
                mainpage_NLP()
            case 2:
                mainpage_CV()
            case 3:
                mainpage_RS()

#NLP主页
def mainpage_NLP():
    while (True):
        match menu2("NLP mainpage", "entrance", "返回主页", "基本功能", "词向量计算", "推理模式"):
            case 0:
                return -2
            case 1:
                base_NLP()
            case 2:
                log("说明：将使用旧版主页访问该模块。")
                main_page_NLP(True)
            case 3:
                run_reasoning_mode(core_vocab)

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
    #注册表
    _TABLE_REGISTRY = {}
    _MAIN_TABLE = "core_vocab"

    #创建表
    def __init__(self, name, parent_vocab=None, keep_words: tuple = None):
        self.name = name

        #分表注册
        if not name == "core_vocab":
            self._register_self()

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

    # 0.自动注册
    def _register_self(self):
        Vocab._TABLE_REGISTRY[self.name] = self

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
    def similarity(self, word1, word2, target_vec=None):
        vec1 = self.get_vec(word1)
        vec2 = target_vec if target_vec is not None else self.get_vec(word2)

        if vec1 is None or vec2 is None:
            return 0.0
        if vec1.shape != vec2.shape:
            return 0.0

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0
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
        freq_dist = self.freq_distribution(available_only)
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

    # 24.清除词频信息
    def clear_freq(self):
            # 重置有效词频数
        for word in self.word2count:
            self.word2count[word] = 1

            # 重置无效词频数
        for word in self.u_word2count:
            self.u_word2count[word] = 1

# 主词表
core_vocab = Vocab("core_vocab")

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

# 推理模式
def run_reasoning_mode(main_vocab):
    """
    独立全局推理模式
    :param main_vocab: 主词表 Vocab 实例（如 core_vocab）
    :return: 推理专用分表
    """
    # 创建推理专用分表
    reasoning_vocab = Vocab(name=f"{main_vocab.name}_reasoning")
    log(f"🧠 推理模式启动 | 已创建推理分表：{reasoning_vocab.name}", 2)

    # 内部核心函数：引导输入加权词汇组合（已修复None报错）
    def _input_weighted_combo():
        log("\n✍️  请逐行输入【词 权重】（空格分隔），完成输入 END 结束：")
        log("示例：king 1.0  |  man -1.0  |  woman 1.0")
        combo_parts = []
        combo_vec = None

        while True:
            line = i_log(input(), newline=1, prefix=False).strip()
            if line.upper() == "END":
                break
            if not line:
                continue

            parts = line.split()
            if len(parts) != 2:
                log("⚠️  格式错误，请输入：词 权重（空格分隔）")
                continue

            word, w_str = parts
            try:
                weight = float(w_str)
            except ValueError:
                log("⚠️  权重必须为数字")
                continue

            if word not in main_vocab.word2idx:
                log(f"⚠️  主词表中无词汇：{word}，已跳过")
                continue

            vec = main_vocab.get_vec(word)
            if vec is None:
                continue

            # 自动初始化向量（彻底修复None报错）
            if combo_vec is None:
                combo_vec = np.zeros_like(vec, dtype=np.float32)

            combo_vec += weight * vec
            sign = "+" if weight >= 0 else ""
            combo_parts.append(f"{sign}{weight}*{word}")

        if not combo_parts or combo_vec is None:
            log("⚠️  未输入有效词汇组合，返回")
            return None, "", ""

        # 表达式过长自动省略
        expr = "".join(combo_parts)
        display_expr = expr if len(expr) <= 40 else f"...{expr[-40:]}"
        log(f"\n✅ 组合表达式：{display_expr}")

        mix_name = f"mix_{len(reasoning_vocab.word2idx)}"
        return combo_vec, expr, mix_name

    # 推理模式主菜单
    while True:
        log("\n==================== 推理模式菜单 ====================")
        log("1.逻辑匹配（组合向量→查找主表相似独立词）")
        log("2.逻辑分析（输入两组组合→计算相似度）")
        log("0.退出推理模式")
        log("========================================================")
        log(">> 请选择功能：", newline=False)
        choice = i_log(input(), newline=1, prefix=False).strip()

        # 退出
        if choice == "0":
            log(f"\n👋 推理模式已退出 | 推理分表保留：{reasoning_vocab.name}", 2)
            return reasoning_vocab

        # 逻辑匹配
        elif choice == "1":
            combo_res = _input_weighted_combo()
            if combo_res[0] is None:
                continue
            combo_vec, expr, mix_name = combo_res

            # 存入推理分表
            max_idx = max(reasoning_vocab.word2idx.values()) + 1 if reasoning_vocab.word2idx else 0
            reasoning_vocab.add(word=mix_name, idx=max_idx, vec=combo_vec, count=1, available=True)
            log(f"✅ 组合向量已存入推理分表：{mix_name}")

            # 相似度阈值
            log(">> 请输入相似度阈值（0~1，默认0.5）：", newline=False)
            threshold_str = i_log(input(), newline=1, prefix=False).strip()
            threshold = float(threshold_str) if threshold_str else 0.5
            threshold = max(0.0, min(1.0, threshold))

            # 匹配主表词汇
            match_results = []
            for word in main_vocab.word2idx:
                sim = main_vocab.similarity(word, mix_name, target_vec=combo_vec)
                if sim >= threshold:
                    match_results.append((word, sim))

            # 排序输出
            match_results.sort(key=lambda x: -x[1])
            log(f"\n🔍 逻辑匹配结果（阈值≥{threshold}）：")
            log("-" * 60)
            if match_results:
                for i, (word, sim) in enumerate(match_results, 1):
                    log(f"[{i:2d}] {word:<15} 相似度：{sim:.4f}")
            else:
                log("    未找到符合阈值的词汇")
            log("-" * 60)

        # 逻辑分析（手动输入两组组合，无需分表）
        elif choice == "2":
            log("\n📝 请输入【第一组逻辑组合】")
            vec1, expr1, _ = _input_weighted_combo()
            if vec1 is None:
                continue

            log("\n📝 请输入【第二组逻辑组合】")
            vec2, expr2, _ = _input_weighted_combo()
            if vec2 is None:
                continue

            # 计算相似度
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            sim = dot_product / (norm1 * norm2) if (norm1 != 0 and norm2 != 0) else 0.0

            # 输出结果
            log("\n" + "=" * 70)
            log(f"组合1：{expr1 if len(expr1) <= 60 else f'...{expr1[-60:]}'}")
            log(f"组合2：{expr2 if len(expr2) <= 60 else f'...{expr2[-60:]}'}")
            log(f"🎯 两组组合逻辑相似度 = {sim:.4f}")
            log("=" * 70)

        else:
            log("⚠️  无效选项，请重新输入")

# RS主页
def mainpage_RS():
    while (True):
        match menu2("RS mainpage", "entrance", "返回主页" ):
            case 0:
                return -2

# 分表管理
def sub_table_manager():
    global core_vocab
    # 主表降级后缀（可自行修改）
    OLD_MAIN_SUFFIX = "_main_old"

    while True:
        log("\n" + "=" * 85)
        log("📋 分表管理中心 | Vocab Table Manager")
        log("=" * 85)
        # 优化排版：名称列加宽
        log(f"{'索引':<4} | {'表名称':<40} | {'类型':<6} | {'有效词汇数':<8} | {'向量维度':<8} | {'状态'}")
        log("-" * 85)

        table_index_map = []
        registry = Vocab._TABLE_REGISTRY

        # 显示当前主表（安全获取向量维度，空表不报错）
        main_ins = core_vocab
        w_num = len(main_ins.word2idx)
        vec_dim = "未知"
        if main_ins.word2vec:  # 关键修复：判断字典非空再取值
            vec_dim = next(iter(main_ins.word2vec.values())).shape[0]
        log(f"[1  ] | {main_ins.name:<40} | 主表    | {w_num:<8} | {vec_dim:<8} | ✅ 系统主表")
        table_index_map.append(("main", main_ins, True))

        # 关键修复：单条固定分隔线，不重复
        log("-" * 85)

        # 显示分表
        has_sub = False
        display_idx = 2
        for name, ins in registry.items():
            has_sub = True
            w_num = len(ins.word2idx)
            # 安全获取向量维度
            vec_dim_sub = "未知"
            if ins.word2vec:
                vec_dim_sub = next(iter(ins.word2vec.values())).shape[0]
            log(f"[{display_idx:<2}] | {name:<40} | 分表    | {w_num:<8} | {vec_dim_sub:<8} | ⭕ 可操作")
            table_index_map.append((name, ins, False))
            display_idx += 1

        if not has_sub:
            log(" " * 40 + "📭 暂无分表")
        log("=" * 85)

        # 操作菜单
        log("\n【操作说明】")
        log("  0 → 退出管理")
        log("  1 → 操作主表")
        log(" ≥2 → 操作对应分表")
        choice = input("\n请输入操作索引：").strip()

        # 退出
        if choice == "0":
            log("\n👋 退出分表管理")
            return

        # 索引校验
        if not choice.isdigit():
            log("❌ 输入无效！请输入数字！")
            continue
        target_idx = int(choice) - 1
        if target_idx < 0 or target_idx >= len(table_index_map):
            log("❌ 输入无效！索引超出范围！")
            continue

        # 获取选中表
        _, ins, is_main = table_index_map[target_idx]
        log(f"\n🎯 选中：{ins.name}（{'主表' if is_main else '分表'}）")

        # =====================
        # 主表操作（重命名 + 清空）
        # =====================
        if is_main:
            op = menu2("主表操作", "choice", "返回", "重命名", "清空词表数据")
            if op == 0:
                continue
            # 重命名
            elif op == 1:
                new_name = input("请输入新名称：").strip()
                if not new_name:
                    log("❌ 名称不能为空！")
                    continue
                ins.name = new_name
                log(f"✅ 主表已重命名为：{new_name}")
            # 清空数据
            elif op == 2:
                if input("⚠️ 确认清空主表所有数据？(y/n)：").lower() == "y":
                    ins.clear()
                    log("✅ 主表数据已清空！")

        # =====================
        # 分表操作
        # =====================
        else:
            op = menu2("分表操作", "choice", "返回", "升级为主表", "重命名", "删除分表")
            if op == 0:
                continue
            # 🔥 升级为主表：不改名！保留原名称
            elif op == 1:
                # 自动去除降级后缀
                final_name = ins.name.replace(OLD_MAIN_SUFFIX, "")
                ins.name = final_name

                # 旧主表降级为分表（加后缀）
                old_main = core_vocab
                old_main.name = f"{old_main.name}{OLD_MAIN_SUFFIX}"
                # 注册旧主表到分表
                Vocab._TABLE_REGISTRY[old_main.name] = old_main

                # ✅ 新主表直接替换，绝不修改名称
                core_vocab = ins

                # 从分表列表中移除当前表
                if ins.name in Vocab._TABLE_REGISTRY:
                    del Vocab._TABLE_REGISTRY[ins.name]

                log(f"✅ 【{ins.name}】已升级为主表！原主表已降级为分表")

            # 分表重命名（禁止使用 core_vocab）
            elif op == 2:
                new_name = input("请输入新名称：").strip()
                if not new_name:
                    log("❌ 名称不能为空！")
                    continue
                if new_name == "core_vocab":
                    log("❌ 禁止使用名称 core_vocab！")
                    continue
                del registry[ins.name]
                ins.name = new_name
                registry[new_name] = ins
                log(f"✅ 分表已重命名为：{new_name}")

                # 删除分表
            elif op == 3:
                if input(f"⚠️ 确认删除分表 {ins.name}？(y/n)：").lower() == "y":
                    del registry[ins.name]
                    log(f"🗑️ 已删除分表：{ins.name}")

# 文库管理
def library_manager():
    global read_list
    # ===================== 核心配置 =====================
    PREVIEW_LINE_LIMIT = 20
    PREVIEW_WORD_LIMIT = 500
    PREVIEW_CHAR_LIMIT = 1800
    SEP = "\\"
    nav_stack = [""]
    INVALID_CHARS = r'[<>:"|?*]'
    BASE_DIR = "训练文本"
    SNIPPET_AROUND = 80
    MAX_EXPAND_CHAR = 10
    # 全局显示宽度（仅设置1次）
    GLOBAL_WIDTH = 0

    # ===================== 全局统一设置行宽（仅进入系统时调用1次） =====================
    def set_global_width():
        nonlocal GLOBAL_WIDTH
        while True:
            inp = input("请设置全局显示宽度（0=不换行，a/auto=自动，数字=固定）：").strip().lower()
            if inp == "0":
                GLOBAL_WIDTH = 0
                log("✅ 全局宽度：不自动换行")
                break
            elif inp in ("a", "auto"):
                try:
                    GLOBAL_WIDTH = os.get_terminal_size().columns - 4
                    log(f"✅ 全局宽度：自动获取({GLOBAL_WIDTH}列)")
                except:
                    log("❌ 自动获取不可用，已设置为不换行")
                    GLOBAL_WIDTH = 0
                break
            elif inp.isdigit() and int(inp) >= 10:
                GLOBAL_WIDTH = int(inp)
                log(f"✅ 全局宽度：{GLOBAL_WIDTH}列")
                break
            else:
                log("❌ 输入无效，请重新输入")

    # ===================== 智能扩展上下文到完整单词 =====================
    def expand_to_full_word(text, pos, left=True):
        current = pos
        expanded = 0
        boundaries = ' \n\t\r.,;!?()[]{}<>"\'/:\\-=+'
        while expanded < MAX_EXPAND_CHAR:
            if current < 0 or current >= len(text):
                break
            if text[current] in boundaries:
                break
            current += -1 if left else 1
            expanded += 1
        return current + 1 if left else current - 1

    # ===================== 文件大小自动格式化（全单位） =====================
    def format_file_size(size_bytes):
        if size_bytes <= 0:
            return "0.0 B"
        units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
        size = size_bytes
        unit_idx = 0
        while size >= 1024 and unit_idx < len(units) - 1:
            size /= 1024
            unit_idx += 1
        return f"{size:.1f} {units[unit_idx]}"

    # ===================== 智能换行：不截断词+超长词加连字符 =====================
    def split_long_word(word, width):
        parts = []
        max_part = width - 1
        i = 0
        while i < len(word):
            if i + max_part < len(word):
                part = word[i:i+max_part] + "-"
                parts.append(part)
                i += max_part
            else:
                parts.append(word[i:])
                break
        return parts

    def wrap_for_preview(text, width):
        if width <= 0:
            return text
        raw_lines = text.splitlines()
        final_lines = []
        for line in raw_lines:
            if not line.strip():
                final_lines.append("")
                continue
            words = line.split()
            current_line = ""
            for word in words:
                word_len = len(word)
                if word_len > width:
                    if current_line:
                        final_lines.append(current_line.rstrip())
                        current_line = ""
                    word_parts = split_long_word(word, width)
                    final_lines.extend(word_parts)
                    continue
                test_line = current_line + word + " "
                if len(test_line.rstrip()) <= width:
                    current_line = test_line
                else:
                    final_lines.append(current_line.rstrip())
                    current_line = word + " "
            if current_line:
                final_lines.append(current_line.rstrip())
        return "\n".join(final_lines)

    # ===================== 自动校验&清理 =====================
    def auto_validate_and_clean():
        original = len(read_list)
        unique = list(dict.fromkeys(read_list))
        valid = [f for f in unique if os.path.isfile(os.path.join(BASE_DIR, f))]
        read_list[:] = valid
        removed = original - len(valid)
        if removed > 0:
            log(f"⚠️ 自动校验：删除{removed}个无效/重复文件")
        else:
            log("✅ 自动校验：全部有效")

    # ===================== 系统级1：扫描根目录所有txt =====================
    def scan_available_files():
        if not os.path.isdir(BASE_DIR):
            log(f"❌ 根目录「{BASE_DIR}」不存在，无法扫描")
            return
        scanned_files = []
        for root, _, files in os.walk(BASE_DIR):
            for file in files:
                if file.lower().endswith(".txt"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, BASE_DIR).replace("/", SEP)
                    scanned_files.append(rel_path)
        scanned_files = list(dict.fromkeys(scanned_files))
        new_add = 0
        for f in scanned_files:
            if f not in read_list:
                read_list.append(f)
                new_add += 1
        log(f"🔍 扫描完成：共找到{len(scanned_files)}个txt文件，新增导入{new_add}个")

    # ===================== 系统级2：切换根目录 =====================
    def change_root_dir():
        nonlocal BASE_DIR
        new_root = input("请输入新的根目录路径：").strip()
        if not new_root:
            log("❌ 路径不能为空")
            return
        if not os.path.isdir(new_root):
            log(f"❌ 目录「{new_root}」不存在")
            return
        BASE_DIR = new_root
        log(f"✅ 根目录已切换为：{BASE_DIR}")
        auto_validate_and_clean()

    # ===================== 路径规范化 =====================
    def normalize_path(user_input):
        p = re.sub(INVALID_CHARS, "", user_input)
        p = p.replace("/", SEP).replace("\\\\", SEP)
        return p[:-4] if p.lower().endswith(".txt") else p.strip()

    # ===================== 构建目录列表 =====================
    def build_current_dir():
        cur = nav_stack[-1]
        folders, files = set(), []
        for fp in read_list:
            pure = fp[:-4]
            if cur and not pure.startswith(cur + SEP):
                continue
            rel = pure[len(cur):].strip(SEP)
            if SEP in rel:
                folders.add(rel.split(SEP)[0])
            else:
                files.append(rel)
        return sorted(folders), sorted(files)

    # ===================== 文件统计 =====================
    def get_file_stats(fn):
        path = os.path.join(BASE_DIR, fn)
        if not os.path.isfile(path):
            return "异常", "异常", "异常", "0.0 B", 0
        raw_size = os.path.getsize(path)
        size_str = format_file_size(raw_size)
        try:
            with open(path, "r", encoding="utf-8") as f:
                c = f.read()
            lines = c.splitlines()
            chars = len(c.replace("\n","").replace(" ",""))
            words = len([w for w in t_clean(c,7) if w.strip()]) if "t_clean" in globals() else len(c.split())
            return f"{len(lines)}行", f"{chars}字", f"{words}词", size_str, chars
        except:
            return "失败", "失败", "失败", "0.0 B", 0

    # ===================== 文件预览（使用全局宽度） =====================
    def file_preview(fn):
        path = os.path.join(BASE_DIR, fn)
        if not os.path.isfile(path):
            log("❌ 文件不存在")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            lines = content.splitlines()
            total_chars = len(content.replace("\n","").replace(" ",""))
            need_ask_fold = len(lines) > PREVIEW_LINE_LIMIT or total_chars > PREVIEW_CHAR_LIMIT

            log("\n" + "="*60)
            log(f"📄 预览：{fn}")
            log("-"*60)

            fold = False
            if need_ask_fold:
                c = input("内容较长，是否折叠预览？(y/n)：").strip().lower()
                fold = c == "y"

            if not fold:
                disp = wrap_for_preview(content, GLOBAL_WIDTH)
                log(disp)
            else:
                head = wrap_for_preview("\n".join(lines[:10]), GLOBAL_WIDTH)
                tail = wrap_for_preview("\n".join(lines[-10:]), GLOBAL_WIDTH)
                omit_l = len(lines) - 20
                omit_c = total_chars - (len(head.replace("\n","")) + len(tail.replace("\n","")))
                log(head)
                log(f"\n... 省略 {omit_l} 行 ({omit_c} 字) ...\n")
                log(tail)
            log("="*60)
        except Exception as e:
            log(f"❌ 预览失败：{str(e)}")

    # ===================== 全文搜索（连续查看+详情保留换行+全局宽度） =====================
    def file_search(fn):
        path = os.path.join(BASE_DIR, fn)
        if not os.path.isfile(path):
            log("❌ 文件不存在")
            return
        raw_key = input("请输入搜索内容：").strip()
        if not raw_key:
            log("❌ 搜索词不能为空")
            return
        key_len = len(raw_key)

        try:
            with open(path, "r", encoding="utf-8") as f:
                full_text = f.read()
        except:
            log("❌ 读取文件失败")
            return

        positions = []
        start = 0
        while True:
            idx = full_text.find(raw_key, start)
            if idx == -1:
                break
            positions.append(idx)
            start = idx + key_len

        if not positions:
            log(f"\n🔍 未找到内容：{raw_key}")
            return

        # 连续查看搜索结果
        while True:
            log(f"\n🔍 共找到 {len(positions)} 处匹配：")
            log("-"*70)
            res_map = {}
            for i, pos in enumerate(positions, 1):
                pre_start = max(0, pos - SNIPPET_AROUND)
                post_end = min(len(full_text), pos + key_len + SNIPPET_AROUND)
                pre_start = expand_to_full_word(full_text, pre_start, left=True)
                post_end = expand_to_full_word(full_text, post_end, left=False)

                # 搜索列表：换行转2空格
                pre = full_text[pre_start:pos].replace("\n", "  ")
                match = full_text[pos:pos+key_len].replace("\n", "  ")
                post = full_text[pos+key_len:post_end].replace("\n", "  ")

                snippet = f"...{pre}【{match}】{post}..."
                log(f"[{i:2d}] {snippet}")
                res_map[i] = pos
            log("-"*70)

            sel = input("选择结果序号查看详情（0=返回搜索）：").strip()
            if sel == "0":
                log("✅ 返回搜索界面")
                break
            if not sel.isdigit() or int(sel) not in res_map:
                log("❌ 无效序号")
                continue

            ctx = input("设置上下文范围（前后字符数，如100）：").strip()
            if not ctx.isdigit():
                log("❌ 请输入数字")
                continue
            ctx_n = int(ctx)
            pos = res_map[int(sel)]

            # 详情页：保留原始换行 + 全局宽度智能换行
            s = max(0, pos - ctx_n)
            e = min(len(full_text), pos + key_len + ctx_n)
            part_pre = full_text[s:pos]
            part_match = f"【{full_text[pos:pos+key_len]}】"
            part_post = full_text[pos+key_len:e]
            detail_raw = f"...{part_pre}{part_match}{part_post}..."
            detail_formatted = wrap_for_preview(detail_raw, GLOBAL_WIDTH)

            log(f"\n📌 搜索结果详情（上下文{ctx_n}字符）：")
            log("-"*70)
            log(detail_formatted)
            log("-"*70)

    # ===================== 初始化：仅1次设置宽度 + 自动扫描 =====================
    set_global_width()  # 进入系统只问这一次！
    auto_validate_and_clean()
    log("🔄 系统启动：自动扫描根目录文件...")
    scan_available_files()

    # ===================== 主循环 =====================
    while True:
        cur_path = nav_stack[-1]
        folders, files = build_current_dir()
        item_map, idx = {}, 1

        log("\n" + "="*90)
        log(f"📚 文库管理中心 | 当前根目录：{BASE_DIR}")
        log(f"📁 当前目录：{cur_path if cur_path else '根目录'} | 文件夹：{len(folders)} | 文件：{len(files)}")
        log("="*90)

        for fld in folders:
            item_map[idx] = ("folder", fld)
            log(f"[{idx:2d}] 📁 {fld}")
            idx +=1
        for fil in files:
            full_f = f"{cur_path}{SEP}{fil}.txt" if cur_path else f"{fil}.txt"
            item_map[idx] = ("file", full_f)
            log(f"[{idx:2d}] 📄 {fil}")
            idx +=1

        # 操作栏（字母指令）
        log("-"*90)
        log("[0] 返回/退出" if cur_path else "[0] 退出系统")
        log("[+]添加 | [b]批量 | [d]删除 | [c]清空 | [s]扫描文件 | [r]切换根目录")
        log("="*90)

        choice = input("请输入指令：").strip().lower()

        if choice == "0":
            if not cur_path:
                log("👋 退出文库管理")
                return
            nav_stack.pop()
            continue

        if choice.isdigit() and int(choice) in item_map:
            typ, name = item_map[int(choice)]
            if typ == "folder":
                nav_stack.append(cur_path + SEP + name if cur_path else name)
                continue
            # 文件操作
            if typ == "file":
                while True:
                    log("\n" + "="*60)
                    log(f"📄 {name}")
                    lines, chars, words, size, _ = get_file_stats(name)
                    log(f"{size} | {lines} | {chars} | {words}")
                    log("-"*60)
                    log("[0] 返回 | [1] 预览 | [2] 删除 | [3] 搜索")
                    fc = input("选择操作：").strip()
                    if fc == "0":
                        break
                    elif fc == "1":
                        file_preview(name)
                    elif fc == "2":
                        if input(f"⚠️ 确认删除 {name}？(y/n)：").strip().lower() == "y":
                            if name in read_list:
                                read_list.remove(name)
                                log("✅ 已删除")
                                break
                        else:
                            log("✅ 已取消")
                    elif fc == "3":
                        file_search(name)
                    else:
                        log("❌ 无效指令")
                continue

        if choice == "+":
            raw = input("文件路径（无需.txt）：").strip()
            if not raw:
                log("❌ 不能为空")
                continue
            norm = normalize_path(raw)
            target = f"{norm}.txt"
            if not os.path.isfile(os.path.join(BASE_DIR, target)):
                log(f"❌ 文件不存在：{target}")
                continue
            if target in read_list:
                log("❌ 已存在")
                continue
            read_list.append(target)
            log(f"✅ 已添加：{target}")
            continue

        if choice == "b":
            log("\n📦 批量导入")
            quick_import()
            auto_validate_and_clean()
            continue

        if choice == "d":
            di = input("输入删除序号：").strip()
            if di.isdigit() and int(di) in item_map:
                t_typ, t_name = item_map[int(di)]
                if t_typ == "file":
                    if input(f"⚠️ 确认删除文件？y/n：").lower() == "y":
                        if t_name in read_list:
                            read_list.remove(t_name)
                            log("✅ 文件已删除")
                else:
                    pre = cur_path + SEP + t_name if cur_path else t_name
                    cnt = len([f for f in read_list if f.startswith(pre)])
                    if input(f"⚠️ 删除文件夹【{t_name}】({cnt}文件)？y/n：").lower() == "y":
                        read_list[:] = [f for f in read_list if not f.startswith(pre)]
                        log("✅ 文件夹已删除")
            else:
                log("❌ 无效序号")
            continue

        if choice == "c":
            if input("⚠️ 确认清空全部？y/n：").lower() == "y":
                read_list.clear()
                nav_stack = [""]
                log("✅ 已清空")
            continue

        # s=扫描 r=切换根目录
        if choice == "s":
            scan_available_files()
            continue
        if choice == "r":
            change_root_dir()
            continue

        log("❌ 无效指令")

# 流程控制
if not is_debugging:
    homepage()