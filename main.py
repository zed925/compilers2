#!/usr/bin/python
import copy
import sys
from jouette import tiles
var_x = "['MEM', ['+', 'TEMP FP', 'CONST "

def read(file, tree, loop):
    
    ifile = open(file)
    currLevel = -1
    seq = False
    counter = 0
    for line in ifile:
        if counter == 0:
            if "SEQ" not in line:
                tree.insert("SEQ",0)
                seq = True
            
        level = line.count('=')
        
        data = line[level:][:-1]
        if seq:
            level+=1
        #print((' '*level)+data, level)
        tree.insert(data, level)
        counter+=1
    tree.insert("end", 0)
    #for i in tree.stack2.items:
    #    print(i)

    tree.get()
    print("==============================================")
    #tree.fold()
    

def readFile(file, tree):
    ifile = open(file)
    currLevel = -1
    for line in ifile:
        level = line.count('=')
        data = line[level:]
        tree.insert(data, level)
    tree.insert("end", 0)
    
class Node:
    data = None
    parent = None
    level = 0
    children = []
    
    def equals(self, other):
        ans = True
        if(self.data == other.data):
            #if not self.level == other.level:
                #print('levels dont match')
            #    return False
            if(len(self.children) == len(other.children)):
                for i in range(len(self.children)):
                    ans = ans and self.children[i].equals(other.children[i])
                #print('all good')
                return ans
            else:
                #print('mismatched kids')
                return False
        else:
            #print('mistmatched data')
            return False

    def structure(self, other):
        ans = True
        #print(self.data, other.data)
        #
        if self.data == 'MOVE' and other.data == 'MOVE':
            self.data =self.children[0].data +' = '+self.children[1].data
            self.children = []
            return True
        if(other.data =='OP' and self.data in ['+','-','*','/']):
           childs = [child.data for child in self.children]
           for i in range(len(self.children)):
               if self.children[i].data in ['+','-','*','/']:
                   self.children[i].structure(other)
                   #print(self.children[i].data)
           #print('data', self.data, chick)
           #print(childs)
           #self.get()
           if not 'TEMP' in childs:

               if(len(self.children)==2):
                    a = self.children[0].data
                    if a == 'CONST':
                       a = self.children[0].children[0].data
                    b = self.children[1].data
                    if b == 'CONST':
                        b = self.children[1].children[0].data
                    #print('a,b',a,b)
                    self.data = '('+a+' '+self.data+' '+b+')'
                    self.children = []
                    return True
        if(other.data == "VARIABLE" or other.data == "EXPRESSION" or other.data == 'input' or other.data == 'function'):
            #print("WE NOW HAVE",self.data) 
            #print("WEVE DONE IT BOYS", self.parent.parent.parent.data)
            if other.data == 'VARIABLE':
                temp = copy.deepcopy(self)
                self.parent.parent.parent.data = temp.data
                self.parent.parent.parent.children = temp.children
            if(other.data == 'EXPRESSION'):
                #print(self.data)
                if(self.data == 'input'):
                    self.parent.parent.data = 'eval(input())'
                    self.parent.parent.children = []
            if(other.data == 'function'):
                    #print('were in the function',self.data)
                    temp = copy.deepcopy(self)
                    self.parent.parent.data = temp.data
                    self.parent.parent.children = self.parent.parent.children[1:]
                    #print([child.data for child in self.parent.parent.children])
                    child = [child.data if (not child.data in ['TEMP','CONST']) else child.children[0].data for child in self.parent.parent.children]
                    #print(len(child), child)
                    params = '('
                    #print(params)
                    if(len(child)>1):
                        #print(child)
                        childs = child[:-1]
                        for kid in childs:
                            params+=kid+', '
                        params+=child[-1]+')'
                    elif(len(child)==1):
                        params+= child[0]+')'
                    else:
                        params+= ')'                    
                    self.parent.parent.data+=params
                    self.parent.parent.children = []
            return True
        
        if(self.data == other.data):
            #if(len(self.children) == len(other.children)):
            for i in range(len(self.children)):
                try:
                    ans = ans and self.children[i].structure(other.children[i])
                except:
                    return ans
            return ans
            #else:
                #print('mismatched kids')
                
        elif (len(self.children)>0):
            for child in self.children:
                child.structure(other)
            #print('mistmatched data')
        else:
            return False
        
    def __init__(self,data, level):
        self.data = data
        self.level = level
        self.children = []

    def add(self,node):
        self.children.append(node)

    def get(self, i=0):
        print(i*"="+self.data)
        for child in self.children:
            child.get(i+1)

    def fold(self):
        ans = []
        if self.data:
            ans = [self.data]
            if self.data == 'TEMP' or self.data == 'CONST':
                val = 'CONST '
                if self.data == 'TEMP':
                    val = 'TEMP '
                val += self.children[0].data
                return val
            for child in self.children:
                ans += [child.fold()]
        return ans

class Tree:
    def __init__(self):
        self.root = None
        self.stack = Stack()
        #self.stack2 = Stack()
    def insert(self, data, level):
        if self.root == None:
            self.root = Node(data, level)
            self.stack.push(self.root)
            #self.stack2.push(self.root.data)

        else:
            node = Node(data, level)
            temp = self.stack.peek()
            if(level > temp.level):
                self.stack.push(node)
                #self.stack2.push([node.data])
            else:
                
                while(self.stack.peek().level >= level and self.stack.size()>1):
                    curr = self.stack.pop()
                    #curr2 = self.stack2.pop()
                    curr.parent = self.stack.items[-1]
                    self.stack.items[-1].children.append(curr)
                    #print(self.stack2.items,curr2)
                    #print(curr.level, self.stack.items[-1].level)
                    #try:
                    #    self.stack2.items[-1].append(curr2)
                    #except:
                    #    self.stack2.items.append(curr2)
                self.stack.push(node)
                #self.stack2.push([node.data])

    def fold(self):
        ans = []
        if self.root:
            ans.append(self.root.data)
            temp = self.root
            for child in temp.children:
                #print(child.data)
                ans.append(child.fold())
        for i in ans:
            #print((var_x) in str(i))
            line = str(i)
            line = findVar(line)
            #print(line)

    def get(self):
        return self.root.get(0)

    def structure(self, other):
        return self.root.structure(other.root)

class Stack:
    items = []
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(items)==0
    
    def push(self,node):
        self.items.append(node)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)

def readTile(tile):
    tiletree = Tree()
    tile = tile.split('\n')
    for line in tile:
        level = line.count('=')
        data = line[level:]
        tiletree.insert(data, level)
    tiletree.insert("end", 0)
    return tiletree


def munch(tree):
    #first we do var, then ops, then input, then moves,  then functions
    findVar(tree)
    findOps(tree)
    findInput(tree)
    findMove(tree)
    findFunc(tree)

def findVar(tree):
    for tile in tiles['var_x']:
        tree1 = readTile(tile)
        tree.structure(tree1)

    
def findInput(tree):
    tree1 = readTile(tiles['input'])
    tree.structure(tree1)
    #tree.get()

def findMove(tree):
    tree1 = readTile(tiles['var_xe'])
    tree.structure(tree1)

def findOps(tree):
    for tile in tiles['ops']:
        tree1 = readTile(tile)
        tree.structure(tree1)

def findFunc(tree):
    #print('finding nemo\n========================')
    tree1 = readTile(tiles['func'])
    tree.structure(tree1)

def findConst(tree):
    #print('finding nemo\n========================')
    tree1 = readTile(tiles['const'])
    tree.structure(tree1)
    
def main():
    tree = Tree()
    loop = Tree()
    arr = []

    loopFile = "loop.lp"
    file ="testdata4.ir"
    #file = sys.argv[1]

    #readLoop(loopstring, loop)
    #readFile(loopFile, loop)
    read(file, tree, loop)
    munch(tree)
    #tree.get()
    if tree.root.data == 'SEQ':
        for child in tree.root.children:
            print(child.data)
if __name__ == "__main__":
    main()
