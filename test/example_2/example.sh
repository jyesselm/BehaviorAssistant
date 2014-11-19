
echo "python ../../ba.py -m 'First commit' dummy_script.py 1"
python ../..//ba.py -m "First commit" -c ./dummy_script.py -args 1

sleep 3

echo "python ../../ba.py -m 'Second commit' dummy_script.py 2"
python ../../ba.py -m "Second commit" -c ./dummy_script.py -args 2

echo "python ../../ba.py --render html --since '1 day ago' -ro test.html"
python ../../ba.py -m Title --render html --since "1 day ago" -ro test.html

echo "showing git log"
git --no-pager log --since "1 day ago"
echo "cleanup git log"
git reset --soft HEAD~2
