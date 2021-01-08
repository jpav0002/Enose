echo "Añadiendo datos a git"
git add .
echo "Realizando commits"
git commit -m "Automatic Commit ${1}"
echo "Realizando push"
git push
echo "Datos listos en repositorio"
