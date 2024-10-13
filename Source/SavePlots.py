import os
import pandas as pd
import matplotlib.pyplot as plt

# Caricamento dei dati
rumorose_df = pd.read_csv('Immagini_Rumorose/risultati_rumorose.csv')
restaurate_df = pd.read_csv('Immagini_Restaurate/risultati_restaurate.csv')

# Unione dei dataframe
merged_df = pd.merge(rumorose_df, restaurate_df, on='ID', suffixes=('_rumorosa', '_restaurata'))

# Funzione per salvare i grafici a barre per un singolo ID
def barplot_metrics_for_id(id_val, output_folder):
    id_data = merged_df[merged_df['ID'] == id_val]
    if id_data.empty:
        print(f"ID {id_val} non trovato.")
        return

    metrics = ['PSNR', 'MSE', 'SSIM']
    ranges = {
        'PSNR': (10, 40 * 1.2),
        'MSE': (0, id_data[['MSE_rumorosa', 'MSE_restaurata']].max().max() * 1.2),
        'SSIM': (0, 1 * 1.2)
    }

    for metric in metrics:
        plt.figure(figsize=(10, 5))
        values = [id_data[f'{metric}_rumorosa'].values[0], id_data[f'{metric}_restaurata'].values[0]]
        bars = plt.bar(['Rumorosa', 'Restaurata'], values, color=['#b22222', '#32cd32'])

        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02 * ranges[metric][1], f'{value:.2f}', ha='center', va='bottom', fontsize=10, color='black', weight='bold')

        plt.xlabel('Tipo Immagine')
        plt.ylabel(f'Valore della Metrica {metric}')
        plt.ylim(ranges[metric])
        plt.title(f'{metric} - Immagine ID: {id_val}')
        plt.grid(axis='y')
        plt.savefig(os.path.join(output_folder, f'barplot_{metric}_ID_{id_val}.png'))
        plt.close()

# Funzione per salvare i grafici a linee per un singolo ID
def lineplot_metrics_for_id(id_val, output_folder):
    id_data = merged_df[merged_df['ID'] == id_val]
    if id_data.empty:
        print(f"ID {id_val} non trovato.")
        return

    metrics = ['PSNR', 'MSE', 'SSIM']
    metrics_colors = {'PSNR': 'blue', 'MSE': 'red', 'SSIM': 'orange'}

    for metric in metrics:
        plt.figure(figsize=(10, 5))
        values = [id_data[f'{metric}_rumorosa'].values[0], id_data[f'{metric}_restaurata'].values[0]]
        plt.plot(['Rumorosa', 'Restaurata'], values, marker='o', label=metric, color=metrics_colors[metric])

        for i, value in enumerate(values):
            plt.text(i, value + (0.01 * value), f'{value:.2f}', ha='center', va='bottom', fontsize=10, color='black', weight='bold')

        plt.xlabel('Tipo Immagine')
        plt.ylabel(f'Valore della Metrica {metric}')
        plt.title(f'{metric} - Immagine ID: {id_val}')
        plt.grid(True)
        plt.savefig(os.path.join(output_folder, f'lineplot_{metric}_ID_{id_val}.png'))
        plt.close()

# Iterazione tra gli ID da 1 a 12 e salvataggio dei grafici
for id_val in range(1, 13):
    output_folder = f'plot_{id_val}'
    os.makedirs(output_folder, exist_ok=True)

    # Generazione e salvataggio dei grafici a barre e a linee per ogni ID
    lineplot_metrics_for_id(id_val, output_folder)
    barplot_metrics_for_id(id_val, output_folder)

print("Grafici salvati con successo per tutti gli ID da 1 a 12.")