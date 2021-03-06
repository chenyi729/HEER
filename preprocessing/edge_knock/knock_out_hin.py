#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Mon Dec 11 13:12:43 2017

@author: Fang Guo

'''

from random import sample,choice
import time
import math
import argparse


# ko_dic records all the tuple that have been knocked out, format: a: {p1,p2...}; w:{p1,p2,...}

def ko_edge(tuple_list,ko_rate,a_dic,p_dic,index2type,file_hin):
    size=len(tuple_list)
    ko_dic={}
    ko_index_list=sample(range(size-1),math.ceil(size*ko_rate))
    for i in ko_index_list:
        
        tuple_list[i][-1]='0'
        node1_value=tuple_list[i][0] #it must be in P type
        node2_value=tuple_list[i][1] #it will be A or P or Other
        node1_type=index2type[node1_value]
        node2_type=index2type[node2_value]
        '''For both a_dic,p_dic and o_dic, if after knocking out, the node has an empty dictionary
           then the node will be poped in the dictionary which it belongs to. 
        '''
        if (node2_type=='A'): 
            if node2_value in a_dic:
                try:
                    del a_dic[node2_value][node1_value]
                except KeyError:
                    pass
                if bool(a_dic[node2_value])==False:
                    try:
                        del a_dic[node2_value]
                    except KeyError:
                        pass
            if node1_value in p_dic:
                try:
                    del p_dic[node1_value][node2_value]
                except KeyError:
                    pass
                if bool(p_dic[node1_value])==False:
                    try:
                        del p_dic[node1_value]
                    except KeyError:
                        pass
        else:
            if (node2_type=='P'): 
                if node2_value in p_dic:
                    try:
                        del p_dic[node2_value][node1_value]
                    except KeyError:
                        pass
                    if bool(p_dic[node2_value])==False:
                        try:
                            del p_dic[node2_value]
                        except KeyError:
                            pass
            else:
                if node2_value in o_dic[node2_type]:
                    try:
                        del o_dic[node2_type][node2_value][node1_value]
                    except KeyError:
                        pass
                    if bool(o_dic[node2_type][node2_value])==False:
                        try:
                            del o_dic[node2_type][node2_value]
                        except KeyError:
                            pass
            if node1_value in p_dic:
                try:
                    del p_dic[node1_value][node2_value]
                except KeyError:
                    pass
                if bool(p_dic[node1_value])==False:
                    try:
                        del p_dic[node1_value]
                    except KeyError:
                        pass
                
        if node2_value not in ko_dic:
            ko_dic[node2_value]={}
            ko_dic[node2_value][node1_value]=1
        else:
            if node1_value not in ko_dic[node2_value]:
                ko_dic[node2_value][node1_value]=1
                
    #write result from tuple_list to file_hin 
    print('Started writing to file_hin')
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    file =open(file_hin,'w+')
    count=0
    content=''
    for i in tuple_list:
        if i[2]!='0':
            line=index2type[i[0]]+':'+i[0]+' '+index2type[i[1]]+':'+i[1]+' '+i[2]+'\n'
            content=content+line
        else:
            count+=1
    file.write(content)
    
    file.close()
    print('finished writing to file_hin')

    return ko_dic,tuple_list

'''

'''
def get_file_eval_info(ko_dic,a_dic,p_dic,o_dic,index2type,sample_number):
    not_valid_count=0
    count=0
    for key,dic in ko_dic.items():   
        for sub_key,edge in dic.items():
            if (index2type[key]=='A'):
            #10 negative sampling with same author, but non-relative paper
                if key not in a_dic or sub_key not in p_dic:
                    not_valid_count+=1
                    continue
                count+=1
            else: 
                if index2type[key].lower()=='p':#when key is paper type
                #10 negative sampling with same paper and non-relative papers
                    if sub_key not in p_dic or key not in p_dic:
                        not_valid_count+=1
                        continue
                    count+=1
                else:# when key is other types
                    node_type=index2type[key]
                    if sub_key not in p_dic or key not in o_dic[node_type]:
                        not_valid_count+=1
                        continue
                    count+=1
    file_eval_info=str(sample_number)+' negative example per direction in one batch, '+str(count)+' batches in total.\n'
    print(file_eval_info+'Not valid count is, '+str(not_valid_count))
    return file_eval_info
    
#neagtive sampling, one from ko_list with another 20 from random sampling with same nodes
def build_file(ko_dic,a_dic,p_dic,o_dic,index2type,type_dic,sample_number,file_eval,buffer_size):
    p_list=list(p_dic)
    a_list=list(a_dic)
    o_list={}
    for key in o_dic:
        o_list[key]=list(o_dic[key])
    file =open(file_eval,'w+')
    #for key,value in ko_dic.items():
    print('Started writing to file_eval')
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    content=''
    rd=0
    file_eval_info=get_file_eval_info(ko_dic,a_dic,p_dic,o_dic,index2type,sample_number)
    file.write(file_eval_info)
    for key,dic in ko_dic.items():   
        for sub_key,edge in dic.items():
            content_temp=[]
            temp=index2type[key]+':'+key+' '+index2type[sub_key]+':'+sub_key+' '+str(edge)+' '+index2type[key]+index2type[sub_key]+'\n'
            content_temp.append(temp)
            if (index2type[key]=='A'):
            #10 negative sampling with same author, but non-relative paper
                if key not in a_dic or sub_key not in p_dic:
                    continue
                count=0
                while count<sample_number:
                    random_paper=choice(p_list)  
                    while random_paper in a_dic[key]:
                        random_paper=choice(p_list)
                    temp='A:'+key+' '+index2type[random_paper]+':'+str(random_paper)+' '+'0'+' '+'AP-1'+'\n'
                    content_temp.append(temp)
                    count+=1
            #10 negative sampling with same paper, but random-author
                count=0        
                while count<sample_number:
                    random_author=choice(a_list)
                    while random_author in p_dic[sub_key]:
                        random_author=choice(a_list)
                    temp='P:'+sub_key+' '+'A:'+random_author+' '+'0'+' '+'PA-1'+'\n'
                    content_temp.append(temp)
                    count+=1
            else: 
                if index2type[key].lower()=='p':#when key is paper type
                #10 negative sampling with same paper and non-relative papers
                    if sub_key not in p_dic or key not in p_dic:
                        continue
                    count=0
                    while count<sample_number:
                        random_paper=choice(p_list)
                        while random_paper in p_dic[sub_key]:
                            random_paper=choice(p_list)
                        temp='P:'+sub_key+' '+index2type[random_paper]+':'+random_paper+' '+'0'+' '+'PP-1'+'\n'
                        content_temp.append(temp)
                        count+=1
                    count=0
                    while count<sample_number:
                        random_paper=choice(p_list)
                        while random_paper in p_dic[key]:
                            random_paper=choice(p_list)
                        temp=index2type[key]+':'+key+' '+'P:'+random_paper+' '+'0'+' '+index2type[key]+'P-1'+'\n'
                        content_temp.append(temp)
                        count+=1
                else:# when key is other types
                    node_type=index2type[key]
                    if sub_key not in p_dic or key not in o_dic[node_type]:
                        continue
                    count=0
                    
                    #10 negative sampling with same paper, but non-relative same other type nodes
                    while count<sample_number:
                        random_other=choice(o_list[node_type])
                        while random_other in p_dic[sub_key]:
                            random_other=choice(o_list[node_type])
                        temp='P:'+sub_key+' '+node_type+':'+random_other+' '+'0'+' '+'P'+node_type+'-1'+'\n'
                        content_temp.append(temp)
                        count+=1
                    #10 negative sampling with same other type nodes, but non-realtive papers
                    count=0
                    while count<sample_number:
                        random_paper=choice(p_list)
                        while random_paper in o_dic[node_type][key]:
                            random_paper=choice(p_list)
                        temp=node_type+':'+key+' '+'P:'+random_paper+' '+'0'+' '+node_type+'P-1'+'\n'
                        content_temp.append(temp)
                        count+=1
            content=content+''.join(content_temp)
            rd+=1
            if rd % buffer_size ==0:
                print (rd,'batches finished')
                file.write(content)
                content=''
    file.write(content)
    file.close()
    
    print('finished writing to file_eval.')
    return 

if __name__ == '__main__':
    
    start_time = time.time()
    parser = argparse.ArgumentParser(description='Read in input and output filenames.')
    parser.add_argument('--input-p2afile', nargs='?', help='Input p2a filename.', type=str)
    parser.add_argument('--input-p2ofile', nargs='?', help='Input p20 filename.', type=str)
    parser.add_argument('--input-index2name', nargs='?', help='Input index2name filename.', type=str)
    parser.add_argument('--ko-rate', nargs='?', help='Input knockout rate.', type=float)
    parser.add_argument('--sample-number', nargs='?', help='Input sample number generated per node.', type=int,default=10)
    parser.add_argument('--data-set-name', nargs='?', help='data_set_name used to build network.', type=str,default='unknown')
    parser.add_argument('--path-output', nargs='?', help='The output to write.', type=str)
    parser.add_argument('--buffer-size', nargs='?', help='Buffer Size.', type=int, default= 50000)

    args = parser.parse_args()
    '''
    First of all, we will build a directory from index2name, key-value: index:name
    '''
    filename0=args.input_index2name
    index2type={}
    type_dic={}
    with open(filename0,encoding='utf-8') as file:
        for line in file:
            line=line.split()
            second_part=line[1].split('.')
            itemtype=second_part[0]
            index2type[line[0]]=itemtype
            if second_part[0] not in type_dic:
                type_dic[itemtype]={}
            type_dic[itemtype][line[0]]=1
    for itemtype in type_dic:
        type_dic[itemtype]=list(type_dic[itemtype])
    print('finished index2type and type_dic')
    
    #create p hash ,a hash and tuple list from p2a
    filename1 = args.input_p2afile
    tuple_list=[]
    p_dic={}
    a_dic={} 
    with open(filename1) as file_1:
        count=0
        for line in file_1:
            line=line.split()
            if(line[-1]!='0'):
                tuple_list.append(line)
                #update the both the p_dic and a_dic
                if line[0] not in p_dic:
                    p_dic[line[0]]={}
                    p_dic[line[0]][line[1]]=1
                else :
                    if line[1] not in p_dic[line[0]]:
                        p_dic[line[0]][line[1]]=1
                if line[1] not in a_dic:
                    a_dic[line[1]]={}
                    a_dic[line[1]][line[0]]=1
                else:
                    if line[0] not in a_dic[line[1]]:
                        a_dic[line[1]][line[0]]=1
            count+=1
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    print('finished reading p2a')
    #get more into p hash and tuple list from p2o
    filename2 = args.input_p2ofile
    o_dic={}
    with open(filename2) as file_2:
        count=0
        for line in file_2:
            line=line.split()
            if(line[2]!='0'):
                tuple_list.append(line)
                #update both the p_dic and o_dic
                if line[0] not in p_dic:
                    p_dic[line[0]]={}
                if line[1] not in p_dic[line[0]]:
                    p_dic[line[0]][line[1]]=line[2]
                
                node_type=index2type[line[1]]
                #Check whether its PP type   
                if node_type.lower()=='p':
                    if line[1] not in p_dic:
                        p_dic[line[1]]={}
                    if line[0] not in p_dic[line[1]]:
                        p_dic[line[1]][line[0]]=line[2]
                else:
                    if node_type not in o_dic:
                        o_dic[node_type]={}
                    if line[1] not in o_dic[node_type]:
                        o_dic[node_type][line[1]]={}
                    if line[0] not in o_dic[node_type][line[1]]:
                        o_dic[node_type][line[1]][line[0]]=1
            count+=1
    #print(o_dic)
    #print(p_dic)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    print('finished reading p2o') 

    ko_rate=args.ko_rate
    sample_number=args.sample_number
    data_set_name=args.data_set_name
    path_out=args.path_output
    file_hin=path_out+'/'+data_set_name+'_ko_'+str(ko_rate)+'.hin'
    file_eval=path_out+'/'+data_set_name+'_ko_'+str(ko_rate)+'_'+str(sample_number)+'_eval.txt'
    ko_dic,tuple_list=ko_edge(tuple_list,ko_rate,a_dic,p_dic,index2type,file_hin)
    buffer_size=args.buffer_size
    build_file(ko_dic,a_dic,p_dic,o_dic,index2type,type_dic,sample_number,file_eval,buffer_size)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    
    
  
    