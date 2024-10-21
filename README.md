# MultimediaProject
Il restauro di immagini digitali è fondamentale in numerosi settori, tra cui la medicina diagnostica, la videosorveglianza e la conservazione di archivi storici. Le immagini possono essere compromesse da vari tipi di rumore, come quello gaussiano, sale e pepe o periodico, che ne degradano la qualità e l'utilità. Nonostante i progressi nelle tecniche di acquisizione e trasmissione, il rumore rimane una sfida significativa che può ostacolare l'analisi e l'interpretazione delle immagini.
Questo progetto mira a sviluppare un sistema software che permetta agli utenti di migliorare la qualità visiva di immagini degradate attraverso l'applicazione di filtri e tecniche di deconvoluzione. Sono state selezionate quattro immagini, sia a colori che in scala di grigi, sulle quali sono stati applicati tre tipi distinti di rumore. Successivamente, diversi algoritmi di filtraggio sono stati utilizzati per il restauro, con l'obiettivo di valutare l'efficacia di ciascun filtro in relazione al tipo di rumore presente.
Gli obiettivi principali di questo lavoro sono:
	Implementare un'interfaccia utente intuitiva per facilitare l'applicazione dei filtri;
	Automatizzare la raccolta dei dati dei risultati in file CSV per un'analisi approfondita;
	Valutare se i filtri utilizzati per il restauro migliorano effettivamente la qualità delle immagini affette da rumore rispetto alle originali, utilizzando metriche quantitative.
La struttura modulare del programma consente una facile estensione con nuovi filtri e funzionalità. L'interfaccia grafica sviluppata con PyQt5 garantisce un'esperienza utente intuitiva, permettendo una gestione efficiente delle operazioni di restauro.
Nel corso della relazione verranno descritti in dettaglio la metodologia adottata, i risultati ottenuti e un'analisi critica delle prestazioni dei filtri. Infine, saranno discusse le possibili direzioni future, tra cui:
	l'integrazione di tecniche avanzate di deep learning, come le Reti Neurali Convoluzionali (CNN) e le Generative Adversarial Networks (GAN); 
	l'ottimizzazione delle prestazioni attraverso l'elaborazione parallela su GPU;
che potranno rendere il sistema più efficiente e adatto a contesti applicativi complessi.
