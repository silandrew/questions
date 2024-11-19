
# Exercises

## Mounting NFS Shares with the automounter

**Install required packages**
```
dnf install -y autofs nfs-utils
```

**Define autofs master map**
Use `man auto.mater` for documentations.
```
cat <<- EOF > /etc/auto.master.d/op01.autofs
/localhome /etc/op01.auto
EOF
```

**Define indirect mapping**
Use `man 'autofs(5)'` for documentations.
```
cat <<- EOF > /etc/op01.auto
* -fstype=nfs,sync,rw repo.rhcsa.example.com:/user-homes/&
EOF
```

**Test autofs master map**
```
automount -v -f
```

**Enable systemd unit**
```
systemctl enable --now autofs
```

**Create user group**
```
groupadd operator
```

**Create user with secondary group 'operator'**
```
useradd -G operator -M -d /localhome/op01 op01
```

**Enable SELinux Boolean NFS home dir**
```
setsebool use_nfs_home_dirs on
```

Verify
```
getsebool -a | grep use_nfs
...output omit...
use_nfs_home_dirs --> on
...output omit...
```

## Scheduling Future Tasks

**Create sample backup script**
Use `man test` for documentations.
```bash
cat <<- EOF > /user-homes/op01/backup.sh

if [[ ! -d /tmp/backup-op01 ]]; then
 mkdir /tmp/backup-op01
fi

find /user-homes/op01 \
    ! -name backup\.sh -a \ # exclude backup script
    ! -name \.\* -a \ # exclude hidden files
    -mmin -1 \ # older then 1 minute
    -type f \ # backup only files
    -exec cp {} /tmp/backup-op01 \;

tar -cvzf backup-op01-$(date '+%d-%m-%y_%H-%M').tar.gz /tmp/backup-op01

# cleanup backup tmp dir
rm /tmp/backup-op01/*
EOF
```

### Crond
Use `man crontab` for documentations.

crontab -e
```
*/2 9-18 * * 1-6 /user-homes/op01/backup.sh
```

**Test backup job**
Create dummy files:
```
touch file-{1..5}-backup{1-2}-$(date '+%d-%m-%y_%H-%M').txt

watch ls -l /user-homes/op01/
```

### Systemd Timer

```
dnf install -y sysstat
```

```
cp /usr/lib/systemd/system/sysstat-collect.timer /etc/systemd/system/<unit_name>.timer
```

```
systemctl daemon-reload
systemctl enable --now <unit_name>.timer
```

