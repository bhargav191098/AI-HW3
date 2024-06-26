import os
import re
from copy import deepcopy
from collections import deque
import itertools


sentence_id = 0

class Variable:
    def __init__(self,var_name):
        self.name = var_name
    def __str__(self) -> str:
        return self.name
    def __eq__(self, other: object) -> bool:
        if(type(self)!= type(other)):
            return False
        return (self.name == other.name)

class Constant:
    def __init__(self,constant_value) -> None:
        self.value = constant_value
    def __str__(self) -> str:
        return self.value
    def __eq__(self, __value: object) -> bool:
        if(type(self)!= type(__value)):
            return False
        return self.value == __value.value

        

class PredicateFunctions:
    def __init__(self,predicateName,args,negation):
        self.name = predicateName
        #self.arguments = args
        self.variable_present = False
        self.arguments = list()  
        self.variable_list = dict()
        for i in range(len(args)):
            if(isVariable(args[i])):
                variable = Variable(args[i])
                self.arguments.append(args[i])
                if(args[i] in self.variable_list):
                    self.variable_list[variable.name].append(i)
                else:
                    self.variable_list[variable.name] = [i]
                self.variable_present = True
            else: #It must be a constant - is this the case?
                constant = Constant(args[i])
                self.arguments.append(args[i])
        self.negationSign  = negation

    def __hash__(self) -> int:
        return hash(self.name,self.negationSign,self.arguments)
    
    def __str__(self) -> str:
        ans = ""
        if self.negationSign:
            ans = ""+ "~"
        arg_str = ""
        for arg in self.arguments:
            if arg_str == "":
                arg_str = arg
            else:
                arg_str = arg_str+","+arg
        return ans+self.name+"("+ arg_str + ")"
    

    def __eq__(self, __value: object) -> bool:
        if(self.__class__ == __value.__class__):
            if(self.name == __value.name):
                if(self.negationSign == __value.negationSign):
                    if(self.arguments == __value.arguments):
                        return True
        return False



    def getPredicateName(self) -> str:
        if(self.negationSign):
            return "~"+self.name
        else:
            return self.name



class Sentence:
    def __init__(self,predicateList:list):
        self.predicates  = predicateList
        self.variable_set = set()
        for predicate in predicateList:
            variable_list = predicate.variable_list
            for variable in variable_list.keys():
                self.variable_set.add(variable)
    def __hash__(self) -> int:
        return hash(self.predicates)
    
    def __str__(self) -> str:
        ans = ""
        for predicate in self.predicates:
            if(ans == ""):
                ans = str(predicate)
            else:
                ans = ans + "|"+str(predicate)
        return ans

    def __eq__(self, __value: object) -> bool:
        if(self.__class__ == __value.__class__):
            if(self.predicates == __value.predicates):
                return True
        return False


class KB:
    def __init__(self,sentenceList:list):
        self.sentences = sentenceList
    def append(self,sentence:Sentence):
        self.sentences.append(sentence)
    
    def __str__(self) -> str:
        ret = ""
        for sentence in self.sentences:
            if(ret == ""):
                ret = str(sentence)
            else:
                ret = ret + "\n" + str(sentence)
        return ret

def getAVariable(dictionary):
    for key in list(dictionary.keys()):
        if(not dictionary[key]):
            return key


def changeVariables(sentence1,sentence2):
    print("Change variables\n")
    variable_set_1 = sentence1.variable_set
    variable_set_2 = sentence2.variable_set

    intersection_set = variable_set_1.intersection(variable_set_2)
    hash_dict = { ints: False for ints in range(26) }
    print(hash_dict)

    for variable in variable_set_1:
        index = ord(variable)-ord('a')
        hash_dict[index] = True

    for variable in variable_set_2:
        index = ord(variable)-ord('a')
        hash_dict[index] = True
    print("Common variables : "+str(intersection_set))
    new_second_sentence = deepcopy(sentence2)
    for common in intersection_set:
        predicate_list = sentence2.predicates
        safe_variable_number = getAVariable(hash_dict)
        safe_variable = chr(safe_variable_number + ord('a'))
        for i in range(len(predicate_list)):
            if common in predicate_list[i].variable_list:
                places = predicate_list[i].variable_list[common]
                print("Places where "+common+" occurs is "+str(places)+"\n")
                
                print("For that, safe variable is "+safe_variable+"\n")
                
                del new_second_sentence.predicates[i].variable_list[common]
                for place in places:
                    new_second_sentence.predicates[i].arguments[place] = safe_variable
                new_second_sentence.predicates[i].variable_list[safe_variable] = places
        hash_dict[safe_variable_number] = True
        print("After this change, sentence 2 is like: ",str(new_second_sentence))
        

    print("New sentence: \n")
    print(new_second_sentence)
    #print("*****\n")
    return new_second_sentence
    #print(variable_set_1.intersection(variable_set_2))

def getConstantIfItExists(diction,key):
    if isVariable(key) and key not in diction.keys():
        return None
    elif isVariable(key) and key in diction.keys(): 
        if not isVariable(diction[key]):
            return diction[key]
        else:
            return getConstantIfItExists(diction,diction[key])
    return None



def unifySentences(sentence1,sentence2,substitution):
    print("Sentences : "+ str(sentence1) + "---"+ str(sentence2))
    if substitution is None:
        return None
    if(isinstance(sentence1,Sentence) and isinstance(sentence2,Sentence)):
        ret = {}
        sentence3 = changeVariables(sentence1,sentence2)
        print("In unify new sentence : "+str(sentence3))
        for predicate1 in sentence1.predicates:
            for predicate2 in sentence3.predicates:
                #if(predicate1.name == predicate2.name):
                #    if(predicate1.arguments.size() == predicate2.arguments.size()):
                #        for i in range(arguments.size()):
                #            inter_ans = unifyArgs(predicate1.arguments[i],predicate2.arguments[i],substitution)
                print("Calling unify for "+str(predicate1)+str(predicate2)+"with substitution "+str(substitution))
                sub = unify(predicate1,predicate2,substitution)
                if(sub!=None):
                    substitution = sub
                print("Outer :" +str(substitution))
    return substitution

def isVariable(x):
    if(isinstance(x,PredicateFunctions)):
        return False
    if(x.islower() and len(x)==1):
        return True
    return False


def unify(x, y, subst):
    print("x: "+str(x)+" | y: "+str(y)+" | substitution: "+str(subst))
    if subst is None:
        return None
    elif x == y:
        return subst
    elif isVariable(x):
        return unify_variable(x, y, subst)
    elif isVariable(y):
        return unify_variable(y, x, subst)
    elif isinstance(x, PredicateFunctions) and isinstance(y, PredicateFunctions):
        if x.name != y.name or len(x.arguments) != len(y.arguments):
            print("x name: "+x.name+"y name: "+y.name+" not equal : subst: "+str(subst)+"\n")
        else:
            for i in range(len(x.arguments)):
                subst = unify(x.arguments[i], y.arguments[i], subst)
            return subst
    else:
        return None

def occurs_check(v, term, subst):
    assert isVariable(v)
    if v == term:
        return True
    elif isVariable(term) and term in subst:
        return occurs_check(v, subst[term.name], subst)
    elif isinstance(term, PredicateFunctions):
        return any(occurs_check(v, arg, subst) for arg in term.arguments)
    else:
        return False


def unify_variable(v, x, subst):
    print("v: "+str(v)+"| x: "+str(x)+"| substition: "+str(subst))
    assert isVariable(v)
    if v in subst:
        return unify(subst[v], x, subst)
    elif isVariable(x) and x in subst:
        return unify(v, subst[x], subst)
    elif occurs_check(v, x, subst):
        return None
    else:
        print("Substution made : "+ v+ " : " +x)
        return {**subst, v: x}



def negateClause(cnf_form):
    #print("Calling negate for "+str(cnf_form))
    ans = ""
    for and_term in cnf_form:
        sub_res = ""
        for or_term in and_term:
            if(sub_res==""):
                sub_res = sub_res+"~"+or_term
            else:
                sub_res = sub_res + "&" + "~" + or_term
        if(ans==""):
            ans = ans + sub_res
        else:
            ans = ans + "|" + sub_res
    #print("Negate's answer: "+ans)
    what = convert_to_cnf(ans)
    #print("CNF OF NEGATE: "+str(what))
    return what
    
def andClauses(cnf_term_1,cnf_term_2):
    #print("Calling and for "+str(cnf_term_1)+" "+str(cnf_term_2))
    ans_cnf = cnf_term_1 + cnf_term_2
    #print("AND_ANSWER: " + str(ans_cnf))
    return ans_cnf

def orClauses(cnf_term_1,cnf_term_2):
    #print("Calling OR for "+str(cnf_term_1)+" "+str(cnf_term_2))
    ans_cnf = []
    if cnf_term_1 and not cnf_term_2:
        return cnf_term_1
    elif cnf_term_2 and not cnf_term_1:
        return cnf_term_2

    for term1 in cnf_term_1:
        for term2 in cnf_term_2:
            pre_set = set()
            pre_set = term1.union(term2)
            ans_cnf.append(pre_set)
    #print("OR_ANSWER: "+str(ans_cnf))
    return ans_cnf


def simplify_terms(cnf):
    simple_cnf = list()
    cnf.sort(key=len)
    for item in cnf:
        if not any(simple_cnf_item.issubset(item) for simple_cnf_item in simple_cnf):
            simple_cnf.append(item)
    #print(simple_cnf)
    return simple_cnf


def convert_to_cnf(clause:str):
    ans = str()
    ans_list = list()
    if("=>" in clause):
        #Here I can say two parts because there can be only one implication sign in the sentence.
        lhs = clause.split("=>")[0]
        rhs = clause.split("=>")[1]
        #print(str(negate(convert_to_cnf(lhs)))+"--"+str(convert_to_cnf(rhs)))
        return orClauses(negateClause(convert_to_cnf(lhs)),convert_to_cnf(rhs))
    elif("|" in clause):
        split_index = clause.find("|")
        lhs = clause[:split_index]
        rhs = clause[split_index+1:]
        #print(lhs+"--"+rhs)
        return orClauses(convert_to_cnf(lhs),convert_to_cnf(rhs))
    elif("&" in clause):
        split_index = clause.find("&")
        lhs = clause[:split_index]
        rhs = clause[split_index+1:]
        #print(lhs+"--"+rhs)
        return andClauses(convert_to_cnf(lhs),convert_to_cnf(rhs))
    else:
        sub_set = set()
        sub_set.add(clause)
        ans_list.append(sub_set)
        #print("Inside else part " +str(ans_list))
    return ans_list

f = open("input.txt")
lines = f.readlines()
query = lines[0].rstrip("\n")
#print(query)
kb_size = int(lines[1].rstrip("\n"))
#print(kb_size)


kbWithoutParantheses = []
cleanKb = KB([])
counter = 0
predicate_sentence_hash = {}



for i in range(2,kb_size+2):
    sentence = lines[i].rstrip("\n")
    #print("Before: "+sentence+"\n")
    without_white_spaces = sentence.replace(" ","")
    cnf = convert_to_cnf(without_white_spaces)
    #print("After: "+ str(cnf)+"\n")
    simplified_cnf = simplify_terms(cnf)
    for cnf_terms in simplified_cnf:
        predicate_array = []
        for or_terms in cnf_terms:
            #Here we convert into predicate objects.
            negate = False
            if "~" in or_terms:
                negate = True
            #Find predicate name.
            function_name = or_terms.split("(")[0]
            if(negate):
                function_name = function_name[1:]
            arguments = re.findall(r'\((.*?)\)', or_terms)[0]
            arguments_separate = arguments.split(",")
            #print(arguments_separate)
            predicate_obj = PredicateFunctions(function_name,arguments_separate,negate)
            #print(predicate_obj.name)
            #print(predicate_obj.arguments)
            #print(str(predicate_obj.negationSign))
            print(str(predicate_obj))
            predicate_array.append(predicate_obj)
        sentence = Sentence(predicate_array)
        sentence.id = sentence_id
        sentence_id = sentence_id + 1
        for pred in predicate_array:
            key = pred.getPredicateName()
            #print("Key: "+key)
            if( key in predicate_sentence_hash):
                already_present_set = predicate_sentence_hash[key]
                already_present_set.add(sentence.id)
                predicate_sentence_hash[key] = already_present_set
            else:
                newSet = set()
                newSet.add(sentence.id)
                predicate_sentence_hash[key] = newSet
        cleanKb.append(sentence)

    
    #print("After: "+str(simplified_cnf)+"\n")

print("Unification : \n")
print(unifySentences(cleanKb.sentences[0],cleanKb.sentences[1],{}))
print("Unification Complete")

changeVariables(cleanKb.sentences[0],cleanKb.sentences[1])
#print("Variable Set: "+changeVariables(cleanKb.sentences[0],cleanKb.sentences[1]))



print(str(cleanKb))
print("Hash: \n")
print(str(predicate_sentence_hash))

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