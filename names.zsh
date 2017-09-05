for i in stijn izaak lena moniek; do
    echo "lines containing $i:";
    cat brute_force_s_states.py
     | grep $(echo -n $i | sed "s/./.*&/g");
    echo;
done
