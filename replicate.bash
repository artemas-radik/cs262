#thanks https://stackoverflow.com/questions/48591219/open-multiple-terminal-windows-mac-using-bash-script
shopt -s nocasematch
read -p " Execute script? (y/n): " response
if [[ $response == y ]]; then
    printf " Loading....\\n"
    dir="Dropbox/college/cs262/cs262/server.py"
    for ((x = 0; x<3; x++)); do
        base=$((6050+10*x))
        pending_file="pending_send_server$x.csv"
        printf " Open %s Terminal on port %s\\n" $x $base
        osascript -e "tell application \"Terminal\" to do script \"python3 $dir 127.0.0.1 $base $pending_file\"" >/dev/null
    done
    client_dir="Dropbox/college/cs262/cs262/client.py"
    for ((x = 0; x<2; x++)); do
        printf " Open %s Terminal for Client\\n" $((3+x))
        pending_file="pending_send_client$x.csv"
        osascript -e "tell application \"Terminal\" to do script \"python3 $client_dir 127.0.0.1 6050 6060 6070 $pending_file\"" >/dev/null
    done
fi
shopt -u nocasematch