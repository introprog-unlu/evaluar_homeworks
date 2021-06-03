#!/usr/bin/python

from os import listdir
from os.path import isdir
import os
import subprocess
import json
import csv
import sys, getopt


def main(argv):
    inputdir = ''
    outputdir = ''
    autogradintFile = 'autogradingsValues.json'
    roostercsvfile = 'classroom_roster_2021.csv'
    try:
        opts, args = getopt.getopt(argv,"hi:o:")
    except getopt.GetoptError:
        print ('runtest.py -i <inpudir> -o <outputdir>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print ('runtest.py -i <inputdir> -o <outputdir>')
            sys.exit()
        elif opt in ("-i"):
            inputdir = arg
        elif opt in ("-o"):
            outputdir = arg

    autogradingsJson = {}

    with open (autogradintFile, 'r') as autogradingsValuesFile:
        autogradingsJson = json.load(autogradingsValuesFile)
    rooster = {}
    with open (roostercsvfile, 'r') as roosterFile:
        csv_content = csv.reader(roosterFile,delimiter=',')
        for student_rooster in csv_content:
            rooster[student_rooster[1]]=student_rooster[0] 

    if isdir(inputdir) and isdir(outputdir):  
        #Recorro los directorios deonde estan los wh
        list_results= []
        list_results_extended = []
        for hw in listdir(inputdir):
            if isdir(inputdir+'/'+hw):
                #Recorro los hw de los estudiantes en un HWX
                #Cada hw indicidual corresponde con el alumno
                for student in listdir(inputdir+'/'+hw):
                    path = inputdir+'/'+hw+'/'+student+'/'
                    if isdir(path):
                        if student != '.pytest_cache' and student in rooster:
                            #  autogradingsJson['HW'+parse_hw(hw)[0]]
                            # Recorro todos los test para este hw
                            # Formato ['comandodetest archivo_con_test::test_individual', puntaje]
                            # ejempolo: ['pytest test_hw1.py::testValorAbsoluto', 15]
                            succes , failed = 0, 0
                            for test_unit  in  autogradingsJson['HW'+parse_hw(hw)[0]]:
                                #ejecuto los test, si pasan suman los puntos positivos
                                #si no suman suman los puntos negativos
                                #se calcula con esto los puntajes
                                hw_number = hw.split()[1].split('-')[0]
                                function_name = getTestFromComand(test_unit[0].split()[1])

                                if not subprocess.call(['python3',\
                                    '-m',\
                                    test_unit[0].split()[0],
                                    path+test_unit[0].split()[1],
                                    '--quiet',
                                    '--tb=no',
                                ]):
                                    #Se guardan los resultados extendidos (hw,ejercicio,estudiante,identificador_estudiante,exitoso,fallidos)
                                    list_results_extended.append([hw_number,rooster[student],student,function_name,test_unit[1],0])
                                    succes += test_unit[1]

                                else:
                                    list_results_extended.append([hw_number,rooster[student],student,function_name,0,test_unit[1]])
                                    print((hw_number,rooster[student],student,function_name,0,test_unit[1]))
                                    failed += test_unit[1]
                            #Se guardan los resultados (hw,estudiante,identificador_estudiante,exitosos,fallidos,total)
                            list_results.append([hw_number,rooster[student],student,succes,failed, succes+failed])
        # guardo los datos de los test en un archivo
            with open(outputdir+'/List_result_Hw'+hw+'_sutuden.csv','w',newline='') as out:
                csv_out=csv.writer(out)
                csv_out.writerow(['hw','estudiante','identificador_estudiante','exitosos','fallidos','total'])
                csv_out.writerows(list_results)
            with open(outputdir+'/List_result_Hw'+hw+'_sutuden_extended.csv','w',newline='') as out:
                csv_out=csv.writer(out)
                csv_out.writerow(['hw','ejercicio','estudiante','identificador_estudiante','exitoso','fallidos'])
                csv_out.writerows(list_results_extended)
            list_results_extended=[]
            list_results= []
    else:
        print(inputdir,outputdir,"Tienen que ser directorios validos")

def parse_hw(hw):
    hw_date = hw.split()[1].split('-')
    return  hw_date[0],'-'.join(hw_date[1:])

#separa el string me quedo con el nombre de la funcion y le saco la palabra test
# para el primer homework tengo que escapar el _ 
def getTestFromComand(comand):
    print(comand)
    if '_' in comand:
        print(comand)
        return comand.split('::')[1]
    else:
        return comand.split('::')[1][4:]

if __name__ == "__main__":
   main(sys.argv[1:])
