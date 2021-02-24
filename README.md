# esame

Una time series (univariata) è una serie di coppie di punti dove il primo elemento della coppia è un istante di tempo, anche detto timestamp, ed il secondo è il valore di una qualche quantità relativa a quell’istante, come ad esempio la temperatura.


Il timestamp può essere rappresentato in vari formati, uno dei più comuni in informatica è l’epoch, che sta a rappresentare il numero di secondi passati dalla mezzanotte (00:00) del  primo Gennaio 1970 sulla timezone UTC (ovvero il meridiano fondamentale di Greenwich, senza cambi di ora legale). All’una di notte del primo Gennaio 1970 il timestamp epoch vale quindi “3600” secondi, alle due vale “7200” secondi, e così via.


Al momento della scrittura di questo testo, il 18 Febbraio 2021 alle 23:25 in Italia, ovvero alle 22:25 UTC, l’epoch vale “1613600700” secondi. Tra un minuto questo epoch sarà incrementato di 60 secondi (e varrà “1613600760”). E domani alla stessa ora sarà incrementato di 86400 secondi (60 secondi volte 60 minuti volte 24 ore) e varrà quindi “1613687100”. Questo sito fornisce un rapido modo di convertire una data e ora in epoch e viceversa: epochconverter.com.


Il file data.csv contiene la time series della temperatura dell’interno di un’abitazione, registrata ogni 10 minuti per un paio di settimane a Gennaio 2019, e si presenta così:


epoch,temperature

1546819200,22.78

1546819800,22.84

1546820400,22.85

...


ovvero, messa sotto forma di tabella per comodità:


epoch

temperature

1546819200

22.78

1546819800

22.84

1546820400

22.85

...

...



Vogliamo leggere questo tipo di dati e calcolare quante volte, per ogni ora, c’è una inversione del trend di temperatura. Per “trend di temperatura” si intende semplicemente quando la variazione di temperatura cambia segno, ovvero se ho le temperature “21,22,20,19,18,17,19” ho avuto due inversioni del trend di temperatura (tra 22 e 20, e tra 17 e 19).




Informazioni sullo svolgimento

Non c’è un limite minimo o massimo a quanti dati ci sono nel file CSV. Potrebbe esserci una misurazione soltanto, una manciata di misurazioni tutte appartenenti alla stessa ora, oppure misurazioni per decine di ore o anche mesi e mesi di dati.


Un punto chiave dello svolgimento sta nel capire, dato il timestamp epoch delle misurazioni, se quest’ultime appartengono alla stessa ora (non a quale ora, ma solo se alla stessa ora) e gestire correttamente il tutto.


Possono esserci dei dati mancanti, quindi attenzione a come gestite le aggregazioni orarie ed ai conti che fate. Tuttavia, se mancano dati, questi non mancano mai per più di un’ora (ovvero, per ogni ora è presente almeno una misurazione di temperatura).


Lavoriamo esclusivamente sulla timezone UTC (dove non si considera mai il passaggio all’ora legale, che invece nella realtà è parecchio fastidioso).


Alla luce di tutto questo, create la classe CSVTimeSeriesFile, modificando o estendendo la classe CSVFile vista a lezione (oppure scrivendola da zero). La classe deve essere istanziata sul nome del file tramite la variabile name e deve avere un metodo get_data() che torni una lista di liste, dove il primo elemento delle liste annidate è l’epoch ed il secondo la temperatura.


Questa classe si dovrà quindi poter usare così:


        time_series_file = CSVTimeSeriesFile(name='data.csv')


    time_series = time_series_file.get_data()


...ed il contenuto della variabile time_series tornato dal metodo get_data() dovrà essere così strutturato (come lista di liste):


    [

      [1546819200, 22.78],

      [1546819800, 22.84],

      [1546820400, 22.85],

      ...

    ]


Per calcolare quante volte cambia il trend della temperatura per ogni ora, dovete invece creare una funzione a sé stante (cioè posizionata non nella classe CSVTimeSeriesFile ma direttamente nel corpo principale del programma), di nome hourly_trend_changes, che avrà come input la time series e che verrà usata così:


    hourly_trend_changes(time_series)


..e che dovrà ritornare in output, tramite un return, una lista i cui elementi sono il numero di inversioni di trend di temperatura rilevati per ogni ora presente nel dataset:


    [

      numero_inversioni_di_trend_prima_ora_del_dataset,

      numero_inversioni_di_trend_seconda_ora_del_dataset,

      numero_inversioni_di_trend_terza_ora_del_dataset,

      ...

    ]


Il file in cui scrivere il vostro codice deve chiamarsi "esame.py" e le eccezioni da alzare in caso di input non corretti o casi limite devono essere istanze di una specifica classe ExamException, che dovete definire nel codice come segue, senza modifica alcuna (copia-incollate le due righe):


    class ExamException(Exception):

        pass


...e che poi userete come una normale eccezione, ad esempio:


    raise ExamException('Errore, lista valori vuota')



Qualche informazione in più sulle specifiche e qualche e suggerimento:

Le misurazioni che sono effettuate esattamente ad inizio ora (ad esempio alle 16:00 esatte) fanno parte dell’ora entrante. In particolare, se la misurazione delle 16:00 fa cambiare il trend delle temperatura, questo cambio di trend va conteggiato assieme agli altri potenziali cambi di trend dovuti alle misurazioni delle 16:10, 16:20, 16:30 etc. fino alle 17:00 escluse. Chiaramente voi dovete usare epoch e non ore “umane” come invece fatto in questo esempio per semplificare la lettura, ma il concetto non cambia.
Attenzione che nel calcolo delle inversioni di trend per una determinata ora non vi basta considerare esclusivamente le misurazioni di quell’ora, ma potreste dover considerare anche cosa succede nell’ora precedente (se non nelle ore precedenti in certi casi limite). Consideriamo infatti il seguente esempio (dove i timestamp sono anche in questo caso rappresentati con ora “umana” e non epoch per semplicità di lettura):
15:50      temperatura = 22
16:00      temperatura = 20
16:10      temperatura = 21

In questo caso l’inversione di trend tra le 16:00 e le 16:10 conta come inversione di trend appartenente all’ora che va dalle 16 alle 17, ma è necessario tenere in considerazione anche l’informazione delle 15:50 per poter rilevare correttamente l’inversione. Spingendo al limite, consideriamo anche quest’ ulteriore esempio in cui c’è solo una misurazione all’ora ora che coincide con l'inizio delle varie ore:

14:00      temperatura = 22
15:00      temperatura = 21
16:00      temperatura = 23

In questo caso il trend di temperatura cambia alle 16:00, ma per poterlo rilevare correttamente bisogna considerare addirittura la misurazione delle 14:00. Occhio quindi ai vari casi limite e a come processate le misurazioni.

I timestamp epoch che leggete da file sono da considerarsi di tipo intero. Se per caso dovessero esserci dei timestamp epoch floating point, questi vanno convertiti silenziosamente ad interi (tramite arrotondamento con round(), non tramite cast diretto) e tutto deve procedere comunque.
I valori di temperatura che leggete dal file CSV sono da aspettarsi di tipo numerico (intero o floating point): un valore di temperatura non numerico, oppure vuoto o nullo
non deve essere accettato, ma tutto deve procedere comunque senza alzare eccezioni.
La serie temporale nel file CSV è da considerarsi sempre ordinata, se per caso ci dovesse essere un timestamp fuori ordine o un duplicato va alzata un'eccezione nella funzione get_data(), e non si deve cercare di riordinare la serie.
Il file CSV può contenere letteralmente di tutto. Da linee incomplete a pezzi di testo che non c’entrano niente, e ogni errore salvo quello di un timestamp fuori ordine o duplicato va ignorato (ovvero, ignoro la riga contenente l’errore e vado a quella dopo). Nota: se riuscite a leggere due valori (epoch e temperatura) ma c’è un campo di troppo sulla stessa riga, questo non è da considerarsi un’errore e non bisogna ignorare quella riga.
Se leggete correttamente una serie temporale dal file CSV, questa (come già accennato precedentemente) è assicurato abbia almeno una misurazione di temperatura per ora.
La classe CSVTimeSeriesFile controlla l’esistenza del file solo quando viene chiamato il metodo get_data() e, nel caso il file non esista o non sia leggibile, alza un'eccezione.
Suggerimento: per capire se due timestamp epoch appartengono alla stessa ora, vi basta dividerli entrambi per 3600 e confrontare il risultato.
Nota bene: la lista in output da hourly_trend_changes() contiene semplicemente  il numero di inversioni di trend per ogni ora del dataset, senza nessun riferimento a quali ore siano o senza usare concetti di aritmetica modulare sulle 24 ore . Ovvero, se il dataset ha 3 giorni di dati, la lista in output deve essere semplicemente di 24*3 = 72 elementi, dove gli elementi sono un numero intero che rappresenta  appunto il numero di cambi nel trend di temperatura per la prima ora dei dati, per la seconda, e così via.
