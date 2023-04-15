import os
import re
from copy import deepcopy
from collections import deque
import itertools



class PredicateFunctions:
    def __init__(self,predicateName,args,negation,valAsString):
        self.name = predicateName
        self.arguments = args
        self.negationSign  = negation
        self.stringVal = valAsString


class Sentence:
    def __init__(self,predicateList:list):
        self.predicates  = predicateList

class KB:
    def __init__(self,sentenceList:list):
        self.sentences = sentenceList


def negateClause(clause:str) -> str:
    ans = str()
    if "&" in clause and not "|" in clause:
        and_terms = clause.split("&")
        for term in and_terms:
            if(ans==""):
                ans = "~"+term
            else:
                ans = ans + "|" + "~" + term
        return ans
    elif "|" in clause and not "&" in clause:
        or_terms = clause.split("|")
        for term in or_terms:
            if(ans==""):
                ans = "~"+term
            else:
                ans = ans +"&"+"~"+term
        return ans
    else:
        #First step, we split the clause by all the OR terms it contains.
        or_terms = clause.split("|")
        for term in or_terms:
            sub_ans = str()
            if('&' in term):
                and_terms = term.split("&")
                for literal in and_terms:
                    if(sub_ans == ""):
                        sub_ans = sub_ans+"~"+literal
                    else:
                        sub_ans = sub_ans + "|" + "~"+literal
            else:
                sub_ans = "~"+term
            if(ans==""):
                ans = ans + sub_ans
            else:
                ans = ans + "&" + sub_ans
    return ans


def distribute(clause:str)->str:
    ans = str()
    if "&" in clause and not "|" in clause:
        print(clause + "already in cnf")
    elif "|" in clause and not "&" in clause:
        print(clause + "already in cnf - all disjunctions")
    else:
        or_terms = clause.split("|")
        outer_res = []
        for term in or_terms:
            and_terms = term.split("&")
            outer_res.append(and_terms)
        #print(outer_res)
        combination = [p for p in itertools.product(*outer_res)]
        print("Combination: "+str(combination))
        ans = str()
        for combination_item in combination:
            inter_ans = str()
            for individual_items in combination_item:
                print("IndividualItems :"+individual_items)
                if(inter_ans==""):
                    inter_ans = inter_ans + individual_items 
                else:
                    inter_ans = inter_ans+"|"+individual_items
                
            if(ans == ""):
                ans = ans+ inter_ans
            else:
                ans = ans + "&" + inter_ans
        
    return ans








def convert_to_cnf(clause:str)->str:
    ans = str()
    if("=>" in clause):
        #Here I can say two parts because there can be only one implication sign in the sentence.
        lhs = clause.split("=>")[0]
        rhs = clause.split("=>")[1]

        lhs = negateClause(lhs)
        pre_dis = lhs+"|"+rhs
        ans  = distribute(pre_dis)
    else:
        ans = distribute(clause)
    
    return ans





def to_cnf(clause:str) -> str:
    variables=set()
    if '=>' in clause:
        print("There is a imply sign.\n")
        lhs,rhs=clause.split('=>')[0],clause.split('=>')[1]
        if '&' in lhs and '|' not in lhs: 
            print("First case ")
            lhs = '|'.join([x[1:] if x[0]=='~' else '~'+x for x in lhs.split('&')])
            clause=lhs+'|'+rhs
            print(clause)
        elif '|' in lhs and '&' not in lhs: 
            lh=[]
            for l in lhs.split('|'):
                if l[0]=='~': lh.append(l[1:]+'|'+rhs)
                else: lh.append('~'+l+'|'+rhs)
            if len(lh)>1:
                print(lh)
                print(lh[1:]) 
                #self.kb.extend(lh[1:])
                #self.k+=1
            clause=lh[0]
        else:
            if lhs[0]=='~': clause=lhs[1:]+'|'+rhs 
            else: clause='~'+lhs+'|'+rhs
    else:
        if '&' in clause:
            csplt=clause.split('&')
            if len(csplt)>1: 
                #self.kb.extend(csplt[1:])
                #self.k+=1
                print(csplt[1:])
            clause=csplt[0]
    print(clause)

sentence = "~a|b&c"
distribute_sentence = ""



#print("Standalone: "+negateClause(sentence))
print("Standalone Distribute: "+convert_to_cnf(negateClause(sentence)))
f = open("input.txt")
lines = f.readlines()
query = lines[0].rstrip("\n")
print(query)
kb_size = int(lines[1].rstrip("\n"))
print(kb_size)


rawKB = []
kb1 = []
kbWithoutParantheses = []
cleanKb = []
counter = 0



for i in range(2,kb_size+2):
    sentence = lines[i].rstrip("\n")
    print(sentence+"Before")
    without_white_spaces = sentence.replace(" ","")
    rawKB.append(without_white_spaces)
    #to_cnf(without_white_spaces)
    #print(sentence)
    
print(kb)


# create output file
if os.path.isfile("output.txt"):
    wf = open("output.txt", 'w')
    wf.truncate()
else:
    wf = open("output.txt", 'w')



output = False
wf.write(str(output))
wf.write("\n")
wf.close()