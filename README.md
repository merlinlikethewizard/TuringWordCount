# Frequency.py
I took a class in college in which we were assingned the task of writing a very simple program
to count and sort the occurances of each word it a text document. The caveat was, we had to choose
a interesting programming language to do it in, one we hadn't coded in before. Here is the
description of the assignment:


>Given a text file, display its 25 most frequent words and the number of times each occurs. Convert all words to lowercase, ignore punctuation, and don't do common "stop words", which are specified in stop_words.txt.
>For example, if the file is named input.txt and contains
>
>```
>White tigers live mostly in India
>Wild lions live mostly in Africa
>```
>
>and the python program is frequency.py , then running
>
>```
>$ python frequency.py input.txt
>```
>
>should produce
>
>```
>live - 2 
>mostly - 2 
>africa - 1 
>india - 1 
>lions - 1 
>tigers - 1 
>white - 1 
>wild - 1
>```
>
>Stop Words:
>```
>a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,
>at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,
>else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,
>however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,
>might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,
>our,own,rather,said,say,says,she,should,since,so,some,than,that,the,
>their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,
>were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,
>your
>```

So I wrote a turing machine! Okay, technically I used python to generate the turing "code,"
but I still count it. The resulting program has more than 20k instructions and is not fast.
But it basically works!

```
$ python frequency.py input.txt
eat - 12
ate - 6
ite - 6
ote - 6
ute - 6
apples - 2
bananas - 2
epples - 2
benenes - 2
eepples - 2
beeneenees - 2
ipples - 2
bininis - 2
oplles - 2
bononos - 2
upples - 2
bununus - 2
```
