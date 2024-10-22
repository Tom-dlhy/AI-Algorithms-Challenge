# AI-Algorithms-Challenge


### DEADLINE :  
- The deadline for submitting your notebook is Friday, December 13th
- The deadline to complete this file and finalize your teams is November 10th : [Lien du forms](https://devinci-my.sharepoint.com/personal/farah_ait_salaht_devinci_fr/_layouts/15/guestaccess.aspx?share=EZdFUA_tCwxPln2I6hc5lsoBlhwFgfvxdLYLHvs2hVZjPA&e=Mya4tS)

### Modélisation :

--> Goal state : pâte remplie avec le profit maximum (profit des biscuits - perte)

--> Approche : discretizer en case (exemple 500 cases de 1 unité de x avec donc un certain nombre de defects par case) et on augmente les bins au fur et à mesure pour gagner en précision (et en temps mdrr)

--> Deux axes de progressios : - Pour un même nombre de bins on va trouver une solution optimale (coût minimum peut-être pas le même chemin mais coût minimum quand même) et l'axe d'optimisation c'est l'algo le plus rapide pour trouver la solution 

                               - Une fois l'algo le plus rapide trouver, on augmente le nombre de bins pour gagner en précision et on va forcément mettre plus de temps à résoudre d'où le fait de trouver le meilleur algo avant. 
                                 Les deux axes sont donc vitesse et minimisation du coût.
--> Question : Comment gérer le fait de laisser un blanc et de pas mettre un biscuit pck il est plus smart de ne pas mettre un biscuit pour éviter une anomalie ? Idée : inventer le biscuit vide (quelle longueur il a ?)

--> Le set d'action : {Placer le biscuit 0,1,2,3 ou le biscuit -1,-2,-3,-4,-5,-6,-7 (qui correspondent aux biscuits vides de différentes size)}
