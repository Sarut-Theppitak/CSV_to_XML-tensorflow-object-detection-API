# 2020/09/04
# Created by Sarut Theppitak

import os
import pandas as pd
import numpy as np
from lxml import etree
import xml.etree.ElementTree as ET
import argparse
pd.set_option('display.max_columns', 25)
pd.set_option('display.max_rows', 15)

#--csv_path=C:\Users\3978\Desktop\Faster-Rcnn\inceptionV2_ais_s1_20200826\data\test.csv
##specify the img folder information which will be writen in the xml file
#--img_folder=eval_img 
#output_folder=C:\Users\3978\Desktop\Faster-Rcnn\inceptionV2_ais_s1_20200826\data\convert_xml

# we can pass the argument without '' because the program already notice that this will be tring

def main(csv_path,img_folder,output_folder):

    fields = ['filename', 'xmin', 'ymin', 'xmax', 'ymax', 'class', 'x', 'y']
    df = pd.read_csv(csv_path, usecols=fields)
    
#    num_img = df['filename'].nunique()
    
    for img_name in pd.unique(df['filename']):
        
        sub_df = df[df['filename'] == img_name]
        
        #the hight and width information will be extract from the first entry of its file_name
        height = df['y'].iloc[0]
        width = df['x'].iloc[0]
        #specify the num of chanel of you image 
        depth = 1
    
        annotation = ET.Element('annotation')
        ET.SubElement(annotation, 'folder').text = img_folder.split('\\')[-1]
        ET.SubElement(annotation, 'filename').text = img_name
        ET.SubElement(annotation, 'path').text = os.path.join(img_folder,img_name)
        source = ET.SubElement(annotation, 'source')
        ET.SubElement(source, 'database').text = 'Unknown'
        size = ET.SubElement(annotation, 'size')
        ET.SubElement(size, 'width').text = str(width)
        ET.SubElement(size, 'height').text = str(height)
        ET.SubElement(size, 'depth').text = str(depth)
        ET.SubElement(annotation, 'segmented').text = '0'
        
        obs = {}
        bbox_obs = {}
        for i in range(len(sub_df)):
            
            obs['ob'+ str(i)] = ET.SubElement(annotation, 'object')
            ET.SubElement(obs['ob'+ str(i)], 'name').text = sub_df['class'].iloc[i]
            ET.SubElement(obs['ob'+ str(i)], 'pose').text = 'Unspecified'
            ET.SubElement(obs['ob'+ str(i)], 'truncated').text = '0'
            ET.SubElement(obs['ob'+ str(i)], 'difficult').text = '0'
            bbox_obs['ob'+ str(i)] = ET.SubElement(obs['ob'+ str(i)], 'bndbox')
            ET.SubElement(bbox_obs['ob'+ str(i)], 'xmin').text = str(sub_df['xmin'].iloc[i])
            ET.SubElement(bbox_obs['ob'+ str(i)], 'ymin').text = str(sub_df['ymin'].iloc[i])
            ET.SubElement(bbox_obs['ob'+ str(i)], 'xmax').text = str(sub_df['xmax'].iloc[i])
            ET.SubElement(bbox_obs['ob'+ str(i)], 'ymax').text = str(sub_df['ymax'].iloc[i])
        
        
        img_name_xml = img_name.replace('.png','.xml')
        final_xml_path = os.path.join(output_folder,img_name_xml)
        
        tree = ET.ElementTree(annotation)
        tree.write(final_xml_path, encoding='utf8')
        
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= 'Create xml files from CSV file')
    parser.add_argument('--csv_path', type= str,required = True, help = 'Specify your csv path with .csv extention')
    parser.add_argument('--img_folder', type= str,required = True, help = 'Specify your last folder name. This will not effect to the data')
    parser.add_argument('--output_folder', type= str,required = True, help = 'Specify your output folder')
    args = parser.parse_args()
    main(args.csv_path,args.img_folder,args.output_folder)

    
    
    
    
    
    