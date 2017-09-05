for i in {0..9};
  do
    echo -n $i" ";
    python brute_force_s_states.py -j 3 -m 20 -p
     | grep "^  "$i
     | wc -l;
  done
