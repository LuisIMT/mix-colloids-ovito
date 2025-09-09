import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path
import json, os

class Grapichs:
    def __init__(self) -> None:
        pass

    def write_category_colors(self, df:pd.DataFrame, color_file:str ) -> dict :
        df_structure = df.dropna(subset=['Acronimos'])
        categories = df_structure['Acronimos'].unique()
        palette = plt.get_cmap('Paired', lut=len(categories))
        category_colors = {category: palette(i) for i, category in enumerate(categories)}
        self.save_category_colors(category_colors, color_file)
        return category_colors
        
    def save_category_colors(self,category_colors:dict, filename:str) -> None:
        """Guardar el diccionario de colores en un archivo JSON."""
        with open(filename, 'w') as file:
            json.dump(category_colors, file)

    def load_category_colors(self,filename:str)-> dict:
        """Cargar el diccionario de colores desde un archivo JSON."""
        with open(filename, 'r') as file:
            return json.load(file)
        
    def diagram_structure(self,clasification:str, lambda_A:str, color_file = None) -> None:
        # Leer el archivo CSV
        df = pd.read_csv(clasification, skiprows=1)
        particles_A_fixed = df[df['particulaA'] == lambda_A]
        particles_A_fixed = particles_A_fixed.dropna(subset=['Acronimos'])
        
        particles_A_fixed['cociente'] = particles_A_fixed['cociente'].astype(float)
        particles_A_fixed['densidad'] = particles_A_fixed['densidad'].astype(float)

        radio = df.loc[0, 'radio']
        if color_file != None:
            category_colors = self.load_category_colors(filename=color_file) 
        else:
            category_colors = self.write_category_colors(df=df,color_file='category_color.json')
        categories_colors = particles_A_fixed['Acronimos'].unique()
        filtered_colors = {category: category_colors[category] 
                                    for category in categories_colors}
        colors = particles_A_fixed['Acronimos'].map(filtered_colors)
        fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
        
        # Redondear los valores de los puntos
        particles_A_fixed['cociente'] = particles_A_fixed['cociente'].round(3)
        particles_A_fixed['densidad'] = particles_A_fixed['densidad'].round(3)

            
        scatter = ax.scatter(particles_A_fixed['densidad'], particles_A_fixed['cociente'], 
                            c=colors, s=50)
        ax.set_xlabel(r"$\rho^{*}$", fontsize=14)
        ax.set_ylabel(r"$\delta$", fontsize=14 )
        ax.set_title(f'Diagrama de Estructuras', fontsize=16)

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.3f}"))

        handles = [plt.Line2D([0], [0], marker='o', color=color, label=category,
                            linestyle='', markerfacecolor=color, markersize=10) 
                for category, color in filtered_colors.items()]
        ax.legend(handles=handles, title=f'Estructuras Radio {radio}', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        output_file = f'C://Users//Hp//simulations//core-shell//fixed_particles_A_r_{radio}//densidad_cociente_{radio}_lA_{lambda_A}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print("Save_correct")
        plt.close(fig)
        #plt.show()


    def energies(self, clasification:str, color_file:str) -> None:

        # Cargar el archivo CSV
        df = pd.read_csv(clasification, skiprows=1)
        radio = df.loc[0, 'radio']

        # Eliminar filas con valores nulos en 'Acronimos'
        df = df.dropna(subset=['Acronimos'])

        # Asegurarse de que 'Acronimos' sea de tipo str
        df.loc[:, 'Acronimos'] = df['Acronimos'].astype(str)

        # Eliminar cualquier fila en 'Acronimos' que contenga valores numéricos no deseados
        df = df[df['Acronimos'].str.isalpha()]

        # Convertir columnas numéricas
        df.loc[:, 'cociente'] = pd.to_numeric(df['cociente'], errors='coerce')
        df.loc[:, 'Energia'] = pd.to_numeric(df['Energia'], errors='coerce')

        # Cargar colores por categoría (diccionario con claves tipo 'SE', 'OM', etc.)
        all_category_colors = self.load_category_colors(filename=color_file)

        # Verificar si existe la columna de densidades
        if 'densidad' in df.columns:
            densidades = df['densidad'].unique()

            for densidad in densidades:
                df_dens = df[df['densidad'] == densidad]

                # Filtrar los colores a solo los acrónimos presentes
                present_categories = df_dens['Acronimos'].unique()
                present_category_colors = {
                    cat: all_category_colors[cat] for cat in present_categories if cat in all_category_colors
                }

                # Colorear por categoría
                colors = df_dens['Acronimos'].map(present_category_colors)

                # Crear la figura
                fig, ax = plt.subplots(figsize=(10, 8))
                scatter = ax.scatter(df_dens['cociente'], df_dens['Energia'], c=colors, s=50)

                # Crear la leyenda
                handles = [
                    plt.Line2D([0], [0], marker='o', color=color, label=category,
                            linestyle='', markerfacecolor=color, markersize=10)
                    for category, color in present_category_colors.items()
                ]
                ax.legend(handles=handles, title=f'Estructuras Radio {radio}', loc='center left', bbox_to_anchor=(1, 0.5))

                # Etiquetas
                ax.set_xlabel(r'$\delta$', fontsize=14)
                ax.set_ylabel(r'$\lambda_{eff}$', fontsize=14)
                ax.set_title(f' Estructuras - Densidad {densidad}', fontsize=16)

                plt.grid(True)
                plt.tight_layout()

                # Guardar el archivo
                output_dir = f'C://Users//Hp//simulations//core-shell//fixed_particles_A_r_{radio}//'
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, f'energias_{radio}_rho_{densidad}.png')
                plt.savefig(output_file, dpi=300, bbox_inches='tight')
                plt.close()
        else:
            print("No se encontró la columna 'densidad'. Solo se generará una imagen general.")

    def average(self, clasification:str, color_file:str)-> None:

        # Cargar CSV
        df = pd.read_csv(clasification, skiprows=1)
        radio = df.loc[0, 'radio']

        # Preprocesamiento
        df = df.dropna(subset=['Acronimos'])
        df['Acronimos'] = df['Acronimos'].astype(str)
        df['densidad'] = pd.to_numeric(df['densidad'], errors='coerce')
        df['Energia'] = pd.to_numeric(df['Energia'], errors='coerce')

        # Cargar colores
        category_colors = self.load_category_colors(filename=color_file)

        # Valores únicos de particulaA
        particula_values = df['particulaA'].dropna().unique()

        for value in particula_values:
            subset = df[df['particulaA'] == value].copy()
            if subset.empty:
                continue

            # Mapear colores
            subset['color'] = subset['Acronimos'].map(category_colors)

            # Filtrar acrónimos únicos presentes en el subset (y que tengan color definido)
            acronimos_presentes = subset['Acronimos'].unique()
            acronimos_con_color = [acr for acr in acronimos_presentes if acr in category_colors]

            # Crear gráfico
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.scatter(subset['densidad'], subset['Energia'], c=subset['color'], s=30, alpha=0.8)

            # Crear leyenda SOLO con los acrónimos del subset
            handles = [
                plt.Line2D([0], [0], marker='o', color=category_colors[acr], label=acr,
                        linestyle='', markerfacecolor=category_colors[acr], markersize=10)
                for acr in acronimos_con_color
            ]
            ax.legend(handles=handles, title=f'Estructuras Radio {radio}', loc='center left', bbox_to_anchor=(1, 0.5))

            # Etiquetas y formato
            ax.set_xlabel(r'$\rho^{*}$', fontsize=14)
            ax.set_ylabel(r'$\lambda_{eff}$', fontsize=14)
            ax.set_title(f'Diagrama de Estructuras - particulaA {value}', fontsize=16)

            plt.grid(True)
            plt.tight_layout()

            # Guardar archivo
            output_dir = f'C://Users//Hp//simulations//core-shell//fixed_particles_A_r_{radio}'
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f'promedios_coronas_radio_{radio}_particulaA_{value}.png')
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()

    def plot_particulas_por_densidad(self, clasification, color_file):
        df = pd.read_csv(clasification, skiprows=1)
        df = df.dropna(subset=['Acronimos', 'particulaA', 'particulaB'])
        df['Acronimos'] = df['Acronimos'].astype(str)
        df['particulaA'] = pd.to_numeric(df['particulaA'], errors='coerce')
        df['particulaB'] = pd.to_numeric(df['particulaB'], errors='coerce')

        # Suponiendo que tienes una columna llamada 'densidad'
        if 'densidad' not in df.columns:
            raise ValueError("Falta la columna 'densidad' para separar por densidad")

        category_colors = self.load_category_colors(filename=color_file)

        for densidad, group in df.groupby('densidad'):
            group['color'] = group['Acronimos'].map(category_colors)
            acronimos_presentes = group['Acronimos'].unique()
            acronimos_con_color = [acr for acr in acronimos_presentes if acr in category_colors]

            fig, ax = plt.subplots(figsize=(10, 8))
            ax.scatter(group['particulaA'], group['particulaB'], c=group['color'], s=60, alpha=0.7)

            handles = [
                plt.Line2D([0], [0], marker='o', color=category_colors[acr], label=acr,
                        linestyle='', markerfacecolor=category_colors[acr], markersize=10)
                for acr in acronimos_con_color
            ]
            ax.legend(handles=handles, title='Estructuras', loc='center left', bbox_to_anchor=(1, 0.5))

            ax.set_xlabel(r'$\lambda_{A}$', fontsize=14)
            ax.set_ylabel(r'$\lambda_{B}$', fontsize=14)
            ax.set_title(rf'$\rho^{{*}}={densidad}$', fontsize=16)
            plt.grid(True)
            plt.tight_layout()

            output_file = f'particulas_A_vs_B_densidad_{densidad}.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()

            print(f'Gráfico guardado para densidad {densidad}: {output_file}')


    def plot_particulas_tamaños_por_densidad(self, clasification, color_file):

        # Cargar CSV
        df = pd.read_csv(clasification, skiprows=1)

        # Filtrar datos válidos
        df = df.dropna(subset=['Acronimos', 'particulaA', 'particulaB', 'densidad'])
        df['Acronimos'] = df['Acronimos'].astype(str)
        df['densidad'] = pd.to_numeric(df['densidad'], errors='coerce')

        # Asegurar que columnas sean numéricas
        df['particulaA'] = pd.to_numeric(df['particulaA'], errors='coerce')
        df['particulaB'] = pd.to_numeric(df['particulaB'], errors='coerce')

        # Cargar colores
        category_colors = self.load_category_colors(filename=color_file)
        df['color'] = df['Acronimos'].map(category_colors)

        # Crear carpeta para guardar los gráficos
        output_folder = 'graficos_por_densidad'
        os.makedirs(output_folder, exist_ok=True)

        # Iterar sobre cada densidad única
        for densidad_valor in sorted(df['densidad'].dropna().unique()):
            df_densidad = df[df['densidad'] == densidad_valor]

            acronimos_presentes = df_densidad['Acronimos'].unique()
            acronimos_con_color = [acr for acr in acronimos_presentes if acr in category_colors]

            fig, ax = plt.subplots(figsize=(10, 8))
            scatter = ax.scatter(df_densidad['particulaA'], df_densidad['particulaB'],
                                c=df_densidad['color'], s=50, alpha=0.8)

            handles = [
                plt.Line2D([0], [0], marker='o', color=category_colors[acr], label=acr,
                        linestyle='', markerfacecolor=category_colors[acr], markersize=10)
                for acr in acronimos_con_color
            ]
            ax.legend(handles=handles, title='Estructuras', loc='center left', bbox_to_anchor=(1, 0.5))

            ax.set_xlabel(r'$\lambda_{A}$', fontsize=14)
            ax.set_ylabel(r'$\lambda_{B}$', fontsize=14)
            ax.set_title(f'Mapa de Partículas A vs B - Densidad {densidad_valor}', fontsize=16)

            plt.grid(True)
            plt.tight_layout()

            output_file = os.path.join(output_folder, f'tamaños_A_vs_B_densidad_{densidad_valor}.png')
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()

            print(f'Gráfico guardado en: {output_file}')

    def grid_colormap_by_structure(self, clasification, color_file):

        # Leer CSV
        df = pd.read_csv(clasification, skiprows=1)

        # Limpiar datos
        df = df.dropna(subset=['Acronimos', 'particulaA', 'particulaB'])
        df['Acronimos'] = df['Acronimos'].astype(str)
        df['particulaA'] = pd.to_numeric(df['particulaA'], errors='coerce')
        df['particulaB'] = pd.to_numeric(df['particulaB'], errors='coerce')

        # Cargar mapa de colores
        category_colors = self.load_category_colors(filename=color_file)
        df['color'] = df['Acronimos'].map(category_colors)

        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 8))

        # Pintar cada celda con color de fondo y borde negro
        for _, row in df.iterrows():
            x = row['particulaA']
            y = row['particulaB']
            color = row['color']

            rect = plt.Rectangle(
                (x - 0.5, y - 0.5), 1, 1,
                facecolor=color,
                edgecolor='black',
                linewidth=0.5,
                alpha=0.7
            )
            ax.add_patch(rect)

        # Dibujar puntos encima (opcional)
        ax.scatter(df['particulaA'], df['particulaB'], c=df['color'], s=30, edgecolors='k', linewidth=0.3)

        # Leyenda solo con los acrónimos presentes
        acronimos_presentes = df['Acronimos'].unique()
        handles = [
            plt.Line2D([0], [0], marker='s', color=category_colors[acr], label=acr,
                    linestyle='', markerfacecolor=category_colors[acr], markersize=10)
            for acr in acronimos_presentes if acr in category_colors
        ]
        ax.legend(handles=handles, title='Estructuras', loc='center left', bbox_to_anchor=(1, 0.5))

        # Etiquetas y formato
        ax.set_xlabel(r'$\lambda_{A}$', fontsize=14)
        ax.set_ylabel(r'$\lambda_{B}$', fontsize=14)
        ax.set_title('Mapa estructural coloreado por celda', fontsize=16)

        # Ajustar límites y ticks
        ax.set_xticks(sorted(df['particulaA'].unique()))
        ax.set_yticks(sorted(df['particulaB'].unique()))
        ax.set_xlim(df['particulaA'].min() - 0.5, df['particulaA'].max() + 0.5)
        ax.set_ylim(df['particulaB'].min() - 0.5, df['particulaB'].max() + 0.5)
        plt.grid(True, which='both', linestyle=':', linewidth=0.3, alpha=0.5)
        plt.tight_layout()

        # Guardar imagen
        output_file = 'mapa_estructuras_celdas.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f'Gráfico guardado como: {output_file}')


def main():
    with open('particles.json', 'r') as file:
        data = json.load(file)

    scatter_plot = Grapichs()
    # for lambda_A in data['lA']:
    #     print(lambda_A)
    #     scatter_plot.diagram_structure(clasification=Path('./radio3.csv'), 
    #                              lambda_A=lambda_A
    #                          )
        
    # scatter_plot.energies( clasification=Path('./radio3.csv'),
    #                         color_file='category_color.json' 
    #                 )
    # scatter_plot.average( clasification=Path('./radio3.csv'),
    #                         color_file='category_color.json' 
    #                 )
    scatter_plot.plot_particulas_por_densidad(clasification=Path('./radio3.csv'),color_file='category_color.json')
    # scatter_plot.plot_particulas_tamaños_por_densidad(clasification=Path('./radio3.csv'), color_file='category_color.json')
if __name__ == '__main__':
    main()


# def main():
#     # Leer los valores de lambda_A desde JSON
#     with open('particles.json', 'r') as file:
#         data = json.load(file)

#     # Instancia de la clase de gráficos
#     scatter_plot = Grapichs()

#     # Lista de valores específicos de lambda_A que quieres graficar
#     selected_lambda_A = [2.5, 2.6, 2.7,2.8,2.9,3.0]  # ← Ajusta según lo que quieras mostrar en la tesis

#     # Carpeta de salida organizada para la tesis
#     output_dir = Path('./figures/thesis/')
#     output_dir.mkdir(parents=True, exist_ok=True)

#     Generar los gráficos solo para los casos seleccionados
#     for lambda_A in selected_lambda_A:
#         print(f"Generando gráfico para λ_A = {lambda_A} ...")
        
#         scatter_plot.diagram_structure(
#             clasification=Path('./radio3.csv'), 
#             lambda_A=lambda_A
#         )

#         # Mover la imagen generada a la carpeta de la tesis con un nombre claro
#         src_file = Path(f'C://Users//Hp//simulations//core-shell//fixed_particles_A_r_3//densidad_cociente_3_lA_{lambda_A}.png')
#         dst_file = output_dir / f'diagram_lambda_{lambda_A}.png'
#         src_file.rename(dst_file)


#     print("¡Gráficos listos y organizados para la tesis!")

#     scatter_plot.energies( clasification=Path('./radio3.csv'),
#                             color_file='category_color.json' 
#                     )
#     scatter_plot.average( clasification=Path('./radio3.csv'),
#                             color_file='category_color.json')
    
#     print('lo logramos')

# if __name__ == '__main__':
#     main()