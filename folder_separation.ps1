# Define el directorio base donde se crearon las carpetas con el primer script
$baseDir = "C://Users//Hp//simulations//core-shell//50_50"

# Define los valores para los bucles
$r_values = @(3)
$rho_values = @(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
$lambdA_values = @("1.1","1.2","1.3","1.4","2.1","2.2","2.3","2.4","2.5","2.6","2.7","2.8","2.9","3.0","3.1","3.2","3.3","3.4")
$lambdB_values = @("1.11", "1.21", "1.31", "1.41", "1.51", "2.10", "2.50","2.51", "2.61","2.71","2.81","2.9","3.10", "3.50", "4.10", "4.12", "4.51", "5.10", "5.50")

# Bucle anidado para recorrer las carpetas creadas y agregar nuevos subfolders
foreach ($r in $r_values) {
    foreach ($rho in $rho_values) {
        # Ruta de la carpeta creada en el primer script
        $folder = Join-Path -Path $baseDir -ChildPath "Radio_$r"

        # Verificar si la carpeta existe
        Write-Host "Verificando carpeta: $folder"
        if (Test-Path $folder) {
            $rho_folder = Join-Path -Path $folder -ChildPath "rho_$rho"
            Write-Host "Verificando carpeta rho: $rho_folder"
            if (Test-Path $rho_folder) {
                foreach ($lambdA in $lambdA_values) {
                    $lambdA_folder = Join-Path -Path $rho_folder -ChildPath ("lambdA_$lambdA")
                    
                    # Verificar si la carpeta lA existe
                    Write-Host "Verificando carpeta lA: $lambdA_folder"

                    if (Test-Path $lambdA_folder) {
                    # Crear folders para cada valor de lambdB
                        foreach ($lambdB in $lambdB_values) {
                            $lambdB_folder = Join-Path -Path $lambdA_folder -ChildPath ("lambdB_$lambdB")
                            
                            # Verificar si la carpeta lB existe
                            Write-Host "Verificando carpeta lB: $lambdB_folder"
                            if (Test-Path $lambdB_folder) {
                                # Crear nuevo folder para r, rho, y lB
                                $folder_new_A = Join-Path -Path $lambdB_folder -ChildPath ("r_$r" + "rho$rho" + "lA$lambdA")
                                $folder_new_B = Join-Path -Path $lambdB_folder -ChildPath ("r_$r" + "rho$rho" + "lB$lambdB")
                                if (-not (Test-Path $folder_new_A)) {
                                    New-Item -Path $folder_new_A -ItemType Directory
                                    Write-Host "Creado: $folder_new_A"
                                }
                                if (-not (Test-Path $folder_new_B)) {
                                    New-Item -Path $folder_new_B -ItemType Directory
                                    Write-Host "Creado: $folder_new_B"
                                }
                            }
                        
                            } else {
                                Write-Host "Carpeta lB no encontrada: $lambdB_folder"
                            }
                        }
                    } else {
                        Write-Host "Carpeta lA no encontrada: $lambdA_folder"
                    }
                }
            } else {
                Write-Host "Carpeta rho no encontrada: $rho_folder"
            }
        } else {
            Write-Host "Carpeta no encontrada: $folder"
        }
    }


Write-Host "Nuevos subfolders agregados con éxito."
