#AI-lab 开发者：浪兮（hhu2524030232张锐寒）

"""
    【开发者注】

"""


import re
import time
import os
import random
import math
import numpy as np
from datetime import datetime


"""
    【日志记录模块】 2026.3.17 浪兮（hhu2524030232张锐寒）
"""


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


"""
    【文本处理模块】  2026.3.17 浪兮（hhu2524030232张锐寒）
"""


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


"""
    【词库管理模块】  2026.3.17 浪兮（hhu2524030232张锐寒）
"""


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
            match menu2("词库管理", "skill", "返回主页","词库统计","词库显示","词库整理","词库导出","词库测试"):
                case 0:
                    return -2
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    pass

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

#流程控制
homepage()

