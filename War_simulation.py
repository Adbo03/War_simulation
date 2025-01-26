import random
import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt 
import seaborn as sns
import glob
import os
import csv
from PIL import Image

# -------------------------------------------- MAP CODE -------------------------------------------- #
sns.set(style="whitegrid",palette='bright',color_codes=True) 
sns.mpl.rc("figure", figsize=(10,6))
shp_path="UKR_adm1/UKR_adm1.shp"
sf=shp.Reader(shp_path)
len(sf.shapes())
sf.records()

def read_shapefile(sf):
    fields = [x[0] for x in sf.fields][1:]
    records = [list(i) for i in sf.records()]
    shps = [s.points for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    return df

df=read_shapefile(sf)



def plot_map_fill_multiples_ids(title, city, sf,progress,day,x_lim = None,y_lim = None, figsize = (9,7)):    
    plt.figure(figsize = figsize)
    fig, ax = plt.subplots(figsize = figsize)
    ax.axis('off')
    fig.suptitle(title, fontsize=16)
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        ax.plot(x, y, 'k')
            
    for i in range(len(city)):
        shape_ex = sf.shape(city[i])
        x_lon = np.zeros((len(shape_ex.points),1))
        y_lat = np.zeros((len(shape_ex.points),1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        
        # PART ADDED : To display the winner of the war and the progress of the invasion
        if title=='RUSSIA VICTORY':
            if i in {24,18,26,11,10,1,20,7,14}:
                ax.fill(x_lon,y_lat, 'w')
            elif i in {13,21,9,23,0,17,4,5,12}:
                ax.fill(x_lon,y_lat,'b')
            else:
                ax.fill(x_lon,y_lat,'r')
                
        elif title=='UKRAINE VICTORY':
            if i in {22,6,2,23,0,12,4,5,25,3,19,8,15,16}:
                ax.fill(x_lon,y_lat, 'y')
            else:
                ax.fill(x_lon,y_lat,'b')
            
        elif progress[i]<0.5 :
            ax.fill(x_lon,y_lat, 'y')
        
        elif progress[i]==1:
            ax.fill(x_lon,y_lat, 'r')
        
        elif 1>progress[i]>=0.5:
            ax.fill(x_lon,y_lat, 'tab:orange')

        # ------------------------------------------------------- #
             
        x0 = np.mean(x_lon)
        y0 = np.mean(y_lat)
        plt.text(x0, y0, df.NAME_1[city[i]], fontsize=10)
    
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)
    
    fig.savefig('Maps_invasion/'+'Day '+str(day)+'.png')
    plt.close('all')
    
    return None
    

# ------------------------------------------- SIMULATION CODE ------------------------------------------- #
indices_map={"Cherkasy":0,"Chernihiv":1,"Chernivtsi":2,"Crimea":3,"Dnipropetrovs'k":4,"Donets'k":5,"Ivano-Frankisv'k":6,
             "Kharkiv":7,"Kherson":8,"Khmel'nyts'kyy":9,"Kiev City":10,"Kiev":11,"Kirovohrad":12,
             "L'viv":13,"Luhans'k":14,"Mykolayiv":15,"Odessa":16,"Poltava":17,"Rivne":18,"Sevastopol'":19,
             "Sumy":20,"Ternopil'":21,"Transcarpathia":22,"Vinnytsya":23,"Volyn":24,"Zaporizhzhya":25,
             "Zhytomyr":26}

Regions ={"Cherkasy":0,"Chernihiv":1,"Chernivtsi":2,"Crimea":3,"Dnipropetrovs'k":4,"Donets'k":5,"Ivano-Frankisv'k":6,
        "Kharkiv":7,"Kherson":8,"Khmel'nyts'kyy":9,"Kiev":10,"Kirovohrad":11,
        "L'viv":12,"Luhans'k":13,"Mykolayiv":14,"Odessa":15,"Poltava":16,"Rivne":17,"Sevastopol'":18,
        "Sumy":19,"Ternopil'":20,"Transcarpathia":21,"Vinnytsya":22,"Volyn":23,"Zaporizhzhya":24,
        "Zhytomyr":25,"Kiev City":26}

options=[['Kiev','Vinnytsya'],['Kiev'],["Ternopil'","Khmel'nyts'kyy",'Vinnytsya']
         ,['Kherson'],['Poltava','Kirovohrad','Mykolayiv'],["Dnipropetrovs'k",'Zaporizhzhya'],['Chernivtsi',"Ternopil'"]
         ,['Poltava',"Dnipropetrovs'k"],["Dnipropetrovs'k",'Mykolayiv'],['Vinnytsya','Zhytomyr'],['Kiev City'],['Cherkasy','Poltava','Vinnytsya']
         ,['Rivne',"Ternopil'"],["Donets'k"],['Odessa','Kirovohrad'],['Vinnytsya','Kirovohrad'],['Chernihiv','Kiev','Cherkasy']
         ,['Zhytomyr',"Khmel'nyts'kyy"],['Crimea'],["Chernihiv","Poltava"],["Rivne","Khmel'nyts'kyy"],["L'viv","Ivano-Frankisv'k"]
         ,['Kiev','Zhytomyr'],['Rivne'],["Dnipropetrovs'k","Kherson"],['Kiev']]

zone1 = {"Luhans'k",'Sumy','Kharkiv',"Donets'k",'Zaporizhzhya','Crimea',"Sevastopol'",'Kherson','Mykolayiv','Odessa','Chernivtsi'
         ,"Ivano-Frankisv'k",'Transcarpathia','Volyn',"L'viv"}
zone2 = {"Dnipropetrovs'k",'Poltava','Kirovohrad','Vinnytsya',"Ternopil'","Khmel'nyts'kyy",'Rivne','Cherkasy'}
zone3 = {'Kiev','Kiev City','Chernihiv','Zhytomir'}

def simulation(soldiers,duration): 
    soldiers = [soldiers]
    duration = [duration]
    K=random.random()
    L=random.random()
    S=random.random()
    days=[]
    cities=[]
    percentages=[]
    city=''
    inv_dico=dict()
    envaded=[]
    j=0
    d=1

    # SIMULATION LOOP
    while j<duration[0] and soldiers[len(soldiers)-1]>0 and city!='Kiev City':
        p=1
        if inv_dico==dict():
            lim=10
            m=0
            i=0

            # Random choice of the first region to invade : Kharkiv, Sumy or Luhans'k
            for i in [K,L,S]:
                if i >= m:
                    m=i
                    
            if m==K:
                city='Kharkiv'

            elif m==L:
                city="Luhans'k"

            elif m==S:
                city='Sumy'

            soldiers.append(soldiers[len(soldiers)-1]-int((15/100)*soldiers[len(soldiers)-1]))
            duration.append(duration[len(duration)-1]-lim)
            
            
        else:
            if city!='Kiev City':
                r=int(random.random()*len(options[Regions[city]]))            
                city=options[Regions[city]][r]
                

                if city in zone1 :
                    lim=10
                    soldiers.append(soldiers[len(soldiers)-1]-int((15/100)*soldiers[len(soldiers)-1]))
                    duration.append(duration[len(duration)-1]-lim)
                    
                    
                elif city in zone2 :
                    lim=25
                    soldiers.append(soldiers[len(soldiers)-1]-int((25/100)*soldiers[len(soldiers)-1]))
                    duration.append(duration[len(duration)-1]-lim)
                    
                elif city in zone3 :
                    lim=50
                    soldiers.append(soldiers[len(soldiers)-1]-int((50/100)*soldiers[len(soldiers)-1]))
                    duration.append(duration[len(duration)-1]-lim)
                    
        while p<=lim and j!=duration[0]:
            inv_dico[city]=p/lim
            envaded.append([(v,inv_dico[v]) for v in inv_dico])
            p+=1
            j+=1
        

    for l in envaded:
        for (c,a) in l:
            days.append(d)
            cities.append(c)
            percentages.append(a)
            
        d+=1
    
    tab=[]
    for (d,c,a) in zip(days,cities,percentages):
        tab.append([d,c,a])
    
    towns={t for t in cities}
    
    for x in Regions:
        if x not in towns:
            tab.append([0,x,0])
        
        
        
    titles=['Days', 'Cities', 'Progress']
    
    with open('invasion_sumup','w') as f:
        write=csv.writer(f)
        write.writerow(titles)
        write.writerows(tab)
    
    data=pd.read_csv('invasion_sumup')

    for day in range(1,j+1):
        w = data[data['Days']==day]
        ciudades = w['Cities']
        ids = [indices_map[z] for z in ciudades]
        progress = [e for e in w['Progress']]
        plot_map_fill_multiples_ids('Day '+str(day), ids,sf,progress,day,x_lim = None,y_lim = None, figsize = (9,7))
    
    # If Kyiv is reached and fully conquered, the war is won
    if cities[len(cities)-1] == 'Kiev City' and percentages[len(percentages)-1] == 1:
        plot_map_fill_multiples_ids('RUSSIA VICTORY',[indices_map[c] for c in indices_map],sf,[],j+1,x_lim = None,y_lim = None, figsize = (9,7))

    # Otherwise, it is lost
    else:
        plot_map_fill_multiples_ids('UKRAINE VICTORY',[indices_map[c] for c in indices_map],sf,[],j+1,x_lim = None,y_lim = None, figsize = (9,7))


    # Creation of the images and the GIF image of the war
    frames = []
    imgs=[]
    for y in range(1,j+2):
        path="Maps_invasion/Day "+str(y)+".png"
        imgs.append(path)
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    frames[0].save('Maps_invasion/Invasion_'+str(soldiers[0])+'_'+str(duration[0])+'.gif', format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=325,optimize=False, loop=1)
    
    # Destruction of the images used to create the GIF (no longer needed)
    for t in range(1,j+2):
                os.remove("Maps_invasion/Day "+str(t)+".png")
    
    return None
