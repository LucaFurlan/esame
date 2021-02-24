# -*- coding: utf-8 -*-
"""
ESAME

Created on Fri Feb 19 19:29:33 2021

@author: furlan
"""
class ExamException(Exception): 
    pass

class CSVFile():
    def __init__(self,name):
        if  not isinstance(name,str):  #controllo che l'argomento passato passato in fase di inizailizzazione sia di tipo stringa
            raise ExamException("il nome del file deve essere passato attraverso un valore di tipo str") #in caso contratio alzo un'eccezione
        self.name=name
    def get_data(self):
        try:
            f=open(self.name, mode="r")
        except:
            raise ExamException("impossibile aprire il file, file inesistente")
        result=[]
        for line in f:
            elements=line.split(",")
            result.append(elements)
        f.close()

class CSVTimeSeriesFile(CSVFile):
    def get_data(self):
        try:
            f=open(self.name, mode="r") #provo ad aprire il file
        except:
            raise ExamException("impossibile aprire il file, file inesistente o accesso negato")  #alzo un'eccezione qualora non fosse possibile
        result=[]  #inizializzo una variabile lista di output
        for line in f:
            elementi=line.split(",") #inizializzo una lista contenete sottoforma di stringa gli elementi della linea divisi dagli elementi separatori del file
            if len(elementi)>=2: #controllo che vi siano almeno due elementi, altrimenti la linea viene ignorata 
                try:
                    epoch=int(elementi[0]) #provo a tramutare in intero il primo elemento della lista e lo attribuisco alla variabile epoch
                except:
                    try:
                        epoch=float(elementi[0]) #qualora non sia possibile renderlo intero, provo a renderlo un floating point
                        epoch=round(epoch) #qualora sia un floating point lo arrotondo ad intero
                    except:
                        continue #ignoro l'intera linea e passo alla sucessiva, qualora nel suo primo elemento non sia possibile leggere un valore epoch valido
                if result!=[] and epoch<=result[-1][0]: #se e' stato salvato almeno un record nella lista di output, controllo che il valore epoch sia strettamente maggiore dell'ultimo salvato
                    raise ExamException("problema di ordine epoch") # nel caso non lo fosse alzo un'eccezione come da specifiche
                try:
                    temperature=float(elementi[1]) #provo a tramutare in floating point il secondo elemento della lista e lo attribuisco alla var temperature
                except:
                    continue #qualora non fosse possibile ignoro l'intera linea e passo alla successiva
                if temperature!=0: #controllo che il valore di temperatura non sia un valore numerico nullo, in tal caso ignoro la linea e passo alla sucessiva
                    result.append([epoch,temperature]) #aggiungo alla lista di output una lista avente come primo e secondo elemento epoch e temperatura
        f.close() #chiudo il file
        return result #ritorno la lista

def hourly_trend_changes(time_series):
    if not isinstance(time_series,list): #controllo che il dato in input sia effetivamente una lista, altrimenti alzo un'eccezione
        raise ExamException("il dato passato alla funzione deve essere di tipo lista")
    if len(time_series)<3: #controllo che la lista abbia almeno 3 record, altrimenti la funzione di ricerca seppur funzionante, non avrebbe senso
        raise ExamException("per misurare i cambiamenti di trend orari è necessaria una lista di dati di almeno 3 elementi") #in caso contrario alzo un eccezione
    result=[] #inizializzo una variabile lista di output
    prec_variation=0 #inizializzo a 0 una avariabile ausiliaria, rappresentante la differenza fra le due variabili precedenti in ordine
    changes=0 #inizializzo a 0 una variabile ausiliaria, rappresentante un counter per il numero di cambiamenti di trend nell'ora considerata
    try:next_hour=((time_series[0][0]//3600)+1)*3600 #calcolo il valore epoch di inizio dell'ora a cui appartiene il primo valore epoch della time series e lo incremento di 3600 per passare all'inizio dell'ora successiva 
    except:raise ExamException("errore nel formato dati della time series")#qualora il calcolo non fosse possibile il formato dati della time series non è corretto
    i=1 #inizializzo a 1 l'indice di iterazione del while
    while i<len(time_series): #itero il processo su ogni elemento della time series tranne il primo
        try:
            while i<len(time_series) and time_series[i][0]<next_hour: #avvio un iterazione finché non raggiungo la fine della time series oppure il valore epoch corrente appartiene all'ora sucessiva
                if prec_variation*(time_series[i][1]-time_series[i-1][1])<0: #controllo che la variazione precedente fra le temperature e quella che considero siano discordi nel segno
                    changes+=1 #qualora lo fossero si ha un'inversione di trend e aumento di 1 il counter
                    prec_variation*=(-1) #invece di attribuire alla variabile ausiliaria il valore della variazione attuale ne cambio solo il segno, unico nostro interesse
                elif prec_variation==0: #qualora prec_variation abbia il valore di default
                    prec_variation=time_series[i][1]-time_series[i-1][1] #le attribuisco l'effettivo valore della variazione attuale
                i+=1 # incremento l'indice di ricorsione
        except:
            ExamException("errore nel tipo di dati") #nel caso in cui vi siano errori sono attribuibili ad IndexError o a TypeError riconducibili a un formato dati della time series non corretto, da notare che gli elementi lista della timeseries possono avere anche più di 2 elementi
        result.append(changes) # aggiungo il numero di inversioni rilevate per quel giorno alla lista di output
        changes=0 #azzero il counter
        next_hour+=3600 #incremento di 3600 per passare all'inizio dell'ora sucessiva
        #da notare l'assenza dell'incremento dell'indice i 
    return result #restituisco la lista di output          
                      
#se lanciato dà in output numero di giorni e lista delle inversioni di trend per giorno di un file "data.csv" presente nella cartella           
if __name__=="__main__":                   
                
    time_series_file = CSVTimeSeriesFile(name='data.csv')


    time_series = time_series_file.get_data()




    b=hourly_trend_changes(time_series)



    print(len(b))
    
    print(b)