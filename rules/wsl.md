# WSL 2

## Global installer

Do not use `apt` or `apt-get` by default. Use them only as a last resort when
the preferred installers cannot meet the requirement.

## Disk space

Query the total and available space. The Linux filesystem is a
[virtual disk](https://learn.microsoft.com/en-us/windows/wsl/disk-space) that
reports its maximum size, not the free space of the Windows drive behind it, so
also check the mounted Windows drives:

```sh
df -h --output=target,size,avail -- "$PWD" /mnt/[a-z]
```
