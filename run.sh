# run with "bash" command, I don't know the path to include here
cd app
if [ "$1" = "app" ]; then
exec python -m uvicorn --host 0.0.0.0 main:app
elif [ "$1" = "test" ]; then
exec python -m unittest discover
else
echo Error: Invalid mode passed. Please use "app" to run the app or "test" to run the unit tests
fi