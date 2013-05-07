'''
Created on May 2, 2013

@author: ted
'''

import operator
import os

def csv2linelists(filename):
        print filename
        f = open(filename, 'r')
        lines = f.readlines()
        clean = []
        for line in lines:
                if line.strip() == '':
                        pass
                else:
                        clean.append(line.strip())
        f.close()
        return clean

def indexFromCSV(columns):
        columns_split = columns.split(",")
        columns_index = {}
        for column_index in range(0, len(columns_split)):
                columns_index[columns_split[column_index].strip()] = column_index
        return columns_index

def reducer(lines):
        word_count = {}
        reducer_output = open(config['data_dir']+'wordcount.csv', 'a')
        char_count = 0
        for line in lines:
                line = line.split(',')[0]
                line = line.lower()
                char_strip = '!,@,#,$,%,^,&,*,(,),-,_,?,>,<,[,],~,|,/,.,:,;'.split(',')
                word_strip = 'a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your'.split(',')

                for c in char_strip:
                        line = line.replace(c, ' ')
                for w in word_strip:
                        line = line.replace(w, '')
                
                words = line.split(' ')
                
                for word in words:
                        word = word.strip()
                        if len(word) >= 3:
                                char_count += len(word)
                                if word in word_count:
                                        word_count[word] += 1
                                else:
                                        word_count[word] = 1
                
        sorted_wordcount = sorted(word_count.iteritems(), key=operator.itemgetter(1))
        print sorted_wordcount.__class__

        for x in sorted_wordcount:
                print x[0]+'\t'+str(x[1])
                if x[1] == 1:
                        pass
                else:
                        reducer_output.write(x[0]+'\t'+str(x[1])+'\n')
                        
        reducer_output.close()
                
if __name__ == '__main__':
	cwd = os.getcwd()
        config = {}
        config['data_dir'] = cwd+'/data/'
        config['grading_tweets_meancenter'] = 'grading_tweets_meancenter.csv'
        
        lines = csv2linelists(config['data_dir']+config['grading_tweets_meancenter'])
        
        header = lines.pop(0)
        columns = indexFromCSV(header)
        
        reducer(lines)
