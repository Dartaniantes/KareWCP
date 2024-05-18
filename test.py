import translator as tr
import pyperclip as clip

text = "A pachyderm side table, not just for animal lovers - Our Elefant side "\
       "table, a not-entirely-serious creation inspired by a comic figure, performs a useful function.\n"\
       "A crazy eyecatcher in the shape of an elephant. More loyal than any real four-legged friend.\n"\
       "An original table which will put a smile on the face of everyone who sees it. With its practical\n"\
       "top our elephant is actually a flyweight, but with its fighting weight of 6 kg it still puts in a\n"\
       "robust performance. A great eyecatcher for the bar, the living room or anywhere else you decide to\n"\
       "put it. Material: polyresin."


'''
print(tr.get_rus(text))
print()
print(tr.get_ukr(text))
'''
#print(tr.detect("some text in english: Інформація про товар:"))
print(tr.detect('hello'))

# products = 300
# print(1400*products/1000000 * 20)
# print(8.4/300)

