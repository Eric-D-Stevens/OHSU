
# coding: utf-8

# ## Question 3

# In[1]:


list1 = [1, 2, "c", 4, "e"]
list2 = [6, "g", 7, "i", "j"]


# In[2]:


print("list1: ", list1)
print("list2: ", list2)


# In[5]:


list3 = list1 + list2
print(list3)


# In[4]:


list4 = [list1,list2]
print(list4)


# In[5]:


list1.append("x")
print(list1)


# In[6]:


list1.extend(list2)
print(list1)


# In[7]:


list1 = [1, 2, "c", 4, "e"]
print(list1[0])
print(list1[3])
print(list1[-1])


# In[9]:


print(list1[1:3])
print(list1[:])
print(list1[2:])
print(list1[-3:-1])


# In[10]:


print(list1[2:3])
print(list1[2])


# In the code above the first line returns a slice of list1 with a range of one index. The second line returns the value at a single index of the list.

# In[11]:


list1 = [1, 2, "c", 4, "e"]
list2 = list1
list1.append("x")
print(list2)


# In this statement, setting list2 equal to list1 is not actually creating a new list variable and copying data over from list one but rather creating a list pointer object that points to the same object that list one points to.

# In[13]:


list1 = [1, 2, "c", 4, "e"]
list2 = list1
list1 = list1 + [6]
print(list1)
print(list2)


# In this situation you are setting list1 equal to itself and another list. This requires the creation of a new object. List two is still pointing to the first object.

# In[6]:


list1 = [1, 2, "c", 4, "e"]
list2 = list1[:]
list1.append("x")
print(list1)
print(list2)


# Here we are setting list2 equal to the values within list1 as opposed to list1 itself. In this situation a new object is created and pointed to by list2.

# ## Question 4

# In[10]:


def parse(atom):
    for x in range(1,len(atom)):
        if atom[x][0].islower():
            print("constant ", atom[x])
        else:
            print("variable ", atom[x])


# In[11]:


myatom = ["pred", "foyer", "X", "foyer", "parlour", "Y", "X"]
parse(myatom)


# ## Question 5

# In[23]:

print("\n\n")

def parse(atom):
    d={}
    for x in range(1,len(atom)):
        if atom[x][0].islower():
            d[atom[x]] = "constant "
        else:
            d[atom[x]] = "variable "
    for i in d:
        print ( d[i], i)


# In[24]:


myatom = ["pred", "foyer", "X", "foyer", "parlour", "Y", "X"]
parse(myatom)

