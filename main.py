#!/usr/bin/python
import copy
import sys
from jouette import tiles
var_x = "['MEM', ['+', 'TEMP FP', 'CONST "

def read(file, tree, loop):
    
    ifile = open(file)
    currLevel = -1
    for line in ifile:
        level = line.count('=')
        data = line[level:][:-1]
        #print((' '*level)+data, level)
        tree.insert(data, level)
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
            self.data ='('+self.children[0].data +' = '+self.children[1].data+')'
            self.children = []
            return True    
        if(other.data == "VARIABLE" or other.data == "EXPRESSION" or other.data == 'input'):
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
           
            return True
        if(self.data == other.data):
            if(len(self.children) == len(other.children)):
                for i in range(len(self.children)):
                    ans = ans and self.children[i].structure(other.children[i])
                #print('all good')
                return ans
            else:
                #print('mismatched kids')
                return False
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

    def get(self, i):
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



def findVar(tree):
    tree1 = readTile(tiles['var_x'][1])
    tree2 = readTile(tiles['var_x'][0])

    #tree1.get()
    #tree2.get()
    if(tree.structure(tree1)):
        print("FOUND")
    elif(tree.structure(tree2)):
        print("FOUND IN 2")
    #    tree.get()
    else:
        print("NOT FOUND")
    
def findInput(tree):
    tree1 = readTile(tiles['input'])
    tree.structure(tree1)
    #tree.get()

def findMove(tree):
    tree1 = readTile(tiles['var_xe'])
    tree.structure(tree1)
def main():
    tree = Tree()
    loop = Tree()
    arr = []

    loopFile = "loop.lp"
    file ="test.ir"
    #file = sys.argv[1]

    #readLoop(loopstring, loop)
    #readFile(loopFile, loop)
    read(file, tree, loop)
    findVar(tree)
    findInput(tree)
    findMove(tree)
    tree.get()
if __name__ == "__main__":
    main()
