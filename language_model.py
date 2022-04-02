import sys
import re
import math
import random
import string


stopword= ['', "" , 'if','do', 'few', "it's",  'has', 'its', 'with' ,'can', 'been', 'won', "you'll", 'below', "weren't", 'into', 'him', 'this', 'our', 'above', "needn't", 'here', 'i' ,'me','all', 're', "won't", 'don', 'should', 'such', 'for',"couldn't" ,"or",'what' ,"should've" ,'does',"hers","other","that'll", "doesn't", "wasn't", 'once', 'while', 'between', 'mightn', "hasn't", 'too', 'up', 'before', 'their', 'himself', 'it', "you'd", 'some', 'themselves', 'ain', 'an', 'ours', 'at', 'haven', 'about', 'just', 'shouldn', 'o', 'both', 'out', "isn't", 'll', 'ma', 'you', "haven't", 'only', 'hadn', 'those', 'they', 'against', 'down', 'over', 't', 'she', 'again', 'why', 'did', 'wouldn', 'a', 'when', 'your', 'ourselves', 'who', 'having', 'on', 'y', 'theirs', 'being', 'herself', 'nor', 'that', 'by', "don't", "mustn't", "shan't", 'because', 'not', 'under', 'are', 'he', 'own', "you've", 'there', 'yours', 'and', 'most', "mightn't", 'have', 'doing', 'during', 'couldn', "didn't", 'will', 'weren', 'd', 'were', "she's", "wouldn't", 'isn', 'then', 'doesn', 'wasn', 'itself', 'now', 'didn', 'these', 'them', 'needn', 'yourself', 'shan', 'is', 'more', 'be', "you're", 'than', 'after', 'aren', 'how', 'where', 'which', 'in', "hadn't", 'further', 'no', 'yourselves', 'as', 'whom', 'to', 'hasn', 'mustn', 'through', 'the', 'm', 's', 'very', 'we', 'each', 'until', 'same', "aren't", 'was', 'my', 'so', 'from', 've', 'am', 'had', 'his', 'but', 'off', 'any',"of","her", "shouldn't","myself"]

def remove_stopword(text):
    final_words = []
    for line in text:
        l=[]
        for word in line:
            if word not in stopword:
                l.append(word)
        final_words.append(l)
    return final_words

def remove_punctuation(text):
    p = '''!()-{}[];:'"\,<>?#@$&%^/*_~'''
    new_text= ""
    for char in text:
        if char in p:
            continue
        else:
            new_text = new_text + char
    return new_text

def cleanData(corpus,path):
    data = remove_punctuation(re.sub(' +', ' ', corpus.lower()))
    final_data = re.compile(r'<[^>]+>').sub('',str(data))
    final_data = re.sub(r'[^a-zA-Z0-9. ]','', final_data)
    return final_data

def genrateGrams(n,tokens):
    dic=dict()
    ngramslist=[]
    for sentence in tokens:
        x=len(sentence) -n
        for i in range(x):
            y = sentence[i:i+1+n]
            y_tuple = tuple(i for i in y) 
            ngramslist.append(y_tuple)
    for gram in ngramslist:
        if gram in dic:
            dic[gram]+=1
        else:
            dic[gram]=1    
    return dic


def precidingInput(input,grams):
    temp=0
    for key,value in grams.items():
        x=key[-1]
        if(x==input):
            temp=1+temp
    return temp


def CalcPerp(prob,N):
    if prob==0:
        return 0
    return prob**(-1/N)

# Kneser-Ney smoothing
def KneserNey(input,gm_list,term):
    inputdic = {}
    firsterm=0
    num=0
    lambda_fnc= 0
    gm3_list = gm_list[3]
    gm_list_i = gm_list[4-term]

    if term== 4:
        inputdic={}
        i = 4-term
        for key,value in gm_list_i.items():
            x= key[:3-i]
            if(x==input[:term-1]):
                inputdic[key]=value
        denom=sum(inputdic.values())

        if input in gm_list[0].keys():
            num=gm_list[0][input]
    else:
        denom=len(gm_list_i)
        num=precidingInput(input[-1],gm_list_i)
    aa=3/4
    if max(0,num-(aa)) != 0:
        firsterm = max(0,num-0.75)/denom
    if term==4:
        if len(inputdic) != 0:
            lambda_fnc = (aa* len(inputdic))/sum(inputdic.values())

    elif term == 1:
        lambda_fnc = (aa*len(gm3_list))/sum(gm3_list.values())
    else:
        inputdic={}
        i = 4-term
        for key,value in gm_list_i.items():
            x= key[:3-i]
            if(x==input[:term-1]):
                inputdic[key]=value   
        if len(inputdic)!= 0:
            sum_val = sum(inputdic.values())
            nn = len(inputdic)
            lambda_fnc = ((3/4)*nn) /sum_val
    
    if term!=1 and lambda_fnc!=0:
        Kneserfunct = KneserNey(input[1:],gm_list,term-1)
        return firsterm+ lambda_fnc*Kneserfunct
    else:
        return firsterm+lambda_fnc


#written bell smoothing
def WittenBell(input,gm_list,term):
    ip_cnt=0
    gm_list_i = gm_list[4-term]
    if input in gm_list_i.keys():
        ip_cnt = gm_list_i[input]
    total_count = sum(gm_list_i.values())
    if(term == 1):
        nc = len(gm_list[3])
        nc_plus_cnt = total_count+nc
        return ((total_count/nc_plus_cnt)*(ip_cnt/total_count)) + (1/nc_plus_cnt)
    inputdic={}
    i = 4-term
    for key,value in gm_list_i.items():
        x= key[:3-i]
        if(x==input[:term-1]):
            inputdic[key]=value
    
    nc = len(inputdic)
    o_lambda=0
    if len(inputdic) != 0:
        o_lambda = nc/(nc + sum(inputdic.values()))
    
    if o_lambda ==0:
        return (((1-o_lambda) * ip_cnt)/total_count)
    return (((1-o_lambda) * ip_cnt)/total_count) + ((1-o_lambda) * WittenBell(input[1:],gm_list,term-1))
    
             
def UserInput(gm_list,smoothing_type,path):
    input_sentence = input()
    input_sentence = cleanData(input_sentence,path)
    temp = input_sentence.split(" ")
    vocab =[]
    
    for word in temp:
        if word not in stopword:
            vocab.append(word)
    if(len(input_sentence)==0):
        return
    temp=vocab
    temp = tuple(i for i in temp) 
    prob,tempprob=1,1
    

    gm3_list = gm_list[3]
    a=3/4
    if(len(temp)<=3):
        if(smoothing_type=='k'):
            prob = prob* KneserNey(temp, gm_list, len(temp))
            
            if tempprob == 0:
                vv = sum(gm3_list.values())
                tempprob = (len(gm3_list) * a)/vv
        elif smoothing_type == 'w':
            prob *= WittenBell(temp,gm_list,len(temp))
            if prob == 0:
                vv = sum(gm3_list.values())
                prob = (len(gm3_list) *a)/vv

            if prob ==0:
                ip_cnt=0
                if input in gm3_list.keys():
                    ip_cnt = gm3_list[input]
                total_count = sum(gm3_list.values())
                nc = len(gm3_list)
                yy = total_count + nc
                prob = ((total_count/yy)*(ip_cnt/total_count)) + (1/yy)
    else:
        for j in range(-3+len(temp)):
            if(smoothing_type=='k'):
                tempprob = KneserNey(temp[j:4+j],gm_list,4)
                if tempprob == 0:
                    tempprob = (len(gm3_list) *a)/( sum(gm3_list.values()))
            elif smoothing_type == 'w':
                tempprob = WittenBell(temp[j:4+j],gm_list,4)
                if tempprob==0:
                    ip_cnt=0
                    if input in gm3_list.keys():
                        ip_cnt = gm3_list[input]
                    total_count = sum(gm3_list.values())
                    nc = len(gm3_list)
                    yy = total_count + nc
                    tempprob = ((total_count/yy)*(ip_cnt/total_count)) + (1/yy)
            
            prob= tempprob*prob
    
    perp = CalcPerp(prob,len(temp))

    print("Probability="+str(prob))
    print("Perplexity="+str(perp))
    


def runData1(gm_list,data1,smoothing_type):
    f = open("./2020201092-LM1-train-perplexity.txt","x") # kept changing

    avgperp=0
    
    for i in range(0,len(data1)):
        
        if(len(data1[i])<=0):
            continue

        temp = tuple(i for i in data1[i])
        prob,tempprob=1,1
        
        gm3_list = gm_list[3]
        
        if(len(temp)>3):
            for j in range(-3+len(temp)):
                if(smoothing_type=="k"):
                    tempprob = KneserNey(temp[j:j+4], gm_list, 4)
                    
                    if tempprob==0:
                        sum_val=sum(gm3_list.values())
                        tempprob=(len(gm3_list) * (3/4))/(sum_val)

                elif smoothing_type=="w":
                    tempprob = WittenBell(temp[j:4+j], gm_list, 4)

                    if tempprob==0:
                        ip_cnt=0
                        if input in gm3_list.keys():
                            ip_cnt = gm3_list[input]
                        total_count = sum(gm3_list.values())
                        nc = len(gm3_list)
                        abc = ip_cnt/total_count
                        tempprob = ((total_count/ (total_count +nc))*abc) + (1/(nc+total_count))
                print(tempprob)
                        
                prob= tempprob *prob
            
        else:
            if(smoothing_type == 'k'):
                Kneserfunct = KneserNey(temp,gm_list,len(temp))
                prob = prob * Kneserfunct
            elif smoothing_type == 'w':
                WittenBellfunc = WittenBell(temp,gm_list,len(temp))
                prob *= WittenBellfunc
                sum_val = sum(gm3_list.values())
                if prob==0:

                    prob = (len(gm3_list)* (3/4))/( sum_val)
                if prob == 0:
                    ip_cnt=0
                    if input in gm3_list.keys():
                        ip_cnt = gm3_list[input]
                    nc = len(gm3_list)
                    prob = ( (sum_val / (sum_val+ nc))* (ip_cnt/sum_val)) + (1/(nc+sum_val))

        perp= CalcPerp(prob,len(temp))
        avgperp= avgperp + perp
        f.write(" ".join(data1[i]) +"\t"+str(perp))
        f.write("\n")
    
    avgperp= avgperp/len(data1)
    f.write("averagePerplexity : \t" + str(avgperp))
    f.close()
    
def main():
    smoothing_type=sys.argv[1]
    path=sys.argv[2]
    
    
    print("input a sentence? (y/n):")
    ch =input()

    file = open(path)
    corpus = file.read()
    totsl_sent = 1000
    cleaned_corpus = cleanData(corpus,path)

    sentences = []
    for temp in cleaned_corpus.split("."):
        sentences.append(temp.strip())

    tokens=[]
    for temp in sentences:
        tokens.append(temp.split(" "))
    tokens = remove_stopword(tokens)

    if(ch=='n'):
        curr_sent = len(tokens)
        curr_sent-=1

        data1=[]
        for i in range(totsl_sent):
            data1.append(tokens.pop(random.randint(0,curr_sent)))
            curr_sent-=1

    gm_list=[]
    gm_list.append(genrateGrams(3,tokens))
    gm_list.append(genrateGrams(2,tokens))
    gm_list.append(genrateGrams(1,tokens))
    gm_list.append(genrateGrams(0,tokens))


    if(ch=='y'):
        UserInput(gm_list,smoothing_type,bol)
    else:
        runData1(gm_list,data1,smoothing_type)


main()