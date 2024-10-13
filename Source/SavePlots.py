import os
import re
import pandas as pd
import matplotlib.pyplot as plt

rumorose_df = pd.read_csv('Immagini_Rumorose/risultati_rumorose.csv')
restaurate_df = pd.read_csv('Immagini_Restaurate/risultati_restaurate.csv')

merged_df = pd.merge(rumorose_df, restaurate_df, on='ID', suffixes=('_rumorosa', '_restaurata'))

def get_common_name_by_id(id_val):
    id_data = merged_df[merged_df['ID'] == id_val]
    if id_data.empty:
        return "Nome Sconosciuto"
    nome_completo = id_data['NomeFile_rumorosa'].values[0]
    nome_modificato = re.sub(r'(_[^_]+){1}$', '', nome_completo)
    nome_modificato = re.sub(r'(_)', r'\1rumore_', nome_modificato, count=1)
    return nome_modificato

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

    nome_comune = get_common_name_by_id(id_val)

    for metric in metrics:
        plt.figure(figsize=(10, 5))
        values = [id_data[f'{metric}_rumorosa'].values[0], id_data[f'{metric}_restaurata'].values[0]]
        bars = plt.bar(['Rumorosa', 'Restaurata'], values, color=['#b22222', '#32cd32'])

        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02 * ranges[metric][1], f'{value:.2f}', ha='center', va='bottom', fontsize=10, color='black', weight='bold')

        plt.xlabel('Tipo Immagine')
        plt.ylabel(f'Valore della Metrica {metric}')
        plt.ylim(ranges[metric])
        plt.title(f'{metric} - {nome_comune}')
        plt.grid(axis='y')
        plt.savefig(os.path.join(output_folder, f'barplot_{metric}_ID_{id_val}.png'))
        plt.close()

def lineplot_metrics_for_id(id_val, output_folder):
    id_data = merged_df[merged_df['ID'] == id_val]
    if id_data.empty:
        print(f"ID {id_val} non trovato.")
        return

    metrics = ['PSNR', 'MSE', 'SSIM']
    metrics_colors = {'PSNR': 'blue', 'MSE': 'red', 'SSIM': 'orange'}

    nome_comune = get_common_name_by_id(id_val)

    for metric in metrics:
        plt.figure(figsize=(10, 5))
        values = [id_data[f'{metric}_rumorosa'].values[0], id_data[f'{metric}_restaurata'].values[0]]
        plt.plot(['Rumorosa', 'Restaurata'], values, marker='o', label=metric, color=metrics_colors[metric])

        for i, value in enumerate(values):
            plt.text(i, value + (0.01 * value), f'{value:.2f}', ha='center', va='bottom', fontsize=10, color='black', weight='bold')

        plt.xlabel('Tipo Immagine')
        plt.ylabel(f'Valore della Metrica {metric}')
        plt.title(f'{metric} - {nome_comune}')
        plt.grid(True)
        plt.savefig(os.path.join(output_folder, f'lineplot_{metric}_ID_{id_val}.png'))
        plt.close()

for id_val in range(1, 13):
    output_folder = os.path.join('Grafici', f'plot_{id_val}')
    os.makedirs(output_folder, exist_ok=True)

    lineplot_metrics_for_id(id_val, output_folder)
    barplot_metrics_for_id(id_val, output_folder)

print("Grafici salvati con successo per tutti gli ID da 1 a 12.")
