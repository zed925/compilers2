#!/usr/bin/python
import copy
import sys

def read(file, tree, loop):
    
    ifile = open(file)
    currLevel = -1
    for line in ifile:
        level = line.count('=')
        data = line[level:][:-1]
        #print((' '*level)+data, level)
        tree.insert(data, level)
    tree.insert("end", 0)
    for i in tree.stack2.items:
        print(i)

    #tree.get()
    


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
    level = 0
    children = []
    
    def equals(self, other):
        ans = True
        if(self.data == other.data):
            if not self.level == other.level:
                #print('levels dont match')
                return False
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


class Tree:
    def __init__(self):
        self.root = None
        self.stack = Stack()
        self.stack2 = Stack()
    def insert(self, data, level):
        if self.root == None:
            self.root = Node(data, level)
            self.stack.push(self.root)
            self.stack2.push(self.root.data)

        else:
            node = Node(data, level)
            temp = self.stack.peek()
            if(level > temp.level):
                self.stack.push(node)
                self.stack2.push([node.data])
            else:
                
                while(self.stack.peek().level >= level and self.stack.size()>1):
                    curr = self.stack.pop()
                    curr2 = self.stack2.pop()
                    self.stack.items[-1].children.append(curr)
                    print(self.stack2.items,curr2)
                    print(curr.level, self.stack.items[-1].level)
                    try:
                        self.stack2.items[-1].append(curr2)
                    except:
                        self.stack2.items.append(curr2)
                self.stack.push(node)
                self.stack2.push([node.data])
           

    def get(self):
        return self.root.get(0)



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
def main():
    tree = Tree()
    loop = Tree()
    arr = []
    loopstring="""SEQ
=SEQ
==SEQ
===SEQ
====SEQ
=====SEQ
======SEQ
=======SEQ
========MOVE
=========TEMP
==========t1
=========CONST
==========4
========MOVE
=========TEMP
==========t2
=========CONST
==========6
=======LABEL
========start
======CJUMP
=======<
=======TEMP
========t2
=======TEMP
========t1
=======NAME
========t12
=======NAME
========f12
=====LABEL
======f12
====BODY
===MOVE
====TEMP
=====t1
====+
=====TEMP
======t1
=====CONST
======1
==JUMP
===NAME
====start
=LABEL
==t12"""
    loopFile = "loop.lp"
    file ="testdata7.ir"
    #file = sys.argv[1]

    #readLoop(loopstring, loop)
    #readFile(loopFile, loop)
    read(file, tree, loop)

main()
