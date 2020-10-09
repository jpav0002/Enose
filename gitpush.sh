echo "Añadiendo datos a git"
git add Data_files
echo "Realizando commits"
git commit -m "Commit ${1}"
echo "Realizando push"
git push
echo "Datos listos en repositorio"
