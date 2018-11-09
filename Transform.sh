#!/bin/bash
##############################################################################
# Nombre        : Transform.sh
# Descripción   : Realiza la transformación de los archivos del Dataset Topology Zoo
#                 Cálcula la distancia para cada nodo Soruce - Edge
#                                 
# Parámetros:
# Realizado Por : Richard Abuabara Caserta
#
# HISTORIAL DE CAMBIOS:
#
# 
##############################################################################

File=$1
nodes=`grep -i "node id=" $1 | wc -l`
echo "El numero de nodos para esta topolopia es: "$nodes
nodes=`expr $nodes - 1`

###############################SEARCHING THE MAX#############################################
function Maximum(){
arg=$1
var4=`grep -i "node id=" $arg | wc -l`
max=0
for (( h=0; h<$var4;h++))
do
    aux=`cat Source_Edge.txt | grep -i "source=$h " | wc -l`
    if [[ $aux > $max ]] ; then
        max=$aux
    fi
done
}
################################# END S. MAX ################################################

###############################SACAR DATO SOURCE - EDGE#####################################
function S_E(){
k=$1
cat Source_Edge.txt | grep -i "source=$k " >temp.txt
conct=`awk 'BEGIN { FS="=" } { printf ("%d;" , $3);N=NR}END{for (i=N+1;i<='$max';i++) printf (";");print ""}' temp.txt` #>temp2.txt
#echo $conct
}
###############################END S-E######################################################


############################### HAVERSINE FORMULE ########################################
function deg2rad () {
 bc -l <<< "0.0174532925 * $1" # 1 Radian = 0.0174533 Deg
}

function rad2deg () {
 bc -l <<< "57.2958 * $1" # 57.2958 DEG = 1 RAD (57.2957795)
}

function acos () {
 pi="3.141592653589793"
 bc -l <<<"$pi / 2 - a($1 / sqrt(1 - $1 * $1))"
}

function distance () {
 lat_1="$1"
 lon_1="$2"
 lat_2="$3"
 lon_2="$4"
 delta_lat=`bc <<<"$lat_2 - $lat_1"`
 delta_lon=`bc <<<"$lon_2 - $lon_1"`
 lat_1="`deg2rad $lat_1`"
 lon_1="`deg2rad $lon_1`"
 lat_2="`deg2rad $lat_2`"
 lon_2="`deg2rad $lon_2`"
 delta_lat="`deg2rad $delta_lat`"
 delta_lon="`deg2rad $delta_lon`"
 
 distance=`bc -l <<< "s($lat_1) * s($lat_2) + c($lat_1) * c($lat_2) * c($delta_lon)"` #ACOS(COS(RADIANES(90-L1))*COS(RADIANES(90-L2))+SENO(RADIANES(90-L1))*SENO(RADIANES(90-L2))*COS(RADIANES(E4-E5))))
 distance=`acos $distance`
 distance="`rad2deg $distance`"
 distance=`bc -l <<< "$distance * 60 * 1.15078 * 1.609344"` #distancia km
 distance=`bc <<<"scale=4; $distance / 1"`
 distance=$distance";"
 #echo $distance
}

######################### END HAVERSINE FORMULE #############################################

######################### Get Lantency#######################################################
function Latency(){
Lat=`bc -l <<< "scale=4;($1 * 1000) / (1.97 * ( 10^5))"`
}
#############################################################################################

############################## BUSCAR LOS NODOS #############################################

var="node id="
var1=`grep -i "$var" $1`
grep -n $var1 $1 > output.txt 2>/dev/null #funciona
awk 'BEGIN { FS=":" } { print $2}' output.txt > output2.txt

################################ BUSCAR CONEXIONES SOURCE - EDGE #############################################
var2="edge source="
var3=`grep -i "$var2" $1`
grep -n $var3 $1 > newoutput.txt 2>/dev/null #funciona
cat newoutput.txt | awk 'BEGIN { FS="<" } { print $2}' newoutput.txt > newoutput2.txt
cat newoutput2.txt | sed 's/"//g' | sed 's/>//g'> Source_Edge.txt
rm newoutput*
##############################################################################################################

Maximum $File
#echo $max

##################### PARA CONSTRUIR EL ARCHIVO FINAL THE TOPOLOGY ZOO ######################### 
for j in `cat output2.txt`
do
               ##echo $j
               id=`awk 'NR=='$j'{print $0 }' $1`
               id=`echo $id | sed 's/"/:/g'`
               id=`echo $id |  awk 'BEGIN { FS=":" } { print $2}' `
               #echo $id
               lat=`awk 'NR=='$j+2'{print $0 }' $1`
               lat=`echo $lat | sed 's/>/</g'`
               lat=`echo $lat |  awk 'BEGIN { FS="<" } { print $3}' `
               #echo $lat
               long=`awk 'NR=='$j+5'{print $0 }' $1`
               long=`echo $long | sed 's/>/</g'`
               long=`echo $long |  awk 'BEGIN { FS="<" } { print $3}' `
               #echo $long
			   S_E $id
               echo $id";"$lat";"$long";"$conct >> "new"$1
               #awk 'NR=='$j'{print $0; l= '$j'+2 }; NR==l {print $0; ll= '$j'+5}; NR==ll {print $0}' $1 #ok
done
rm output*
rm temp.txt

################################################ Calculo Distancia######################################################
maxx=`expr $max + 3`
for j in `cat new$1`
do
        for (( i=4;i<=$maxx;i++ )) #maxx = max*2
		do
			 
			 edg=`echo $j | awk 'BEGIN { FS=";" } { print $'$i'}'`
			 if [[ $edg != "" ]] ; then
			     lat1=`echo $j | awk 'BEGIN { FS=";" } { print $2}'`
				 lon1=`echo $j | awk 'BEGIN { FS=";" } { print $3}'`
                 lat2=`cat "new"$1 | awk 'BEGIN { FS=";" } ($1=='$edg') {print $0}' | awk 'BEGIN { FS=";" } {print $2}'`
                 lon2=`cat "new"$1 | awk 'BEGIN { FS=";" } ($1=='$edg') {print $0}' | awk 'BEGIN { FS=";" } {print $3}'`
                 distance $lat1 $lon1 $lat2 $lon2 	
				 new[$i-4]=$distance  
			 
			 else
			     new[$i-4]=";"
			 			 
			 fi
			 
		done
		echo $j${new[*]} >> temp.txt
done

perl -lape 's/\s+//sg' temp.txt > "new"$1
rm temp*
rm Source_Edge.txt
###########################################################################################################################

################################################ Calculo Latency ######################################################
maxx=`expr $max + 4`
#maxl=`expr $maxx + $max - 1`
for j in `cat new$1`
do
        for (( i=0;i<=$max-1;i++ )) #maxx = max*2
		do
			 hold=`expr $maxx + $i`
			 dist=`echo $j | awk 'BEGIN { FS=";" } { print $'$hold'}'`
			 if [[ $dist != "" ]] ; then
			     Latency $dist
				 aux=`expr $i + 4`
				 aux=`echo $j | awk 'BEGIN { FS=";" } {print $'$aux'}'`
				 echo $j | awk 'BEGIN { FS=";" } { print $1" "'$aux'" "'$Lat'}' >> temp.txt
			 fi		 
		done
done
cat temp.txt > "new"$1
rm temp*
cat "new"$1 | awk 'BEGIN { FS=" " } { print $2" "$1" "$3}' >> "new"$1
cat "new"$1 | sort -nk 1 > temp.txt && mv temp.txt "new"$1
