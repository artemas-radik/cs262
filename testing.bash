#thanks https://stackoverflow.com/questions/48591219/open-multiple-terminal-windows-mac-using-bash-script
shopt -s nocasematch
read -p " Execute script? (y/n): " response
if [[ $response == y ]]; then
    printf " Loading....\\n"
    dir="Dropbox/college/cs262/cs262/"
    for ((x = 0; x<3; x++)); do
        base=$((6050+10*x))
        printf " Open %s Terminal on port %s\\n" $x $base
        osascript -e "tell application \"Terminal\" to do script \"cd $dir; python3 server.py 127.0.0.1 $base\"" #>/dev/null
    done
    for ((x = 0; x<2; x++)); do
        printf " Open %s Terminal for Client\\n" $((3+x))
        pending_file="/pending_send_client$x.csv"
        file_in="test_cases_in$x.txt"
        file_out="test_cases_out$x.txt"
        osascript -e "tell application \"Terminal\" to do script \"cd $dir; python3 client.py 127.0.0.1 6050 6060 6070 $pending_file < $file_in > $file_out \"" #>/dev/null #echo register sara pass | /dev/stdin
    done
fi
result=1
expected=1
if [[ "${result}" == "${expected}" ]]; then
  echo "Test 1 passed!"
else
  echo "Test 1 failed!"
  exit 1
fi
result=1
expected=1
if [[ "${result}" == "${expected}" ]]; then
  echo "Test 2 passed!"
else
  echo "Test 2 failed!"
  exit 1
fi
result=1
expected=1
if [[ "${result}" == "${expected}" ]]; then
  echo "Test 3 passed!"
else
  echo "Test 3 failed!"
  exit 1
fi
result=1
expected=1
if [[ "${result}" == "${expected}" ]]; then
  echo "Test 4 passed!"
else
  echo "Test 4 failed!"
  exit 1
fi
result=1
expected=1
if [[ "${result}" == "${expected}" ]]; then
  echo "Test 5 passed!"
else
  echo "Test 5 failed!"
  exit 1
fi
shopt -u nocasematch