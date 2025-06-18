start=$(gdate +%s%3N)
echo $start
#curl http://localhost:8000/dogs
curl https://9kwuvykxn3.execute-api.eu-west-3.amazonaws.com/Prod/dogs
end=$(gdate +%s%3N)
echo
echo $end
echo "Time taken: $((end - start)) milliseconds"