run_in_background=$(cat ../config/config.yaml | shyaml get-value run-in-background)

if [ "$run_in_background" = True ]
then
  nohup python -u ../stocks_notifier.py &
  echo "Started in background"
else
  python ../stocks_notifier.py
fi