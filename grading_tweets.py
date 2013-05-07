'''
Created on Apr 27, 2013

@author: ted
'''
from sys import stdout
import subprocess
import re
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

def mean_center(field, columns, lines, config):
        f_out = open(config['data_dir']+config['grading_tweets_meancenter'], 'w')
        f_out.write('clean_text,language_code,latitude,longitude,user_id,kincaid,flesch_index,flesch_index_mc,lix_score,lix_school\n')

        flesch_total = 0.0
        flesch_count = 0.0
        for line in lines:
                split_line = line.split(',')
                flesch_total += float(split_line[columns['flesch_index']])
                flesch_count += 1.0

        flesch_mean = (flesch_total/flesch_count)
        
        for line in lines:
                split_line = line.split(',')
                     
                clean_text = split_line[columns['clean_text']].strip()
                language_code = split_line[columns['language_code']]
                latitude = split_line[columns['latitude']]
                longitude = split_line[columns['longitude']]
                user_id = split_line[columns['user_id']]
                kincaid = split_line[columns['kincaid']]
                flesch_index = split_line[columns['flesch_index']]
                flesch_index_mc = float(flesch_index) - flesch_mean
                lix_score = split_line[columns['lix_score']]
                lix_school = split_line[columns['lix_school']]
                
                line_out = clean_text+','+language_code+','+latitude+','+longitude+','+user_id+','+str(kincaid)+','+str(flesch_index)+','+str(flesch_index_mc)+','+str(lix_score)+','+str(lix_school)+'\n'
                f_out.write(line_out)
                        
        f_out.close()
        
def parse_grade(columns, lines, config):

        f_out = open(config['data_dir']+config['grading_tweets'], 'w')
        f_out.write('clean_text,language_code,latitude,longitude,user_id,kincaid,flesch_index,lix_score,lix_school\n')

        total = len(lines)
        count = 0
        
        for line in lines:
                split_line = line.split(',')
                     
                clean_text = split_line[columns['clean_text']].strip()
                language_code = split_line[columns['language_code']]
                latitude = split_line[columns['latitude']]
                longitude = split_line[columns['longitude']]
                user_id = split_line[columns['user_id']]
                     
                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', clean_text)
                if urls:
                        for url in urls:
                                clean_text = clean_text.replace(url, '')
                users = re.findall('@([A-Za-z0-9_]+)', clean_text)
                if users:
                        for user in users:
                                clean_text = clean_text.replace('@'+str(user), '')
                hashes = re.findall('#([A-Za-z0-9_]+)', clean_text)
                if hashes:
                        for h in hashes:
                                clean_text = clean_text.replace('#'+str(h), '') 
                
                clean_text = clean_text.replace('.', '')+'.'
                 
                tmp = open(config['data_dir']+'tmp.txt', 'w')
                tmp.write(clean_text)
                tmp.close()

                p1 = subprocess.Popen(['style', config['data_dir']+'tmp.txt'], stdout=subprocess.PIPE)
                out, err = p1.communicate()
                
                kincaid = 0.0
                flesch_index = 0.0
                lix_score = 0.0
                lix_school = ''
                style_out = out.split('\n')
                for l in style_out:
                        if l.find('Kincaid:') != -1:
                                kincaid = float(l.split(':')[1].strip())
                        elif l.find('Flesch Index:') != -1:
                                flesch_index = float(l.split(':')[1].split('/')[0].strip())
                        elif l.find('Lix:') != -1:
                                lix_score = float(l.split(':')[1].strip().split('=')[0])
                                lix_school = l.split(':')[1].strip().split('=')[1].strip()
                                if lix_school == 'below school year 5':
                                        lix_school = 4
                                elif lix_school == 'school year 5':
                                        lix_school = 5
                                elif lix_school == 'school year 6':
                                        lix_school = 6
                                elif lix_school == 'school year 7':
                                        lix_school = 7
                                elif lix_school == 'school year 8':
                                        lix_school = 8
                                elif lix_school == 'school year 9':
                                        lix_school = 9
                                elif lix_school == 'school year 10':
                                        lix_school = 10
                                elif lix_school == 'school year 11':
                                        lix_school = 11
                                elif lix_school == 'higher than school year 11':
                                        lix_school = 12
                                else:
                                        lix_school = 0

                if flesch_index > 0 and flesch_index <= 100:  
                        line_out = clean_text+','+language_code+','+latitude+','+longitude+','+user_id+','+str(kincaid)+','+str(flesch_index)+','+str(lix_score)+','+str(lix_school)+'\n'
                        f_out.write(line_out)
                
                count += 1
                print '{0}\r'.format([count, total]),
                        
        f_out.close()

if __name__ == '__main__':
	cwd = os.getcwd()
        config = {}
        config['data_dir'] = cwd+'/data/'
        config['input_csv'] = config['data_dir']+'twitter_points_usa_10-23-2012-to-11-06-2012.csv'
        config['grading_tweets'] = 'grading_tweets.csv'
        config['grading_tweets_meancenter'] = 'grading_tweets_meancenter.csv'
        
        lines = csv2linelists(config['input_csv'])
        
        #clean_text,language_code,latitude,location_txt,longitude,row_id,sort_field,start_date,start_time,tweet_id,user_id
        header = lines.pop(0)
        columns = indexFromCSV(header)
        
        parse_grade(columns, lines, config)
        
        lines = csv2linelists(config['data_dir']+config['grading_tweets'])
        header = lines.pop(0)
        columns = indexFromCSV(header)
        
        mean_center(columns['flesch_index'], columns, lines, config)
