# War simulation
The idea behind this project is to code a war simulation in Python (Jupyter Notebook). This project was developed in the beginning of 2022, during the same time Russia decided to invade Ukraine. Therefore, the choice of Ukraine as the focus for this simulation became kind of obvious.

The goal of this simulation is to see, by fixing two constraints :
- Number of soldiers
- Number of days
the turnout of the war. 

It's a really simple simulation that doesn't have for goal to depict the real war happening in Ukraine. In this simulation, we'll only focus on the attacker and the constraints it has to respect. If the day-limit is reached and the attacker didn't succeed in taking Kyiv, the war is lost. The war is also lost if the attacker has no more soldiers. Indeed, in this simulation, we'll only focus on 27 main cyties, each city representing a region of the country:
- Cherkasy, Chernihiv, Chernivtsi, Crimea, Dnipropetrovs'k, Donets'k, Ivano-Frankisv'k, Kharkiv, Kherson, Khmel'nyts'kyy, Kyiv City, Kyiv, Kirovohrad,  
L'viv, Luhans'k, Mykolayiv, Odessa, Poltava, Rivne, Sevastopol', Sumy, Ternopil', Transcarpathia, Vinnytsya, Volyn, Zaporizhzhya, Zhytomyr

The map of Ukraine will be divided in 3 danger zones:
- Zone 1 : Luhans'k, Sumy, Kharkiv, Donets'k, Zaporizhzhya, Crimea, Sevastopol', Kherson, Mykolayiv, Odessa, Chernivtsi, Ivano-Frankisv'k, Transcarpathia, Volyn, L'viv
- Zone 2 : Dnipropetrovs'k, Poltava, Kirovohrad, Vinnytsya, Ternopil', Khmel'nyts'kyy, Rivne, Cherkasy
- Zone 3 : Kyiv, Kyiv City, Chernihiv, Zhytomir

Each danger zone has an impact on the enemy's army. If the adversary's army battle through a Zone 1 region, it will suffer a loss of 15% of its soldiers and it will take 10 days to conquer. If it goes through a Zone 2 region, it will be a loss of 25% of its soldiers and a 25 days siege to conquer it. Finally, a loss of 50% of its soldiers will be inflicted in a Zone 3 region and the siege will take 50 days.

The choice of Ukraine for this simulation imply that the attacker is Russia. Therefore, for realistic purposes, the attacker can only attack from the east of Ukraine (not allowed to attack from Belarus). The goal of this program is to choose the route taken by the enemy automatically. When a region has been conquered, the next one is chosen among the neighboring regions automatically, but not randomly. The decision is taken depending on the difficulty to conquer of each neighboring regions.

In the end, a GIF image is created to depict the outcome of the war. The creation of the map wasn't done by me. I found the code on github but I no longer have the github profile of the person who coded it (but thanks a lot !).

The libraries used are :
- Numpy
- Pandas
- Shapefile
- Matplotlib
- Seaborn

The python file of the simulation is available but I used Jupyter notebook to run the program. To run the program, the folder 'UKR_adm1' and a folder named 'Maps_invasion' (the one attached can be used) must be in the same directory of the file containing the code.

ENJOY ! 

PS : some simulations are available in the folder "Maps_invasion". 
