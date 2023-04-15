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
        #self.variable_list = dict()
        self.arguments = args
        #Is this code even necessary?
        '''
        for i in range(len(args)):
            if(isVariable(args[i])):
                variable = Variable(args[i])
                self.arguments.append(args[i])
                if(args[i] in self.variable_list):
                    self.variable_list[variable.name].append(i)
                else:
                    self.variable_list[variable.name] = [i]
                self.variable_present = True
            else: #It must be a constant - is this the case??
                constant = Constant(args[i])
                self.arguments.append(args[i])
        '''
        self.negationSign  = negation

    def __hash__(self) -> int:
        return hash(self.__str__())
    
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
    
    def getEverythingOtherThanNegation(self)->str:
        arg_str = ""
        for arg in self.arguments:
            if arg_str == "":
                arg_str = arg
            else:
                arg_str = arg_str+","+arg
        return self.name+"("+ arg_str + ")"
    
    def getHashableString(self)->str:
        arg_str = ""
        for arg in deepcopy(self.arguments):
            if(isVariable(arg)):
                arg = 'var'
            if arg_str == "":
                arg_str = arg
            else:
                arg_str = arg_str+","+arg
        return self.getPredicateName()+"("+ arg_str + ")"




class Sentence:
    def __init__(self,predicateList:list):
        self.predicates  = predicateList
        '''
        self.variable_set = set()
        for predicate in predicateList:
            variable_list = predicate.variable_list
            for variable in variable_list.keys():
                self.variable_set.add(variable)
        '''
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
    
cleanKb = KB([])
counter = 0
predicate_sentence_hash = {}


def getAVariable(dictionary):
    for key in list(dictionary.keys()):
        if(not dictionary[key]):
            return key


def changeVariables(sentence1,sentence2):
    print("Change variables\n")
    
    #variable_set_1 = sentence1.variable_set
    #variable_set_2 = sentence2.variable_set
    variable_set_1 = set()
    variable_set_2 = set()
    for pred in sentence1.predicates:
        for arg in pred.arguments:
            if(isVariable(arg)):
                variable_set_1.add(arg)
    
    for pred in sentence2.predicates:
        for arg in pred.arguments:
            if(isVariable(arg)):
                variable_set_2.add(arg)

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
        #Takes one common variable at a time.
        predicate_list = new_second_sentence.predicates
        safe_variable_number = getAVariable(hash_dict)
        safe_variable = chr(safe_variable_number + ord('a'))

        for i in range(len(predicate_list)):
            for j in range(0,len(predicate_list[i].arguments)):
                if predicate_list[i].arguments[j] == common:
                    predicate_list[i].arguments[j] = safe_variable
        

        '''
        for i in range(len(predicate_list)):
            if common in predicate_list[i].variable_list:
                places = predicate_list[i].variable_list[common]
                print("Places where "+common+" occurs is "+str(places)+"\n")
                
                print("For that, safe variable is "+safe_variable+"\n")
                
                del new_second_sentence.predicates[i].variable_list[common]
                for place in places:
                    new_second_sentence.predicates[i].arguments[place] = safe_variable
                new_second_sentence.predicates[i].variable_list[safe_variable] = places
        '''
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

def recursion(sub,x):
    val = sub[x]
    if(not isVariable(val)):
        return val
    else:
        if(isVariable(val) and val in sub.keys):
            recursion(sub,val)

def unionFind(sub):
    print("Union find: "+str(sub))
    for key,value in sub.items():
        if(isVariable(value) and value in sub.keys()):
            print("Value that is a variable : "+value)
            sub[key] = recursion(sub,value)
    return sub
        
def findSubstitution(sentence1,sentence2,substitution):
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
    substitution = unionFind(substitution)
    print("After substitution : "+str(substitution))
    return substitution,sentence3

def applySubstitution(substitution,sentence):
    replacement_sentence = deepcopy(sentence)
    print("sentence: "+str(replacement_sentence))
    for predicate in replacement_sentence.predicates:
        for i in range(len(predicate.arguments)):
            if(predicate.arguments[i] in substitution):
                predicate.arguments[i] = substitution[predicate.arguments[i]]
    return replacement_sentence
    print("Replacement Sentence : "+str(replacement_sentence))


def resolveTwoSentences(sentence1,sentence2):
    substitution,standardized_sentence = findSubstitution(sentence1,sentence2,{})
    new_sentence1 = applySubstitution(substitution,sentence1)
    new_sentence2 = applySubstitution(substitution,standardized_sentence)
    #Onnu dha iruku nu assumption.
    sentence3 = deepcopy(standardized_sentence)
    sentence_1_set = set()
    sentence_2_set = set()
    print("Enna type : "+str(type(sentence1.predicates)))
    new_list = experimentalOrClause(new_sentence1,new_sentence2)
    print("After OR-ing : "+str(new_list))





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

def eligibileForElimination(predicate1,predicate2):
    if((predicate1.negationSign and not predicate2.negationSign) or (predicate2.negationSign and not predicate1.negationSign)):
        if(predicate1.getEverythingOtherThanNegation() == predicate2.getEverythingOtherThanNegation()):
            return True
    return False

def experimentalOrClause(sentence1,sentence2):
    print("OR-ing for "+str(sentence1)+"--"+str(sentence2)+"\n")
    ans = set()
    if sentence1 and not sentence2:
        return sentence1
    elif sentence2 and not sentence1:
        return sentence2
    set1 = set(sentence1.predicates)
    set2 = set(sentence2.predicates)
    print("Sets: \n")
    print("*****\n")
    for item1 in set1.copy():
        elimination_possible = False
        for item2 in set2.copy():
            if(eligibileForElimination(item1,item2)):
                print("Elimination possible for: "+str(item1)+"--"+str(item2)+"\n")
                elimination_possible = True
                set2.remove(item2)
        if(elimination_possible):
            set1.remove(item1)
    print("*****\n")
    print(str(set1)+"---"+str(set2))
    union_ans = set1.union(set2)
    
    print("Answer: \n")
    #for obj in union_ans:
    #    print(obj)
    sentence3 = Sentence(union_ans)
    print(sentence3)
    #print("Union answer : "+str(union_ans))
    return sentence3




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

def getSentenceObject(cnf_terms):
    predicate_array = list()
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
    global sentence_id
    sentence.id = sentence_id
    sentence_id = sentence_id + 1
    for pred in predicate_array:
        key = pred.getHashableString()
        #print("Key: "+key)
        if( key in predicate_sentence_hash):
            already_present_set = predicate_sentence_hash[key]
            already_present_set.add(sentence.id)
            predicate_sentence_hash[key] = already_present_set
        else:
            newSet = set()
            newSet.add(sentence.id)
            predicate_sentence_hash[key] = newSet
    for predicate in sentence.predicates:
        print("Hash oda string ",predicate.getHashableString()+"\n")
    return sentence

f = open("input.txt")
lines = f.readlines()
query = lines[0].rstrip("\n")
query_without_white_spaces = query.replace(" ","")
if query_without_white_spaces[0]=="~":
    negatedQuery = query_without_white_spaces.replace('~','',1)
else:
    negatedQuery = "~"+query_without_white_spaces

query_cnf = convert_to_cnf(negatedQuery)
simplified_cnf = simplify_terms(query_cnf)
for simple_term in simplified_cnf:
    query_sentence = getSentenceObject(simple_term)
    print("Query Sentence : "+str(query_sentence))
    cleanKb.append(query_sentence)


#print(query)
kb_size = int(lines[1].rstrip("\n"))
#print(kb_size)

sentence_id = 0

for i in range(2,kb_size+2):
    sentence = lines[i].rstrip("\n")
    #print("Before: "+sentence+"\n")
    without_white_spaces = sentence.replace(" ","")
    cnf = convert_to_cnf(without_white_spaces)
    #print("After: "+ str(cnf)+"\n")
    simplified_cnf = simplify_terms(cnf)
    for simplified_cnf_term in simplified_cnf:
        sentence_obj = getSentenceObject(simplified_cnf_term)
    cleanKb.append(sentence_obj)
    #convertToSentenceFormAndAddToKB(simplified_cnf)
    #print("After: "+str(simplified_cnf)+"\n")



print("Clean KB : "+ str(cleanKb)+"\n")
#print("Unification : \n")
#print(resolveTwoSentences(cleanKb.sentences[0],cleanKb.sentences[1]))
#print("Unification Complete")

#changeVariables(cleanKb.sentences[0],cleanKb.sentences[1])
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