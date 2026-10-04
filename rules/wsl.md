# WSL 2

## Global installer

Do not use `apt` or `apt-get` by default. Use them only as a last resort when
the preferred installers cannot meet the requirement.

## Disk space

Before installations, downloads, or builds over 100 MB, query the total and
available bytes. The Linux filesystem is a
[virtual disk](https://learn.microsoft.com/en-us/windows/wsl/disk-space) that
reports its maximum size, not the free space of the Windows drive behind it, so
also check the mounted Windows drives:

```sh
df -B1 --output=target,size,avail -- "$PWD" /mnt/[a-z]
```
