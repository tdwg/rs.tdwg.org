#!/bin/bash -eu

# Generate a random password
password=$(< /dev/urandom tr -dc _A-Za-z0-9- | head -c20)
salt=$(< /dev/urandom tr -dc 0-9 | head -c15)
md5hash=$(echo -n admin:BaseX:$password | md5sum | cut -f 1 -d ' ')
sha256hash=$(echo -n $salt$password | sha256sum | cut -f 1 -d ' ')

cat > /basex/basex/data/users.xml <<EOF
<users>
  <user name="admin" permission="admin">
    <password algorithm="digest">
      <hash>$md5hash</hash>
    </password>
    <password algorithm="salted-sha256">
      <salt>$salt</salt>
      <hash>$sha256hash</hash>
    </password>
  </user>
</users>
EOF

# Start BaseX
/usr/local/bin/basexhttp &

# Wait until it has started up.
sleep 5

# Import the data
cd /usr/src/rs.tdwg.org/index

python3 load-db-from-github.py "$1" "$2" "$3" $password

/usr/local/bin/basexhttp stop
