# Definir el directorio raíz donde se crearán las carpetas
$rootPath = "C://Users//Hp//simulations//core-shell//50_50"

# Crear la carpeta raíz si no existe
if (!(Test-Path -Path $rootPath)) {
    New-Item -Path $rootPath -ItemType Directory
}

# Definir los valores para lambdA y lambdB
$lambdA_values = @("1.1","1.2","1.3","1.4","2.1","2.2","2.3","2.4","2.5","2.6","2.7","2.8","2.9","3.0","3.1","3.2","3.3","3.4")
$lambdB_values = @("1.11", "1.21", "1.31", "1.41", "1.51", "2.10", "2.50","2.51", "2.61","2.71","2.81","2.9","3.10", "3.50", "4.10", "4.12", "4.51", "5.10", "5.50")

# Bucle principal para crear las carpetas
for ($i = 1; $i -le 3; $i++) {
    $radio_folder = "Radio_$i"
    
    for ($rho = 0.1; $rho -le 1.0; $rho += 0.1) {
        $rho_folder = "rho_{0:N1}" -f $rho
        
        foreach ($lambdA in $lambdA_values) {
            # Formatear lambdA con 1 decimal
            $lambdA_formatted = "{0:N1}" -f $lambdA
            $lambdA_folder = "lambdA_$lambdA_formatted"
            
            foreach ($lambdB in $lambdB_values) {
                $lambdB_folder = "lambdB_$lambdB"
                
                # Verificar que las variables no están vacías
                if ($radio_folder -and $rho_folder -and $lambdA_folder -and $lambdB_folder) {
                    # Ruta completa de la carpeta
                    $folder_path = Join-Path -Path $rootPath -ChildPath (Join-Path $radio_folder (Join-Path $rho_folder (Join-Path $lambdA_folder $lambdB_folder)))
                    
                    # Crear la carpeta
                    if (!(Test-Path -Path $folder_path)) {
                        New-Item -Path $folder_path -ItemType Directory -Force
                        Write-Host "Creada: $folder_path"
                    }
                } else {
                    Write-Host "Error: Una de las variables está vacía."
                }
            }
        }
    }
}

Write-Host "Árbol de carpetas creado con éxito."
