import boto3
from botocore import UNSIGNED
from botocore.config import Config
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def extraer_metadatos_umbra():
    print("Iniciando conexión anónima con el catálogo abierto de Umbra (AWS S3)...")
    
    s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    bucket_name = 'umbra-open-data-catalog'
    prefix = 'sar-data/tasks/Purdue University Farm Plot/'
    
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    
    registros = []
    archivos_procesados = 0
    
    print("Escaneando el repositorio. Esto puede tardar unos minutos, por favor espera...\n")
    
    for page in pages:
        if 'Contents' not in page:
            continue
            
        for obj in page['Contents']:
            key = obj['Key']
            
            if key.endswith('.json'):
                try:
                    response = s3_client.get_object(Bucket=bucket_name, Key=key)
                    file_content = response['Body'].read().decode('utf-8')
                    data = json.loads(file_content)
                    
                    if 'stac_version' in data:
                        props = data.get('properties', {})
                        fila = {
                            'archivo_fuente': key.split('/')[-1],
                            'fecha_captura': props.get('datetime'),
                            'satelite': props.get('constellation', 'Umbra') + "-" + props.get('platform', ''),
                            'resolucion_rango_m': props.get('sar:resolution_range'),
                            'resolucion_azimut_m': props.get('sar:resolution_azimuth'),
                            'angulo_incidencia': props.get('view:incidence_angle'),
                        }
                    else:
                        fila = {
                            'archivo_fuente': key.split('/')[-1],
                            'fecha_captura': data.get('collectStart'),
                            'satelite': data.get('sensorId'),
                            'resolucion_rango_m': data.get('rangeResolution'),
                            'resolucion_azimut_m': data.get('azimuthResolution'),
                            'angulo_incidencia': data.get('grazingAngle'),
                        }
                    registros.append(fila)
                    
                    archivos_procesados += 1
                    if archivos_procesados % 50 == 0:
                        print(f" -> Procesados {archivos_procesados} archivos...")
                        
                except Exception:
                    pass

    df = pd.DataFrame(registros)
    
    print("\nLimpiando datos de fechas (Modo a prueba de fallos activado)...")
    
    # LA SOLUCIÓN DEFINITIVA: errors='coerce' fuerza la conversión. 
    # Si una fecha es completamente ilegible, la deja vacía en lugar de bloquear todo el programa.
    df['fecha_captura'] = pd.to_datetime(df['fecha_captura'], errors='coerce', utc=True)
    
    # Eliminamos las filas que hayan quedado sin fecha válida y ordenamos cronológicamente
    df = df.dropna(subset=['fecha_captura']).sort_values(by='fecha_captura').reset_index(drop=True)
    
    return df

def generar_analisis_visual(df):
    print("Generando gráficas de Análisis Exploratorio (EDA)...")
    sns.set_theme(style="whitegrid")
    
    plt.figure(figsize=(10, 5))
    df['año_mes'] = df['fecha_captura'].dt.to_period('M')
    df['año_mes'].value_counts().sort_index().plot(kind='bar', color='#1f77b4')
    plt.title('Distribución Temporal de Capturas SAR', fontsize=14)
    plt.tight_layout()
    plt.savefig('analisis_temporal_sar.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    dataset_sar = extraer_metadatos_umbra()
    
    dataset_sar.drop(columns=['año_mes'], errors='ignore', inplace=True)
    archivo_csv = "curated_metadata_purdue_farm.csv"
    dataset_sar.to_csv(archivo_csv, index=False)
    
    generar_analisis_visual(dataset_sar)
    
    print(f"\n¡Pipeline finalizado con éxito! El dataset y las gráficas se han guardado.")